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
    def __init__(self, board, maxDepth=8):
        self.board = board
        self.maxDepth = maxDepth

    def search(self, board, depth, alpha=-np.inf, beta=np.inf, maximizingPlayer=True):    
        """Implementation of minimax search with alpha-beta pruning"""
        if depth == 0 or board.gameOver():
            return self.evaluate()
                
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
                print(bestMove)
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

    #=================================================================================================
    #                                   HEURISTICS
    #=================================================================================================

    def evaluate(self):        
        """Model evaluation score as linear combination"""
        # xEdge = self.edgeBonus()
        # xSmooth = self.smoothness()
        # xMono = self.monotonicity()
        # _, xFree = self.getFreeTiles()
        # xMerge = self.getPotentialMerges()

        # tp2+: tune weights & biases using NN
        # wEdge   = 0.00001
        # wSmooth = 10
        # wMono   = 0.00001
        # wFree   = 0.00001
        # wMerge  = 0.00001

        # bEdge = 0.00001
        # bSmooth = 0.5
        # bMono = 0.00001
        # bFree = 0.00001
        # bMerge = 0.00001        

        # return (wEdge   * xEdge    + bEdge) + \
        #        (wSmooth * xSmooth  + bSmooth) + \
        #        (wMono   * xMono    + bMono)   + \
        #        (wFree   * xFree    + bFree)   + \
        #        (wMerge  * xMerge   + bMerge)
        return self.smoothness1()

    def edgeBonus(self):
        maxVal = 0
        maxCoord = (-1, -1)
        board = self.board.getBoard()
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] > maxVal:
                    maxVal = board[row][col]
                    maxCoord = (row, col)
        if maxCoord == (0, 0):
            return 100    
        return -100

    def monotonicity(self):
        """Check if strictly decreasing from top to down and left to right"""
        # Calculate monotonicity score for rows
        rowScores = []
        monotonicRows = 0
        for row in self.board.getBoard():
            rowScore = self.rowMonotonicity(row)
            rowScores.append(rowScore)            
            if all(row[i] >= row[i+1] for i in range(len(row) - 1)):
                monotonicRows += 1
        
        # Calculate monotonicity score for columns
        colScores = []
        monotonicCols = 0
        for j in range(len(self.board.getBoard(0))):
            col = [self.board.getBoard(i, j) for i in range(len(self.board.getBoard()))]
            col_score = self.rowMonotonicity(col)
            colScores.append(col_score)
            if all(col[i] >= col[i + 1] for i in range(len(col) - 1)):
                monotonicCols += 1

        # Calculate overall monotonicity score
        totalScore = sum(rowScores) + sum(colScores) + monotonicRows + monotonicCols
        return totalScore
        # return totalScore, monotonicRows, monotonicCols
    
    def rowMonotonicity(self, row):
        """Evaluate how well an array is strictly decreasing from left to right"""
        score = 0
        for i in range(len(row)-1):
            diff = row[i] - row[i+1]
            if diff >= 0:
                score += diff
            elif diff < 0:
                score -= diff
        return score

    def getPotentialMerges(self):
        horizCnt = 0
        for r in range(len(self.board.getBoard())):
            for c in range(len(self.board.getBoard())-1):
                if self.board.getBoard(r, c) == self.board.getBoard(r, c+1):
                    horizCnt += 1
        
        vertCnt = 0
        for c in range(len(self.board.getBoard())):
            col = [self.board.getBoard(r, c) for r in range(len(self.board.getBoard()))]
            for r in range(len(col)-1):
                if self.board.getBoard(r, c) == self.board.getBoard(r+1, c):
                    vertCnt += 1
        return horizCnt + vertCnt

    # positions of free tiles might impact evaluation
    def getFreeTiles(self):
        freeTiles = []
        for r in range(len(self.board.getBoard())):
            for c in range(len(self.board.getBoard())):
                if self.board.getBoard(r, c) == 0:
                    freeTiles.append((r, c))
        score = len(freeTiles)
        for tile in freeTiles:
            if tile[0] > 1 and tile[1] > 1:
                score *= 2
        return freeTiles, score

    # s-heuristic idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    # goal is a s-shaped board where high values are at top corners and tiles that can be merged are adjacent
    # weight matrix has descending weights in s-shape to reflect this
    # consistently achieves 64
    WEIGHT_MATRIX = [[2**16, 2**15, 2**14, 2**13],
                    [2**9, 2**10, 2**11, 2**12],
                    [2**8, 2**7, 2**6, 2**5],
                    [2**1, 2**2, 2**3, 2**4],]
    
    # heuristic of game state = dot product of game state (represented as 2D matrix) and weight matrix
    def smoothness1(self):
        eval = 0
        board = self.board.getBoard()
        for row in range(len(board)):
            for col in range(len(board)):
                eval += board[row][col] * self.WEIGHT_MATRIX[row][col]
        return eval
    
    def smoothness2(self):
        return self.smoothness1() * self.board.getScore()

    #=================================================================================================
    #                                   GENERATE MOVES
    #=================================================================================================

    def getAIMove(self):
        boardCopy = copy.deepcopy(self.board)        
        # bestScore, bestMove = self.search(boardCopy, self.maxDepth, alpha=-np.inf, beta=np.inf, maximizingPlayer=True)
        bestScore, bestMove = self.search(boardCopy, self.maxDepth, True)
        if bestScore == -np.inf:
            return None
        return bestMove

