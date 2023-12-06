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

class AISolver:
    def __init__(self, board):
        self.board = board        

    # minimax search with alpha-beta pruning
    def minimax(self, board, depth=7, alpha=-np.inf, beta=np.inf, maxNode=True):
        if depth == 0:
            return None, self.evaluate(board)
        if board.gameOver():
            return None, -np.inf
        if board.winGame():
            return None, np.inf
        if maxNode:
            maxEval = -np.inf
            moves = board.getAvailableMoves()
            bestMove = moves[0]
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                _, eval = self.minimax(boardCopy, depth-1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break         
            return bestMove, maxEval            
        else:            
            minEval = np.inf
            moves = board.getAvailableMoves()
            worstMove = moves[0]
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                _, eval = self.minimax(boardCopy, depth-1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    worstMove = move
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return worstMove, minEval

    
    def getNextMove(self, board):
        bestMove = None
        bestScore = -np.inf
        for move in board.getAvailableMoves():
            score = self.calculateScore(board, move)
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove
    
    def calculateScore(self, board, move):
        newBoard = copy.deepcopy(board)
        newBoard.performMove(move)
        if newBoard == board:
            return 0
        return self.generateScore(newBoard, 0, 2)
    
    def generateScore(self, board, currentDepth, maxDepth):
        if currentDepth == maxDepth:
            return self.calculateFinalScore(board)
        totalScore = 0
        for emptyTile in board.getEmptyTiles():
            # simulate placing a '2', which has 90% chance of happening
            newBoard2 = copy.deepcopy(board)
            newBoard2.addTile(emptyTile, 2)
            moveScore2 = self.calculateMoveScore(newBoard2, currentDepth, maxDepth)
            totalScore += 0.9 * moveScore2
            # simulate placing a '4', which has 10% chance of happening
            newBoard4 = copy.deepcopy(board)
            newBoard4.addTile(emptyTile, 2)
            moveScore4 = self.calculateMoveScore(newBoard4, currentDepth, maxDepth)
            totalScore += 0.1 * moveScore4
        return totalScore

    def calculateMoveScore(self, board, currentDepth, maxDepth):
        bestScore = 0
        for move in ['left', 'right', 'up', 'down']:
            newBoard = copy.deepcopy(board)
            newBoard.performMove(move)
            if newBoard.getBoard() != board.getBoard():
                score = self.generateScore(newBoard, currentDepth+1, maxDepth)
                bestScore = max(score, bestScore)
        return bestScore

    def calculateFinalScore(self, board):
        wSmooth = 10
        wEmpty = 1       
        wMerge = 1
        wMono = 1
        return (wSmooth * self.smoothness(board)        + \
                wEmpty  * self.countEmptySquares(board) + \
                wMerge  * self.getPotentialMerges(board)+ \
                wMono   * self.monotonicity(board))
    
    # s-heuristic idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    # goal is a s-shaped board where high values are at top corners and tiles that can be merged are adjacent        
    SNAKE_MATRIX = [[4**15, 4**14, 4**13, 4**12],
                    [4**8,  4**9,  4**10, 4**11],
                    [4**7,  4**6,  4**5,  4**4],
                    [4**0,  4**1,  4**2,  4**3]]
    
    GRADIENT_MATRIX = [[4**6, 4**5, 4**4, 4**3],
                       [4**5, 4**4, 4**3, 4**2],
                       [4**4, 4**3, 4**2, 4**1],
                       [4**3, 4**2, 4**1, 4**0]]
    # score of game state = dot product of game state (represented as 2D matrix) and weight matrix
    def smoothness(self, board):
        totalScore = 0
        for row in range(len(board.getBoard())):
            for col in range(len(board.getBoard())):
                totalScore += board.getBoard(row, col) * self.SNAKE_MATRIX[row][col]
        return totalScore

    # allowing the board to have more tiles that are potential merges reduces uncertainty and increases value
    def getPotentialMerges(self, board):
        horizCnt = 0
        for r in range(len(board.getBoard())):
            for c in range(len(board.getBoard())-1):
                if board.getBoard(r, c) == board.getBoard(r, c+1):
                    horizCnt *= 2
        vertCnt = 0
        for c in range(len(board.getBoard())):
            col = [board.getBoard(r, c) for r in range(len(board.getBoard()))]
            for r in range(len(col)-1):
                if board.getBoard(r, c) == board.getBoard(r+1, c):
                    vertCnt *= 2
        
        wHoriz = 1
        wVert = 0.6
        return wHoriz * horizCnt + wVert * vertCnt        
    
    def countEmptySquares(self, board):
        #bonus to more empty squares to ENCOURAGE merging        
        count = 1
        for row in range(len(board.getBoard())):
            for col in range(len(board.getBoard())):
                curNum = board.getBoard(row, col)
                if curNum == 0:
                    count *= 1.1 # increase bonus by a ratio
        return count

    # check if strictly decreasing from top to down and left to right
    def monotonicity(self, board): 
        # calculate monotonicity score for rows
        rowScores = []
        monotonicRows = 0
        for row in board.getBoard():
            rowScore = self.rowMonotonicity(row)
            rowScores.append(rowScore)        
            if all(row[i] >= row[i+1] for i in range(len(row)-1)):
                monotonicRows += 1        
        # calculate monotonicity score for columns
        colScores = []
        monotonicCols = 0
        for j in range(len(board.getBoard(0))):
            col = [self.board.getBoard(i, j) for i in range(len(board.getBoard()))]
            col_score = self.rowMonotonicity(col)
            colScores.append(col_score)
            if all(col[i] >= col[i + 1] for i in range(len(col) - 1)):
                monotonicCols += 1

        # calculate overall monotonicity score
        totalScore = sum(rowScores) + sum(colScores) + monotonicRows + monotonicCols
        return totalScore        
    
    # evaluate how well an array is strictly decreasing from left to right
    def rowMonotonicity(self, row):        
        score = 0
        for i in range(len(row)-1):
            diff = row[i] - row[i+1]
            if diff >= 0:
                score += diff
            elif diff < 0:
                score -= diff
        return score