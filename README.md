# 2048 AI Solver
15-112 Term Project (Fall 2023)

## Project Description
This term project aims to expand on the classic game 2048 by adding additional single-player, multiplayer, and AI game modes. Like the original 2048 game, the game is played on a 4x4 board, and the player’s controls are the arrow keys (plus WASD for multiplayer). The player’s score is determined by the tile with the highest value.

## Algorithm Overview
The expectimax algorithm was chosen for this project as 2048 satisfies all the requirements for minimax, but there extra element of chance in where the next tile could be makes expectimax is more optimal for this game. The heuristic function is calculated by the sum product of the current game state (represented as a 2D matrix) and a weight matrix, which resembles a snake-shaped board where high values are in the corners and tiles that can be merged together are adjacent. The expectimax algorithm averages the heuristics of its deepest child nodes, then recursively finds the single branch that has the highest score from all possible moves within a certain number of depths.
