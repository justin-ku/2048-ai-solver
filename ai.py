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

    # expectimax search with alpha-beta pruning
    def expectimax(self, board, depth=2, maxNode=True):
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
                _, eval = self.expectimax(boardCopy, depth-1, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move                
            return bestMove, maxEval            
        else:            
            minEval = np.inf
            moves = board.getAvailableMoves()
            worstMove = moves[0]            
            for move in moves:
                boardCopy = copy.deepcopy(board)
                boardCopy.performMove(move)
                _, eval = self.expectimax(boardCopy, depth-1, True)
                if eval < minEval:
                    minEval = eval
                    worstMove = move
                minEval = min(minEval, eval)            
            return worstMove, minEval

    def evaluate(self, board):        
        return self.snakeHeuristic(board.getBoard())
    
    # ----------

    # def evaluate(self):        
    #     xMono = self.monotonicity()
    #     _, xFree = self.getFreeTiles()
    #     xMerge = self.getPotentialMerges()
        
    #     wMono   = 0.00001
    #     wFree   = 0.00001
    #     wMerge  = 0.00001
                
    #     bMono = 0.00001
    #     bFree = 0.00001
    #     bMerge = 0.00001        

    #     return (wMono   * xMono    + bMono)   + \
    #            (wFree   * xFree    + bFree)   + \
    #            (wMerge  * xMerge   + bMerge)               
    
    # # check if strictly decreasing from top to down and left to right
    # def monotonicity(self): 
    #     # Calculate monotonicity score for rows
    #     rowScores = []
    #     monotonicRows = 0
    #     for row in self.board.getBoard():
    #         rowScore = self.rowMonotonicity(row)
    #         rowScores.append(rowScore)        
    #         if all(row[i] >= row[i+1] for i in range(len(row)-1)):
    #             monotonicRows += 1        
    #     # Calculate monotonicity score for columns
    #     colScores = []
    #     monotonicCols = 0
    #     for j in range(len(self.board.getBoard(0))):
    #         col = [self.board.getBoard(i, j) for i in range(len(self.board.getBoard()))]
    #         col_score = self.rowMonotonicity(col)
    #         colScores.append(col_score)
    #         if all(col[i] >= col[i + 1] for i in range(len(col) - 1)):
    #             monotonicCols += 1

    #     # Calculate overall monotonicity score
    #     totalScore = sum(rowScores) + sum(colScores) + monotonicRows + monotonicCols
    #     return totalScore
    #     # return totalScore, monotonicRows, monotonicCols
    
    # def rowMonotonicity(self, row):
    #     """Evaluate how well an array is strictly decreasing from left to right"""
    #     score = 0
    #     for i in range(len(row)-1):
    #         diff = row[i] - row[i+1]
    #         if diff >= 0:
    #             score += diff
    #         elif diff < 0:
    #             score -= diff
    #     return score

    # def getPotentialMerges(self):
    #     horizCnt = 0
    #     for r in range(len(self.board.getBoard())):
    #         for c in range(len(self.board.getBoard())-1):
    #             if self.board.getBoard(r, c) == self.board.getBoard(r, c+1):
    #                 horizCnt += 1        
    #     vertCnt = 0
    #     for c in range(len(self.board.getBoard())):
    #         col = [self.board.getBoard(r, c) for r in range(len(self.board.getBoard()))]
    #         for r in range(len(col)-1):
    #             if self.board.getBoard(r, c) == self.board.getBoard(r+1, c):
    #                 vertCnt += 1
    #     return horizCnt + vertCnt

    # # positions of free tiles might impact evaluation
    # def getFreeTiles(self):
    #     freeTiles = []
    #     for r in range(len(self.board.getBoard())):
    #         for c in range(len(self.board.getBoard())):
    #             if self.board.getBoard(r, c) == 0:
    #                 freeTiles.append((r, c))
    #     score = len(freeTiles)
    #     for tile in freeTiles:
    #         if tile[0] > 1 and tile[1] > 1:
    #             score *= 2
    #     return freeTiles, score

#=================================================================================================
# Expectimax
# - https://www.baeldung.com/cs/expectimax-search
#=================================================================================================

# class Expectimax(Minimax):
class Expectimax():
    def __init__(self, board, maxDepth=3):
        # super().__init__(board, min(maxDepth, 3))
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
                bestMove = move        
        return bestMove
    
    # expectimax search
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
                maxEval += 1/len(emptyTiles) * self.search(board, depth-0.5, move)[0]
                # maxEval += 1/len(emptyTiles) * 0.9 * self.search(board, depth-0.5, move)[0]
                # board.addTile(addTileLoc, 4)
                # maxEval += 1/len(emptyTiles) * 0.1 * self.search(board, depth-0.5, move)[0]
                board.addTile(addTileLoc, 0)
        return (maxEval, move)
    
    def evaluate(self, board):
        wSnake = 0.65
        wMerge = 4.65
        xSnake = self.snakeHeuristic(board)
        xMerge = self.getPotentialMerges(board)
        return wSnake*xSnake + wMerge*xMerge

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
    WEIGHT_MATRIX_2 = [[2**25, 2**21, 2**18, 2**15],
                       [2**9,  2**10, 2**11, 2**13],
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
                eval += board[row][col] * self.WEIGHT_MATRIX_2[row][col]
        return eval
    
    # allowing the board to have more tiles that are potential merges reduces uncertainty and increases value
    def getPotentialMerges(self, board):
        horizCnt = 0
        for r in range(len(board)):
            for c in range(len(board)-1):
                if board[r][c] == board[r][c+1]:
                    horizCnt *= 2        
        vertCnt = 0
        for c in range(len(board)):
            col = [board[r][c] for r in range(len(board))]
            for r in range(len(col)-1):
                if board[r][c] == board[r+1][c]:
                    vertCnt += 1
        return horizCnt + vertCnt