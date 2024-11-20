
## Overview
This repository contains the code and resources for the Chess Robot Challenge project. The system combines AI models and Raspberry Pi hardware to detect chessboard states, predict optimal moves, solve chess puzzles, and physically execute moves on a chessboard. This project demonstrates the integration of computer vision, deep learning, and hardware control for enhanced chess gameplay and training.


## Repository Contents

### **1. AI Models and Datasets**
- **AI Models**:
  - `det_boards.h5`: A pre-trained model used for detecting the chessboard and verifying its alignment.
  - `det_pieces.h5`: A pre-trained model for identifying and classifying individual chess pieces.
- **Datasets**:
  - `openings_fen7.csv`: A dataset of chess openings containing FEN positions, best moves, and winning percentages.
  - `lichess_puzzle_transformed.csv`: A dataset of chess puzzles with FEN representations, solutions, ratings, and themes.


### **2. Codebase**

#### **AI Code**
- **`chess_openings.ipynb`**:
  - Implements a beginner chess engine that recommends openings based on winning percentages.
  - Highlights top openings for beginners with detailed explanations and visualizations.

- **`Chess-Puzzle.ipynb`**:
  - Processes the chess puzzle dataset and solves puzzles using provided move sequences.
  - Analyzes puzzle themes and difficulty levels.

- **`retarded_fen1.ipynb`**:
  - Handles FEN strings for standardizing and visualizing board states.
  - Validates AI model predictions.

- **`Clustering.ipynb`** and **`prediction_outcome.ipynb`**:
  - Notebooks supporting advanced data analysis and model performance evaluation.

#### **Raspberry Pi Code**
- **`code final.py`**:
  - Integrates Raspberry Pi hardware with AI predictions to physically execute chess moves.
  - Key Features:
    - Controls servos for moving pieces using arm coordinates.
    - Evaluates player moves with Stockfish and provides feedback.
    - Displays messages on an LCD screen and uses text-to-speech for move explanations.
  - Hardware Components:
    - Raspberry Pi Camera for capturing board images.
    - Servo motors for moving pieces on the chessboard.
    - Adafruit LCD for displaying game states.
