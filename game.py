import random
import copy

class Board:        
    def __init__(self, board):
        """Initialize an empty board with two tiles (valued 2 or 4) placed on the board at random locations"""
        self.board = board
        self.score = 0
        self.addTile()
        self.addTile()
    
    def getEmptyTiles(self):
        """Find all the empty tiles on the board"""
        emptyTiles = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == 0:
                    emptyTiles.append((r, c))
        return emptyTiles

    def addTile(self):
        """Add a new tile with a value of 2 or 4 at an empty tile"""
        emptyTiles = self.getEmptyTiles()
        if not emptyTiles:
            return
        pos = random.choice(emptyTiles)
        emptyRow, emptyCol = pos[0], pos[1]
        # P(tile 2)=0.9 and P(tile 4)=0.1
        if random.random() < 0.9:
            val = 2
        else:
            val = 4
        self.board[emptyRow][emptyCol] = val
    
    def __str__(self):
        """Display the board on the terminal in a readable format"""
        if self.gameOver():
            return 'GAME OVER'
        if self.win():
            return 'YOU WON!'
        output = ''
        for r in self.board:
            # note: join() only works for list of strings
            # use 'x' as placeholder for 0 (for now) for better readability
            output += '\t'.join([str(val) if val > 0 else 'x' for val in r])
            output += '\n'
        return output + '\n' + f'Score: {self.score}' + '\n'
    
    #=====================================Board movement==========================================    
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

        if direction == 'UP':      
            _, newScore = self.moveUp()
        elif direction == 'DOWN':
            _, newScore = self.moveDown()
        elif direction == 'LEFT':
            _, newScore = self.moveLeft()
        elif direction == 'RIGHT':
            _, newScore = self.moveRight()

        if self.board != originalState:
            self.score += sum(newScore)
            self.addTile()
        return self.board
    
    #=====================================End conditions==========================================    
    def win(self):
        """Checks if current game state is a win"""
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == 2048:
                    return True
        return False

    def gameOver(self):
        """Checks if current game state is game over"""
        boardCopy = copy.deepcopy(self.board)
        originalBoard = Board(boardCopy)

        postMoveLeft = originalBoard.moveLeft()
        postMoveRight = originalBoard.moveRight()
        postMoveUp = originalBoard.moveUp()
        postMoveDown = originalBoard.moveDown()

        if self.board == postMoveLeft and self.board == postMoveRight and \
           self.board == postMoveUp and self.board == postMoveDown:
            return True
        return False
    
    def availableMoves(self, board):
        """Get available moves under the current game state"""
        available = []
        for move in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
            boardCopy = copy.deepcopy(board)
            newBoard = boardCopy.performMove(move)
            if boardCopy != newBoard:
                available.append(move)
        return available
    
    def getScore(self):
        return self.score