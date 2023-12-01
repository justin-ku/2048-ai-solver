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

    def getBestMove(self, depth=2):  
        bestScore = -np.inf
        bestMove = 'left'
        moves = self.board.getAvailableMoves()
        for move in moves:
            boardCopy = copy.deepcopy(self.board)
            boardCopy.performMove(move)
            score, newMove = self.search(boardCopy, depth, move)
            if score > bestScore:
                bestScore = score
                bestMove = newMove   
        return bestMove

    def search(self, board, depth, alpha=-np.inf, beta=np.inf, maximizingPlayer=True):    
        """Implementation of minimax search with alpha-beta pruning"""
        if depth == 0 or board.gameOver():
            return self.evaluate()                
        if maximizingPlayer:
            moves = board.getAvailableMoves()            
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
            moves = board.getAvailableMoves()                    
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

    def evaluate(self):
        """Model evaluation score as linear combination"""
        xEdge = self.edgeBonus()
        xMono = self.monotonicity()
        _, xFree = self.getFreeTiles()
        xMerge = self.getPotentialMerges()

        # tp2+: tune weights & biases using NN
        wEdge   = 0.00001        
        wMono   = 0.00001
        wFree   = 0.00001
        wMerge  = 0.00001

        bEdge = 0.00001        
        bMono = 0.00001
        bFree = 0.00001
        bMerge = 0.00001        

        return (wEdge   * xEdge    + bEdge)   + \
               (wMono   * xMono    + bMono)   + \
               (wFree   * xFree    + bFree)   + \
               (wMerge  * xMerge   + bMerge)

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

#=================================================================================================
# Expectimax
# - https://www.baeldung.com/cs/expectimax-search
#=================================================================================================

class Expectimax(Minimax):
    def __init__(self, board, maxDepth=3):
        super().__init__(board, min(maxDepth, 3))

    def getBestMove(self, depth=2): 
        bestScore = -np.inf
        bestMove = 'left'
        moves = self.board.getAvailableMoves()
        for move in moves:
            boardCopy = copy.deepcopy(self.board)
            boardCopy.performMove(move)
            score, newMove = self.search(boardCopy, depth, move)
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove
    
    def search(self, board, depth, move=None):
        if board.gameOver():
            return -np.inf, move
        elif depth < 0:
            return self.evaluate(board.getBoard()), move
        
        maxEval = 0
        if depth != int(depth):
            maxEval = -np.inf
            moves = board.getAvailableMoves()
            for move in moves:
                boardCopy = copy.deepcopy(board)
                eval = self.search(boardCopy, depth-0.5, move)[0]
                maxEval = max(maxEval, eval)
        elif depth == int(depth):
            maxEval = 0
            emptyTiles = board.getEmptyTiles()            
            for addTileLoc in emptyTiles:                
                board.addTile(addTileLoc, 2)
                # maxEval += 1/len(emptyTiles) * self.search(board, depth-0.5, move)[0]
                maxEval += 1/len(emptyTiles) * 0.9 * self.search(board, depth-0.5, move)[0]
                board.addTile(addTileLoc, 4)
                maxEval += 1/len(emptyTiles) * 0.1 * self.search(board, depth-0.5, move)[0]
                board.addTile(addTileLoc, 0)
        return (maxEval, move)
    
    def evaluate(self, board):
        wSnake = 10
        wFree = 0.01
        xSnake = self.snakeHeuristic(board)
        _, xFree = self.getFreeTiles(board)
        return wSnake*xSnake + wFree*xFree

    # positions of free tiles might impact evaluation
    def getFreeTiles(self, board):
        score = 0
        freeTiles = []
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 0:
                    freeTiles.append((r, c)) 
                    score += 2
                    if r > 1 and c > 1:
                        score += 2
        return freeTiles, len(freeTiles)

    # s-heuristic idea adopted from: https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    # goal is a s-shaped board where high values are at top corners and tiles that can be merged are adjacent
    WEIGHT_MATRIX_2 = [[2**16, 2**15, 2**14, 2**13],
                       [2**9,  2**10, 2**11, 2**12],
                       [2**8,  2**7,  2**6,  2**5],
                       [2**1,  2**2,  2**3,  2**4]]
    
    WEIGHT_MATRIX_4 = [[4**15, 4**14, 4**13, 4**12],
                       [4**8,  4**9,  4**10, 4**11],
                       [4**7,  4**6,  4**5,  4**4],
                       [4**0,  4**1,  4**2,  4**3]]
    
    # heuristic of game state = dot product of game state (represented as 2D matrix) and weight matrix
    def snakeHeuristic(self, board):
        eval = 0
        for row in range(len(board)):
            for col in range(len(board)):
                eval += board[row][col] * self.WEIGHT_MATRIX_4[row][col]
        return eval
    
    def snakeHeuristic2(self, board):
        return board.getScore() * self.snakeHeuristic(board)
    