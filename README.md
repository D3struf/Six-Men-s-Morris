# Six Men's Morris AI vs Player

This project implements a game of Six Men's Morris where a player can play against an AI opponent that utilizes the Minimax algorithm for decision-making. The game is implemented in Python.

## Table of Contents

- [Six Men's Morris AI vs Player](#six-mens-morris-ai-vs-player)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Game Rules](#game-rules)
  - [Screenshots](#screenshots)

## Introduction

Six Men's Morris is a classic strategy board game that involves two players attempting to form "mills" by aligning their pieces along predefined lines on the board. The game progresses through two phases: the placement phase and the movement phase.

This project provides an implementation of Six Men's Morris where a player can play against an AI opponent. The AI opponent uses the Minimax algorithm to make optimal moves and provide a challenging gameplay experience.

## Features

- Player vs AI gameplay
- Simple command-line interface
- Minimax algorithm for AI decision-making
- Three phases of the game: placement, movement, and mill formation

## Installation

To run the game, follow these steps:

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/your-username/six-mens-morris.git
    ```

2. Navigate to the project directory:

    ```
    cd six-mens-morris
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

To start the game, run the following command:

```
python main.py
```

Follow the on-screen instructions to play the game. Input your moves using the command-line interface and enjoy the gameplay experience!

## Game Rules

Six Men's Morris follows these basic rules:

1. Players take turns placing their pieces on the board.
2. Once all pieces are placed, players take turns moving their pieces to adjacent empty positions.
3. Forming a "mill" (three pieces in a row along a predefined line) allows a player to remove one of the opponent's pieces.
4. The game is won by either capturing all of the opponent's pieces or by leaving the opponent with fewer than three pieces that can form a mill.

For more detailed rules, refer to [Six Men's Morris Rules](https://en.wikipedia.org/wiki/Six_Men%27s_Morris#Rules).

## Screenshots

- Home Page
- Instruction Pages
- Piece Selection
- Main Game
- Pause Page
- Winner Page