#=================================================================================================
# Expectimax
# - https://www.baeldung.com/cs/expectimax-search
#=================================================================================================

class Expectimax(Minimax):
    def __init__(self, board, maxDepth=8):
        super().__init__(board, maxDepth)

    def getAIMove(self):                        
        bestScore, aiMove = self.search(self.board, self.maxDepth, True)
        return aiMove
    
    # NOTE: make sure board is deep copy and not an alias of actual board
    # def search(self, board, depth, maxDepth, alpha1=-np.inf, alpha2=-np.inf, alpha3=-np.inf, alpha4=-np.inf):
    def search(self, board, depth, maximizingPlayer=True):
        if depth == 0 or board.gameOver():
            return self.evaluate(), None

        if maximizingPlayer:
            bestScore = -np.inf
            bestMove = None
            for move in board.availableMoves():
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                score = self.search(boardCopy, depth - 1, False)[0]
                if score > bestScore:
                    bestScore = score
                    bestMove = move
            if depth == self.maxDepth:
                return bestScore, bestMove
            return bestScore, None

        else:
            emptyTiles = board.getEmptyTiles()
            totalScore = 0
            totalMoves = 0
            for tile in emptyTiles:
                for value in [2, 4]:  # Assume new tile can be 2 or 4
                    boardCopy = copy.deepcopy(board)
                    (row, col) = tile
                    boardCopy.addTile((row, col), value)
                    if value == 2:
                        score = 0.9*self.search(boardCopy, depth - 1, True)[0]
                    else:
                        score = 0.1*self.search(boardCopy, depth - 1, True)[0]
                    totalScore += score
                    totalMoves += 1

            averageScore = totalScore / totalMoves if totalMoves > 0 else 0
            return averageScore, None

    def evaluate(self):
        return self.smoothness1()

    # s-heuristic idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    # goal is a s-shaped board where high values are at top corners and tiles that can be merged are adjacent
    # weight matrix has descending weights in s-shape to reflect this
    # consistently achieves 64
    WEIGHT_MATRIX = [[2**16, 2**15, 2**14, 2**13],
                    [2**9, 2**10, 2**11, 2**12],
                    [2**8, 2**7, 2**6, 2**5],
                    [2**1, 2**2, 2**3, 2**4]]
    
    # heuristic of game state = dot product of game state (represented as 2D matrix) and weight matrix
    def smoothness1(self):
        eval = 0
        board = self.board.getBoard()
        for row in range(len(board)):
            for col in range(len(board)):
                eval += board[row][col] * self.WEIGHT_MATRIX[row][col]
        return eval
    
    def smoothness2(self):
        return self.smoothness1() * self.board.getScore()

    