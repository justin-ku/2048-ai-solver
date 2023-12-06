import random
import copy

class Board:    
    highScore = 0

    def __init__(self, board=False, addTiles=False):        
        if not board:
            self.board = [[0] * 4 for i in range(4)]     
        else:
            self.board = board
        if addTiles:
            self.addTile()
            self.addTile()
        self.score = 0

    def getBoard(self, row=-1, col=-1):
        if row == -1 and col == -1:
            return self.board
        elif col == -1:
            return self.board[row]
        elif row == -1:
            return [self.board[row][col] for row in range(len(self.board))]
        else:
            return self.board[row][col]

    def getEmptyTiles(self):        
        emptyTiles = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == 0:
                    emptyTiles.append((r, c))
        return emptyTiles

    def getScore(self):
        return self.score

    def getHighScore(self):
        if self.winGame() or self.gameOver():
            if self.score > Board.highScore:
                Board.highScore = self.score
        return Board.highScore

    def getAvailableMoves(self):
        available = []
        for move in ['left', 'right', 'up', 'down']:
            boardCopy = copy.deepcopy(self)   
            newBoard = boardCopy.performMove(move)
            if self.board != newBoard:
                available.append(move)
        return available

    def addTile(self, location=None, value=None):
        emptyTiles = self.getEmptyTiles()
        if not emptyTiles:
            return []
        pos = random.choice(emptyTiles)
        emptyRow, emptyCol = pos[0], pos[1]
        
        if value:
            if location:
                (row, col) = location
                self.board[row][col] = value
            else:
                self.board[emptyRow][emptyCol] = value
        else: # P(tile 2)=0.9 and P(tile 4)=0.1         
            val = 0
            if random.random() < 0.9:
                val = 2
            else:
                val = 4
            self.board[emptyRow][emptyCol] = val

    # print the board on the terminal for efficient testing
    def __str__(self):
        output = ''
        for r in self.board:
            # note: join() only works for list of strings
            # use 'x' as placeholder for 0 for better readability
            output += '\t'.join([str(val) if val > 0 else 'x' for val in r])
            output += '\n'
        output += '\n' + f'Score: {self.score}' + '\n'
        if self.gameOver():
            output += 'GAME OVER'
        if self.win():
            output += 'YOU WON!'
        return output
    
    def moveLeft(self):
        newScores = []
        for r in range(len(self.board)):
            for c in range(len(self.board)-1):
                self.shiftLeft(r)
                curVal = self.board[r][c]
                nextVal = self.board[r][c+1]
                if curVal == nextVal:
                    self.board[r][c] *= 2
                    self.board[r][c+1] = 0
                    newScores.append(self.board[r][c])
            self.shiftLeft(r)
        return self.board, newScores

    def shiftLeft(self, r):
        curRow = self.board[r]
        self.board[r] = [val for val in curRow if val != 0] + [0]*curRow.count(0)         
    
    def moveRight(self):
        newScores = []
        for r in range(len(self.board)):
            for c in range(len(self.board)-1, 0, -1):
                self.shiftRight(r)
                curVal = self.board[r][c]
                nextVal = self.board[r][c-1]
                if curVal == nextVal:
                    self.board[r][c] *= 2
                    self.board[r][c-1] = 0
                    newScores.append(self.board[r][c])
            self.shiftRight(r)
        return self.board, newScores

    def shiftRight(self, r):
        curRow = self.board[r]
        self.board[r] = [0]*curRow.count(0) + [val for val in curRow if val != 0]        

    def moveUp(self):
        newScores = []
        for c in range(len(self.board)):
            for r in range(len(self.board)-1):
                self.shiftUp(c)
                curVal = self.board[r][c]
                nextVal = self.board[r+1][c]
                if curVal == nextVal:
                    self.board[r][c] *= 2
                    self.board[r+1][c] = 0
                    newScores.append(self.board[r][c])
            self.shiftUp(c)
        return self.board, newScores

    def shiftUp(self, c):
        curCol = [self.board[r][c] for r in range(len(self.board))]
        newCol = [val for val in curCol if val != 0] + [0]*curCol.count(0)
        for r in range(len(self.board)):
            self.board[r][c] = newCol[r]

    def moveDown(self):
        newScores = []
        for c in range(len(self.board)):
            for r in range(len(self.board)-1, 0, -1):
                self.shiftDown(c)
                curVal = self.board[r][c]
                nextVal = self.board[r-1][c]
                if curVal == nextVal:
                    self.board[r][c] *= 2
                    self.board[r-1][c] = 0
                    newScores.append(self.board[r][c])
            self.shiftDown(c)
        return self.board, newScores

    def shiftDown(self, c):
        curCol = [self.board[r][c] for r in range(len(self.board))]
        newCol = [0]*curCol.count(0) + [val for val in curCol if val != 0]
        for r in range(len(self.board)):
            self.board[r][c] = newCol[r]

    def performMove(self, direction):             
        originalState = copy.deepcopy(self.board)

        if direction == 'up':      
            _, newScores = self.moveUp()
        elif direction == 'down':
            _, newScores = self.moveDown()
        elif direction == 'left':
            _, newScores = self.moveLeft()
        elif direction == 'right':
            _, newScores = self.moveRight()

        if self.board != originalState:
            self.score += sum(newScores)
            self.addTile()
        return self.board

    def winGame(self):        
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == 2048:
                    return True
        return False

    def gameOver(self):        
        return not self.getAvailableMoves()

class mtpBoard1(Board):
    highScore = 0
    def __init__(self, board=False, addTiles=False):
        super().__init__(board, addTiles)
    
    def getHighScore(self):        
        if self.score > mtpBoard1.highScore:
            mtpBoard1.highScore = self.score
        return mtpBoard1.highScore

class mtpBoard2(Board):
    highScore = 0
    def __init__(self, board=False, addTiles=False):
        super().__init__(board, addTiles)
    
    def getHighScore(self):        
        if self.score > mtpBoard2.highScore:
            mtpBoard2.highScore = self.score
        return mtpBoard2.highScore

class aiBoard(Board):
    highScore = 0

    def __init__(self, board=False, addTiles=False):
        super().__init__(board, addTiles)
    
    def getHighScore(self):
        if self.winGame() or self.gameOver():
            if self.score > aiBoard.highScore:
                aiBoard.highScore = self.score
        return aiBoard.highScore