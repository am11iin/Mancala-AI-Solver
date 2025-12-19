# Mancala AI Solver

![Mancala](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Mancala_board.jpg/320px-Mancala_board.jpg)

A Python implementation of the classic **Mancala** board game featuring an AI opponent powered by **Minimax** and **Alpha-Beta Pruning**. This project includes a polished **graphical interface** built with **Pygame** and supports both Human vs. AI and AI vs. AI gameplay.

---

## 🚀 Features

* 🎮 **Multiple Game Modes**
    * **Human vs. Computer:** Challenge the AI (utilizing heuristic H1).
    * **Computer vs. Computer:** Watch two AIs battle (P1: Strategic H2 vs. P2: Simple H1).
* 🧠 **Advanced AI Logic**
    * **Minimax Algorithm:** Depth-limited search for optimal decision making.
    * **Alpha-Beta Pruning:** Performance optimization to explore deeper branches.
    * **Heuristic Evaluations:**
        * **H1 (Simple):** Prioritizes the net difference in store counts.
        * **H2 (Strategic):** A sophisticated approach considering store differences, board control, and potential captures.
* 🖥️ **Graphical User Interface**
    * Interactive board built with **Pygame**.
    * Dynamic visual representation of seeds in pits and stores.
    * Real-time turn indicators and game status updates.
* ♟️ **Standard Ruleset**
    * Full implementation of standard Mancala rules.
    * Extra turn mechanics (landing in your own store).
    * Capture mechanics (landing in an empty pit on your side).
    * Automatic endgame detection and score calculation.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/am11iin/Mancala-AI-Solver.git](https://github.com/am11iin/Mancala-AI-Solver.git)
   cd Mancala-AI-Solver



How to Play:

Select Mode: Navigate the main menu to choose your preferred matchup.

Make Moves: In Human mode, simply click on the pit you wish to sow from.

Watch AI: In AI modes, the AI will automatically calculate and execute moves.

🧠 How the AI Works
The AI evaluates the game state using a Minimax tree with a default search depth. To handle the computational load, Alpha-Beta Pruning is used to "prune" branches that are guaranteed to be worse than previously explored options.

H1 (Simple): Focuses solely on the score difference in the stores.

H2 (Strategic): Evaluates the store difference plus the distribution of seeds to maintain board control and maximize capture opportunities.

🤝 Contributing
Fork the repository.

Create a new feature branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.

📜 License
Distributed under the MIT License. See LICENSE for more information.

© 2025 [am11iin]
