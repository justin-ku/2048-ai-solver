from game import Board
import numpy as np

# heuristics idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
# essentially the goal is a snake-shaped board where high values are at top corners and tiles that can be merged are adjacent

WEIGHT_MATRIX = [[4**15, 4**14, 4**13, 4**12],
                 [4**8, 4**9, 4**10, 4**11],
                 [4**7, 4**6, 4**5, 4**4],
                 [4**0, 4**1, 4**2, 4**3],]

# heuristic of a game state = sum product of game state and weight matrix
def heuristic(board):
    h = 0
    for r in range(board.boardSize):
        for c in range(board.boardSize):
            h += board[r][c] * WEIGHT_MATRIX[r][c]
    return h

def minimax(board, depth, maximizingPlayer):    
    if (depth == 0 or board.gameOver): 
        return board
     
    if maximizingPlayer:
        maxEval = -np.inf
        for child in position:
            eval = minimax(child, depth-1, False)            
            maxEval = max(maxEval, eval)
        return maxEval
         
    else:
        minEval = np.inf
        for child in position:
            eval = minimax(child, depth-1, True)            
            minEval = min(minEval, eval)