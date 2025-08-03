from inference import InferencePipeline
from inference.core.interfaces.camera.entities import VideoFrame
import cv2
import json
from web3 import Web3
from dotenv import load_dotenv
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
API_KEY = os.getenv("API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# --- Blockchain setup ---
RPC_URL = "https://node.ghostnet.etherlink.com"
CHAIN_ID = 128123  # Etherlink Ghostnet
CONTRACT_ADDRESS = "0x6dFBC9C0499eb1FdF7661e9Aaf346c2e9eb044C3"
ACCOUNT_ADDRESS = "0xe1237d03373981314cfb3c0ed4a830E9e2DcD276"


with open("YogaPoseTrackerABI.json") as f:
    ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# --- Pose tracking setup ---
current_pose = None
streak = 0
max_streaks = {}
POSE_HOLD_THRESHOLD = 10

def draw_counter(frame, pose, streak, max_streaks):
    text_color = (0, 255, 0) if streak >= POSE_HOLD_THRESHOLD else (0, 0, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    y_offset = 30

    cv2.putText(frame, f"Current Pose: {pose}", (10, y_offset), font, 0.8, text_color, 2)
    cv2.putText(frame, f"Streak: {streak}", (10, y_offset + 30), font, 0.8, text_color, 2)

    y_offset += 60
    for pose_name in ["goddess", "ddog", "warrior", "tree", "plank"]:
        val = max_streaks.get(pose_name, 0)
        cv2.putText(frame, f"{pose_name}: {val}", (10, y_offset), font, 0.7, (255, 255, 0), 2)
        y_offset += 25

    cv2.putText(frame, "Press 'S' to save results to EtherLink or 'Q' to exit", (10, frame.shape[0] - 20),
                font, 0.6, (200, 200, 200), 1)

    return frame

def send_pose_streaks_to_etherlink(pose_data):
    if all(v == 0 for v in pose_data.values()):
        print("⚠️ Not sending empty data to contract.")
        return
    try:
        nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        tx = contract.functions.savePoses(
            pose_data.get("goddess", 0),
            pose_data.get("ddog", 0),
            pose_data.get("warrior", 0),
            pose_data.get("tree", 0),
            pose_data.get("plank", 0),
        ).build_transaction({
            'chainId': CHAIN_ID,
            'from': ACCOUNT_ADDRESS,
            'nonce': nonce,
            'gas': 2_000_000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })
        signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
        print("✅ Saved to Etherlink. Tx Hash:", web3.to_hex(tx_hash))
    except Exception as e:
        print("⚠️ Failed to send:", e)

def my_custom_sink(predictions: dict, video_frame: VideoFrame):
    global current_pose, streak, max_streaks, pipeline

    preds = predictions.get("predictions", [])
    frame = video_frame.image.copy()

    if preds:
        cls = preds[0].get("class", None)
        if cls == current_pose:
            streak += 1
        else:
            if current_pose:
                max_streaks[current_pose] = max(max_streaks.get(current_pose, 0), streak)
            current_pose = cls
            streak = 1
    else:
        if current_pose:
            max_streaks[current_pose] = max(max_streaks.get(current_pose, 0), streak)
        current_pose, streak = None, 0

    frame = draw_counter(frame, current_pose or "None", streak, max_streaks)
    cv2.imshow("Yoga Pose Tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        pipeline.terminate()
    elif key == ord('s'):
        pose_data = {p: max_streaks.get(p, 0) for p in ["goddess", "ddog", "warrior", "tree", "plank"]}
        #print(pose_data)
        send_pose_streaks_to_etherlink(pose_data)

pipeline = InferencePipeline.init(
    model_id="yoga-pose-detection-8eapt/1",
    api_key=API_KEY,
    video_reference=0,
    on_prediction=my_custom_sink
)

def display_leaderboard_aligned(contract):
    from IPython.display import display, HTML
    import pandas as pd

    display(HTML("<h2 style='text-align:center;'>📊 Leaderboard</h2>"))

    users, all_poses = contract.functions.getAllPoses().call()

    data = []
    for i, user in enumerate(users):
        poses = all_poses[i]
        data.append({
            '#': i + 1,
            'User': user,
            'Goddess': poses[0],
            'Downward Dog': poses[1],
            'Warrior': poses[2],
            'Tree': poses[3],
            'Plank': poses[4],
            'Total': sum(poses)
        })

    df = pd.DataFrame(data)
    df.index = [''] * len(df)

    styler = df.style.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), ('font-size', '14px')]},
        {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', '13px')]},
    ]).set_properties(
        subset=['User'], **{'text-align': 'left'}
    )

    display(styler)


display_leaderboard_aligned(contract)

pipeline.start()
pipeline.join()
cv2.destroyAllWindows()
