import random
import copy

class Board:    
    # initializes an empty board with two tiles (valued 2 or 4) placed on the board at random locations
    def __init__(self, boardSize=4):        
        self.boardSize = boardSize
        self.board = [[0] * boardSize for i in range(boardSize)]
        self.addTile()
        self.addTile()

    # finds all the empty tiles on the board
    def getEmptyTiles(self):
        emptyTiles = []
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == 0:
                    emptyTiles.append((i, j))
        return emptyTiles

    # add a new tile with a value of 2 or 4 at an empty tile
    def addTile(self):       
        emptyTiles = self.getEmptyTiles()
        pos = random.choice(emptyTiles)
        # like the original game, P(tile 2)=0.9 and P(tile 4)=0.1
        if random.random() < 0.9:
            val = 2
        else:
            val = 4
        self.board[pos[0]][pos[1]] = val

    # display the board on the terminal
    def __str__(self):        
        output = ''
        for row in self.board:
            # note: join() only works for list of strings
            output += '\t'.join([str(val) if val > 0 else 'x' for val in row])
            output += '\n'
        return output

    def moveLeft(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize-1):
                self.shiftLeft(row)
                curVal = self.board[row][col]
                nextVal = self.board[row][col+1]
                if curVal == nextVal:
                    self.board[row][col] *= 2
                    self.board[row][col+1] = 0
            self.shiftLeft(row)

    def shiftLeft(self, row):
        curRow = self.board[row]
        self.board[row] = [val for val in curRow if val != 0] + [0]*curRow.count(0)         
    
    def moveRight(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize-1, 0, -1):
                self.shiftRight(row)
                curVal = self.board[row][col]
                nextVal = self.board[row][col-1]
                if curVal == nextVal:
                    self.board[row][col] *= 2
                    self.board[row][col-1] = 0
            self.shiftRight(row)

    def shiftRight(self, row):
        curRow = self.board[row]
        self.board[row] = [0]*curRow.count(0) + [val for val in curRow if val != 0]        

    def moveUp(self):
        for col in range(self.boardSize):
            for row in range(self.boardSize-1):
                self.shiftUp(col)
                curVal = self.board[row][col]
                nextVal = self.board[row+1][col]
                if curVal == nextVal:
                    self.board[row][col] *= 2
                    self.board[row+1][col] = 0
            self.shiftUp(col)

    def shiftUp(self, col):
        curCol = [self.board[row][col] for row in range(self.boardSize)]
        newCol = [val for val in curCol if val != 0] + [0]*curCol.count(0)
        for row in range(self.boardSize):
            self.board[row][col] = newCol[row]
    
    def moveDown(self):
        for col in range(self.boardSize):
            for row in range(self.boardSize-1, 0, -1):
                self.shiftDown(col)
                curVal = self.board[row][col]
                nextVal = self.board[row-1][col]
                if curVal == nextVal:
                    self.board[row][col] *= 2
                    self.board[row-1][col] = 0
            self.shiftDown(col)

    def shiftDown(self, col):
        curCol = [self.board[row][col] for row in range(self.boardSize)]
        newCol = [0]*curCol.count(0) + [val for val in curCol if val != 0]
        for row in range(self.boardSize):
            self.board[row][col] = newCol[row]

    def move(self, direction):        
        originalState = copy.deepcopy(self.board)              
        if direction == 'UP':      
            self.moveUp()                                   
        elif direction == 'DOWN':
            self.moveDown()
        elif direction == 'LEFT':
            self.moveLeft()          
        elif direction == 'RIGHT':
            self.moveRight()
    
        if self.board == originalState:
            print('Dead end. Try another direction')
        else:
            self.addTile()

class Marathon:
    def __init__(self, name):
        # Implement player initialization logic
        pass

    def make_move(self):
        # Implement player move input logic
        pass

    def scores(self):
        # Store all existing highest scores as well as current score
        pass

class Sprint:
    def __init__(self, name):
        # Implement player initialization logic
        pass

    def make_move(self):
        # Implement player move input logic
        pass

    def scores(self):
        # Store all existing highest scores as well as current score
        pass

class AIPlayer:
    def __init__(self):
        # Implement AI player initialization logic
        pass

    def make_move(self, board):
        # Implement AI move logic using expectimax algorithm
        pass

    def scores(self):
        pass
        # Store all existing highest scores as well as current score

class Multiplayer:
    def __init__(self, player1, player2):
        # Implement multiplayer game initialization logic
        pass

    def play(self):
        # Implement multiplayer game logic
        pass

    def scores(self, username):
        # Store all existing highest scores as well as current score by username (or not)
        pass
