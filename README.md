# 2048 AI Solver
15-112 Term Project (Fall 2023)

## Project Description
Solve the classic 2048 game using expectimax tree search with alpha beta pruning.

## Algorithm Overview
The expectimax algorithm was chosen for this project as 2048 satisfies all the requirements for minimax, but the extra element of chance in where the next tile could be adds a chance node which makes expectimax more optimal for this game. The heuristic function is calculated by the dot product of the current game state (represented as a 2D matrix) and a predefined weight matrix, which resembles a snake-shaped board where high values are in the corners and tiles that can be merged together are adjacent to each other in a descending manner. The expectimax algorithm averages the evaluation scores of the chance nodes, then recursively searches for the single branch that has the highest score from all possible moves within a certain depth. Alpha-beta pruning is then used to increase the efficiency of the search.

## Results
<!-- As of now, the expectimax algorithm consistently reaches 128 and occasionally reaches 256 or 512. -->
