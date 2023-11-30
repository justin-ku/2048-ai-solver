from game import Board
import numpy as np
import copy

#=================================================================================================
# Minimax & alpha-beta pruning: 
# - https://www.youtube.com/watch?v=5oXyibEgJr0
# - https://www.youtube.com/watch?v=l-hh51ncgDI
# - https://www.youtube.com/watch?v=xBXHtz4Gbdo
# - https://www.cs.cmu.edu/~15281-s20/recitations/rec5/rec5_mtreview_sol.pdf
# Heuristics:
# - Monotonicity: https://theresamigler.files.wordpress.com/2020/03/2048.pdf          
# - Merges, free tiles: https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
#=================================================================================================

class Minimax:
    def __init__(self, maxDepth=8):
        self.maxDepth = maxDepth

    def search(self, board, depth, alpha=-np.inf, beta=np.inf, maximizingPlayer=True):    
        """Implementation of minimax search with alpha-beta pruning"""
        if depth == 0 or board.gameOver():
            return self.evaluate(board)
                
        if maximizingPlayer:
            moves = board.availableMoves()            
            maxEval = -np.inf
            bestMove = moves[0]
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)                
                eval = self.search(boardCopy, depth-1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if depth == self.maxDepth:
                return bestMove, maxEval
            return maxEval            
            
        else:
            moves = board.availableMoves()                    
            minEval = np.inf
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                eval = self.search(boardCopy, depth-1, alpha, beta, True)            
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def evaluate(self, board):        
        """Model evaluation score as linear combination in the form of wx+b to be tuned using NN"""
        xSmooth = self.smoothness(board)
        xMono = self.monotonicity(board)
        xFree = self.getFreeTiles(board)
        xMerge = self.getPotentialMerges(board)

        # constants tuning tbd
        wSmooth = 0.1
        wMono = 0.01
        wFree = 0.005
        wMerge = 0.1

        bSmooth = 0.1
        bMono = 0.01
        bFree = 0.01
        bMerge = 0.05

        return (wSmooth * xSmooth  + bSmooth) + \
               (wMono   * xMono    + bMono)   + \
               (wFree   * xFree    + bFree)   + \
               (wMerge  * xMerge   + bMerge)

    def monotonicity(self, board):
        # Calculate monotonicity score for rows
        rowScores = []
        monotonicRows = 0
        for row in board:
            rowScore = self.rowMonotonicity(row)
            rowScores.append(rowScore)            
            if all(row[i] >= row[i+1] for i in range(len(row) - 1)):
                monotonicRows += 1
        
        # Calculate monotonicity score for columns
        colScores = []
        monotonicCols = 0
        for j in range(len(board[0])):
            col = [board[i][j] for i in range(len(board))]
            col_score = self.rowMonotonicity(col)
            colScores.append(col_score)
            if all(col[i] >= col[i + 1] for i in range(len(col) - 1)):
                monotonicCols += 1

        # Calculate overall monotonicity score
        totalScore = sum(rowScores) + sum(colScores)
        return totalScore
        # return totalScore, monotonicRows, monotonicCols
    
    def rowMonotonicity(self, row):
        score = 0
        for i in range(len(row)-1):
            diff = row[i] - row[i+1]
            if diff > 0:
                score += diff
            elif diff < 0:
                score -= diff
        return score

    def getPotentialMerges(self, board):
        horizCnt = 0
        for r in range(len(board)):
            for c in range(len(board)-1):
                if board[r][c] == board[r][c+1]:
                    horizCnt += 1
        
        vertCnt = 0
        for c in range(len(board)):
            col = [board[r][c] for r in range(len(board))]
            for r in range(len(col)-1):
                if board[r][c] == board[r+1][c]:
                    vertCnt += 1
        return horizCnt + vertCnt

    def getFreeTiles(self, board):
        freeTiles = []
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 0:
                    freeTiles.append((r, c))
        if freeTiles == []:
            return None
        return freeTiles

    # snake-heuristic idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    # goal is a snake-shaped board where high values are at top corners and tiles that can be merged are adjacent
    # weight matrix has descending weights in snake-shape to reflect this
    WEIGHT_MATRIX = [[4**15, 4**14, 4**13, 4**12],
                    [4**8, 4**9, 4**10, 4**11],
                    [4**7, 4**6, 4**5, 4**4],
                    [4**0, 4**1, 4**2, 4**3],]
    
    # heuristic of game state = dot product of game state (represented as 2D matrix) and weight matrix
    def smoothness(self, board):
        h = 0
        for r in range(board.boardSize):
            for c in range(board.boardSize):
                h += board[r][c] * self.WEIGHT_MATRIX[r][c]
        return h

#=================================================================================================
# Expectimax
# - https://www.baeldung.com/cs/expectimax-search
#=================================================================================================

class Expectimax:
    def __init__(self, maxDepth=8):
        self.maxDepth = maxDepth

    def expectimax(self, board, depth, maximizingPlayer=True):    
        """Implementation of expectimax search"""
        if depth == 0 or board.gameOver():
            return self.evaluate(board)
                
        if maximizingPlayer:
            moves = board.availableMoves()            
            maxEval = -np.inf
            bestMove = moves[0] if moves else None
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)                
                eval = self.expectimax(boardCopy, depth-1, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
            if depth == self.maxDepth:
                return bestMove, maxEval
            return maxEval
            
        else:
            moves = board.availableMoves()                 
            avgEval = 0
            probability = 1 / len(moves) if len(moves) > 0 else 0  # Equal probability for each move
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                eval = self.expectimax(boardCopy, depth-1, True)            
                avgEval += probability * eval
            return avgEval