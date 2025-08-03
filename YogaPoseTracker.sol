// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract YogaPoseTracker {
    struct Poses {
        uint256 goddess;
        uint256 ddog;
        uint256 warrior;
        uint256 tree;
        uint256 plank;
    }

    mapping(address => Poses) public userPoses;
    address[] public users;

    function savePoses(
        uint256 goddess,
        uint256 ddog,
        uint256 warrior,
        uint256 tree,
        uint256 plank
    ) public {
        Poses storage current = userPoses[msg.sender];

        // Only push address once if first time
        if (
            current.goddess == 0 &&
            current.ddog == 0 &&
            current.warrior == 0 &&
            current.tree == 0 &&
            current.plank == 0
        ) {
            users.push(msg.sender);
        }

        // Update only if new value is greater
        if (goddess > current.goddess) current.goddess = goddess;
        if (ddog > current.ddog) current.ddog = ddog;
        if (warrior > current.warrior) current.warrior = warrior;
        if (tree > current.tree) current.tree = tree;
        if (plank > current.plank) current.plank = plank;
    }

    function getAllPoses() public view returns (address[] memory, Poses[] memory) {
        Poses[] memory allData = new Poses[](users.length);
        for (uint256 i = 0; i < users.length; i++) {
            allData[i] = userPoses[users[i]];
        }
        return (users, allData);
    }
}
