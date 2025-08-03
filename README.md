
# 🧘 Yoga Pose Tracker with Etherlink Integration

This Python application uses real-time video and AI inference to detect yoga poses, track pose streaks, and store top performance data on the **Etherlink (Tezos) blockchain**. A leaderboard of all users' best pose streaks can be displayed and verified on-chain.

## 📦 Features

- Real-time webcam-based yoga pose detection
- Visual feedback of current pose and streak
- Keyboard shortcuts to save pose data to Etherlink
- Persistent leaderboard stored on a smart contract
- Styled leaderboard display (Jupyter Notebook-compatible)

---

## 🛠️ Requirements

- Python 3.8+
- OpenCV
- Roboflow `inference` SDK
- Web3.py
- Pandas
- Python Dotenv
- Smart contract deployed to Etherlink Ghostnet

---

## 🔧 Installation

1. **Clone this repo:**
   ```bash
   git clone https://github.com/yourusername/yoga-pose-tracker.git
   cd yoga-pose-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```
   API_KEY=your_roboflow_api_key
   PRIVATE_KEY=your_etherlink_private_key
   ```

4. **Ensure you have `YogaPoseTrackerABI.json` in the root directory.**

---

## ▶️ Usage

```bash
python yoga_pose_tracker.py
```

- Press `S` to **save your max streaks** to Etherlink.
- Press `Q` to quit the app.

---

## 🧠 Supported Poses

| Pose Name      | Label in Model |
|----------------|----------------|
| Goddess        | goddess        |
| Downward Dog   | ddog           |
| Warrior        | warrior        |
| Tree           | tree           |
| Plank          | plank          |

---

## 🧾 Blockchain Info

- **Chain**: Etherlink Ghostnet (Testnet)
- **Contract Address**: [`0x6dFBC9C0499eb1FdF7661e9Aaf346c2e9eb044C3`](https://testnet.explorer.etherlink.com/address/0x6dFBC9C0499eb1FdF7661e9Aaf346c2e9eb044C3)
- **Chain ID**: `128123`

The smart contract stores:
- Each user's wallet address
- Their best streaks for 5 poses

---

## 📊 Leaderboard

A leaderboard can be rendered in **Jupyter Notebook** using the built-in function:

```python
display_leaderboard_aligned(contract)
```

It shows:
- Wallet address
- Pose scores
- Total score
- Rank

---

## 🔐 Security Notes

- Do **not** share your `.env` file or `PRIVATE_KEY`.
- This version uses the Ghostnet testnet. Do not use mainnet keys or tokens.

---

## 📜 License

MIT License

---

## 🤝 Credits

- [Roboflow](https://roboflow.com) for inference SDK
- [Etherlink](https://etherlink.com) for blockchain infrastructure
- Yoga pose detection model: `yoga-pose-detection-8eapt/1` (Roboflow)

---
