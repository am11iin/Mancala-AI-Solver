# Mancala AI Solver

![Mancala](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Mancala_board.jpg/320px-Mancala_board.jpg)

A Python implementation of the classic **Mancala** board game with an AI opponent using **Minimax** and **Alpha-Beta Pruning**. Includes a **graphical interface** built with **Pygame** and supports both Human vs AI and AI vs AI modes.

---

## Features

- 🎮 **Game Modes**
  - Human vs Computer (AI uses simple heuristic H1)  
  - Computer vs Computer (P1: strategic heuristic H2, P2: simple heuristic H1)
  
- 🧠 **AI Implementation**
  - Minimax algorithm with depth-limited search  
  - Alpha-Beta pruning for performance optimization  
  - Multiple heuristics:
    - **H1:** Simple heuristic based on store difference  
    - **H2:** Strategic heuristic including board control

- 🖥️ **Graphical User Interface**
  - Interactive board using **Pygame**  
  - Visual representation of seeds in pits and stores  
  - Real-time game status and turn indicators  
  - Clickable pits for human moves

- ♟️ **Game Rules**
  - Standard Mancala rules  
  - Extra turn when last seed lands in own store  
  - Capture opponent's seeds when landing in empty own pit  
  - Automatic game over detection and winner calculation

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/am11iin/Mancala-AI-Solver.git
cd Mancala-AI-Solver

2 . Install dependencies (Python 3.10+ recommended):
pip install pygame

## Usage

Run the game:
python mancala.py
Navigate the menu to choose:

Human vs Computer

Computer vs Computer

Click pits to make moves (Human mode)

Watch the AI think and make moves automatically


How AI Works

The AI uses Minimax to evaluate all possible moves up to a depth limit (MAX_DEPTH=4)

Alpha-Beta pruning improves efficiency by skipping branches that cannot yield better outcomes

Two heuristics guide decision-making:

H1 (Simple): Focuses on the difference in store counts

H2 (Strategic): Considers both store differences and seed distribution on the board

Screenshots

Game Menu with mode selection

In-game board view with seeds and AI moves

Contributing

Fork the repository

Create a new branch

Make changes and commit

Push to your fork and create a pull request

License

MIT License © 2025
Feel free to use and modify this project for educational purposes.
Check the endgame screen for the winner
