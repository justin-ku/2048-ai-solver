# 2048Friends
15-112 Term Project (Fall 2023)

## Project Description
The project aims to recreate the classic 2048 game with additional multiplayer and AI game modes. In the multiplayer game mode, two human players compete to reach the highest score before the other player. In the AI game mode, the AI solves the game using expectimax tree search.

## How To Run
Install cmu_112_graphics: Download this python file (install-cmu-graphics.py: https://www.cs.cmu.edu/~112/notes/install-cmu-graphics.py) and and run it with Python 3.11 (or 3.10, but very preferably 3.11) in VS Code.
To play the game, run the main.py file with cmd+b or ctrl+b.

## Algorithm Overview
The expectimax algorithm was chosen for this project as 2048 satisfies all the requirements for minimax, but the extra element of chance in where the next tile could be adds a chance node which makes expectimax more optimal for this game. The heuristic function is calculated by the dot product of the current game state (represented as a 2D matrix) and a predefined weight matrix, which resembles a snake-shaped board where high values are in the corners and tiles that can be merged together are adjacent to each other in a descending manner. The expectimax algorithm averages the evaluation scores of the chance nodes, then recursively searches for the single branch that has the highest score from all possible moves within a certain depth. Alpha-beta pruning is then used to increase the efficiency of the search.

<!-- ## Results
As of now, the expectimax algorithm consistently reaches 128 and occasionally reaches 256 or 512. -->
