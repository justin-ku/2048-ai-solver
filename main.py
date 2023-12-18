from board import Board, mtpBoard1, mtpBoard2, aiBoard
from ai import AISolver
from cmu_graphics import *
import copy

#=================================================================================================
#                                   MODEL
#=================================================================================================

def onAppStart(app):
    # board objects
    app.classicBoard = Board(False, True)
    app.aiBoard = aiBoard(False, True)   
    app.mtpBoard1 = mtpBoard1(False, True)
    app.mtpBoard2 = mtpBoard2(False, True)
        
    app.AISolver = AISolver(app.aiBoard)
    app.startAI = False

    # screen & presets
    app.width = 1000
    app.height = 800    
    app.modes = ['home', 'classic', 'multiplayer', 'ai']
    app.mode = 'home'
    app.colors = {0: rgb(204, 192, 179),
                  2: rgb(238, 228, 218),
                  4: rgb(237, 224, 200),
                  8: rgb(242, 177, 121),
                  16: rgb(245, 149, 99),
                  32: rgb(246, 124, 95),
                  64: rgb(246, 94, 59),
                  128: rgb(237, 207, 114),
                  256: rgb(237, 204, 97),
                  512: rgb(237, 200, 80),
                  1024: rgb(237, 197, 63),
                  2048: rgb(237, 194, 46),
                  4096: rgb(0, 0, 0)} # any tile with value > 2048 is black

    # title
    app.titleX = app.width//2
    app.titleY = app.height*0.2
    app.titleSize = app.width//20

    # classic mode button
    app.classicRectX = app.width//5
    app.classicRectY = app.height*0.4
    app.classicRectWidth = app.width//5*3
    app.classicRectHeight = app.height*0.1
    app.classicRectColor = None
    app.classicLabelX = app.titleX
    app.classicLabelY = app.height*0.45
    app.classicLabelSize = app.titleSize*0.7

    # multiplayer mode button
    app.mtpRectX = app.classicRectX
    app.mtpRectY = app.height*0.55
    app.mtpRectWidth = app.classicRectWidth
    app.mtpRectHeight = app.classicRectHeight
    app.mtpRectColor = None
    app.mtpLabelX = app.titleX
    app.mtpLabelY = app.height*0.6
    app.mtpLabelSize = app.classicLabelSize

    # ai mode button 
    app.aiRectX = app.classicRectX
    app.aiRectY = app.height*0.7
    app.aiRectWidth = app.classicRectWidth
    app.aiRectHeight = app.classicRectHeight
    app.aiRectColor = None
    app.aiLabelX = app.titleX
    app.aiLabelY = app.height*0.75
    app.aiLabelSize = app.classicLabelSize    
    
    # board outline (classic & ai modes)
    app.rows = len(app.classicBoard.getBoard())
    app.cols = len(app.classicBoard.getBoard(0))
    app.boardWidth = app.boardHeight = 0.6*app.height
    app.boardLeft = app.width*0.4 - app.boardWidth//2
    app.boardTop = app.height*0.3
    app.cellBorderWidth = 2
 
    # board outlines (multiplayer mode)
    app.mtpRows = len(app.mtpBoard1.getBoard())
    app.mtpCols = len(app.mtpBoard1.getBoard(0))
    app.mtpBoardWidth = app.mtpBoardHeight = 0.45*app.height
    app.mtpBoardLeft1 = app.width*0.25 - app.mtpBoardWidth//2
    app.mtpBoardLeft2 = app.width*0.75 - app.mtpBoardWidth//2
    app.mtpBoardTop = app.height*0.35
    app.mtpCellBorderWidth = 2

    # home button
    app.homeRectX = app.width*0.05
    app.homeRectY = app.height*0.05
    app.homeRectWidth = app.width*0.1
    app.homeRectHeight = app.height*0.1
    app.homeRectColor = None
    app.homeLabelX = app.width*0.1
    app.homeLabelY = app.height*0.1
    app.homeLabelSize = app.classicLabelSize*0.5

    # restart button
    app.restartRectWidth = app.width*0.1
    app.restartRectHeight = app.height*0.1
    app.restartRectX = ((app.boardLeft + app.boardWidth) + app.width)//2
    app.restartRectY = app.boardTop + app.boardHeight - app.restartRectHeight
    app.restartRectYMtp = app.mtpBoardTop + app.mtpBoardHeight + app.restartRectHeight//2
    app.restartRectColor = None
    app.restartLabelX = app.restartRectX + app.restartRectWidth//2
    app.restartLabelY = app.restartRectY + app.restartRectHeight//2
    app.restartLabelYMtp = app.restartRectYMtp + app.restartRectHeight//2
    app.restartLabelSize = app.classicLabelSize*0.5    

    # instructions
    app.instructionsLabelX1 = app.restartRectX
    app.instructionsLabelY1 = app.boardTop
    app.instructionsLabelSize1 = app.restartLabelSize
    app.instructionsLabelX2 = app.instructionsLabelX1 - app.instructionsLabelSize1//2
    app.instructionsLabelY2 = app.instructionsLabelY1*1.1
    app.instructionsLabelSize2 = app.instructionsLabelSize1 * 0.8

    # start button
    app.startRectWidth = app.restartRectWidth
    app.startRectHeight = app.restartRectHeight
    app.startRectX = app.restartRectX
    app.startRectY = app.boardTop
    app.startRectColor = None
    app.startLabelX = app.restartLabelX
    app.startLabelY = app.startRectY + app.startRectHeight//2
    app.startLabelSize = app.restartLabelSize    

    # end label
    app.endLabel = ''
#=================================================================================================
#                                   VIEW
#=================================================================================================

def redrawAll(app):
    if app.mode == 'home':
        drawHomeScreen(app)
    elif app.mode == 'multiplayer':
        drawPlayers(app)
        drawBoards(app) 
        drawScoresMtp(app)        
        drawHomeButton(app)
        drawRestartButton(app, True)
        drawEndLabel(app)      
    else: # classic or ai mode
        drawBoard(app)        
        drawScores(app)
        drawHomeButton(app)
        drawRestartButton(app)
        drawEndLabel(app)
        # drawInstructions(app)
        if app.mode == 'ai':
            drawStartButton(app)
            drawStatsButton(app)             

def drawPlayers(app):
    x1 = app.mtpBoardLeft1 + app.mtpBoardWidth//2
    x2 = app.mtpBoardLeft2 + app.mtpBoardWidth//2
    y = app.mtpBoardTop*0.6
    drawLabel('Player 1', x1, y, size=app.classicLabelSize*0.6)
    drawLabel('Player 2', x2, y, size=app.classicLabelSize*0.6)

def drawEndLabel(app):
    if app.mode == 'classic' or app.mode == 'ai':
        drawLabel(app.endLabel, app.restartRectX, app.height//2, size=app.classicLabelSize)
    else:
        drawLabel(app.endLabel, app.width//2, app.height*0.9, size=app.classicLabelSize)

def drawHomeScreen(app):
    # title
    drawLabel('2048 AI', app.titleX, app.titleY, size=app.titleSize, bold=True)
    # classic mode
    drawRect(app.classicRectX, app.classicRectY, app.classicRectWidth, app.classicRectHeight, fill=app.classicRectColor, border='black')
    drawLabel('CLASSIC', app.classicLabelX, app.classicLabelY, size=app.classicLabelSize, bold=True)
    # multiplayer mode
    drawRect(app.mtpRectX, app.mtpRectY, app.mtpRectWidth, app.mtpRectHeight, fill=app.mtpRectColor, border='black')
    drawLabel('MULTIPLAYER', app.mtpLabelX, app.mtpLabelY, size=app.mtpLabelSize, bold=True)
    # ai solve mode
    drawRect(app.aiRectX, app.aiRectY, app.aiRectWidth, app.aiRectHeight, fill=app.aiRectColor, border='black')
    drawLabel('AI SOLVER', app.aiLabelX, app.aiLabelY, size=app.aiLabelSize, bold=True)

def drawBoard(app):
    # toggle between game modes
    if app.mode == 'classic':
        board = app.classicBoard
    elif app.mode == 'ai':
        board = app.aiBoard 
    # draw board outline
    for row in range(len(board.getBoard())):
        for col in range(len(board.getBoard(0))):
            drawCell(app, row, col)
    drawBoardBorder(app)

def drawBoards(app):
    # board 1
    for row in range(len(app.mtpBoard1.getBoard())):
        for col in range(len(app.mtpBoard1.getBoard(0))):
            drawCell(app, row, col, app.mtpBoard1)
    drawBoardBorder(app, app.mtpBoard1)
    # board 2
    for row in range(len(app.mtpBoard2.getBoard())):
        for col in range(len(app.mtpBoard2.getBoard(0))):
            drawCell(app, row, col, app.mtpBoard2)
    drawBoardBorder(app, app.mtpBoard2)

# draw the board outline (with double-thickness)
def drawBoardBorder(app, mtpBoard=None):
    if mtpBoard == app.mtpBoard1:
        drawRect(app.mtpBoardLeft1, app.mtpBoardTop, app.mtpBoardWidth, app.mtpBoardHeight,
                fill=None, border='black',
                borderWidth=app.cellBorderWidth*2)
    elif mtpBoard == app.mtpBoard2:
        drawRect(app.mtpBoardLeft2, app.mtpBoardTop, app.mtpBoardWidth, app.mtpBoardHeight,
                fill=None, border='black',
                borderWidth=app.cellBorderWidth*2)
    else:
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
                fill=None, border='black',
                borderWidth=app.cellBorderWidth*2)

def drawCell(app, row, col, mtpBoard=None):
    board = None
    if app.mode == 'classic':
        board = app.classicBoard
    elif app.mode == 'ai':
        board = app.aiBoard
    elif app.mode == 'multiplayer':
        board = mtpBoard
    value = board.getBoard(row, col)
    # outline
    cellLeft, cellTop = getCellLeftTop(app, row, col, mtpBoard)
    cellWidth, cellHeight = getCellSize(app, mtpBoard)      
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=app.colors[value], border='black',
             borderWidth=app.cellBorderWidth)
    # value
    labelX = cellLeft + cellWidth//2
    labelY = cellTop + cellHeight//2
    labelSize = app.boardWidth//8
    if app.mode == 'classic' or app.mode == 'multiplayer':
        if value > 64:
            labelSize *= 0.8
        elif value > 512:
            labelSize *= 0.6
    elif app.mode == 'ai':
        if value > 512:
            labelSize *= 0.8 
    valueString = f'{value}' if value else ''
    labelColor = 'black' if value < 8 else 'white'
    drawLabel(valueString, labelX, labelY, font='arial', size=labelSize, bold=True, fill=labelColor)

def getCellLeftTop(app, row, col, mtpBoard=None):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    if mtpBoard:
        cellWidth, cellHeight = getCellSize(app, mtpBoard)
        cellLeft = (app.mtpBoardLeft1 if mtpBoard==app.mtpBoard1 else app.mtpBoardLeft2) + col * cellWidth
        cellTop = app.mtpBoardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app, mtpBoard=None):    
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    if mtpBoard:
        cellWidth = app.mtpBoardWidth / app.mtpCols
        cellHeight = app.mtpBoardHeight / app.mtpRows
    return (cellWidth, cellHeight)

def drawScores(app):
    # outline
    cellWidth, cellHeight = getCellSize(app)

    scoreX = app.width*0.4 - app.boardWidth//4 - 10
    scoreY = app.boardTop//2
    scoreWidth = cellWidth
    scoreHeight= cellHeight // 2

    bestX = scoreX + scoreWidth + 20    
    bestY = scoreY
    bestWidth = scoreWidth
    bestHeight = scoreHeight

    drawRect(scoreX, scoreY, scoreWidth, scoreHeight, fill=app.colors[0])
    drawRect(bestX, bestY, bestWidth, bestHeight, fill=app.colors[0])
    
    # values
    scoreLabelX1 = scoreX + scoreWidth // 2
    scoreLabelY1 = scoreY + scoreHeight // 4
    scoreLabelX2 = scoreLabelX1
    scoreLabelY2 = scoreY + scoreHeight // 1.5

    bestLabelX1 = bestX + bestWidth // 2
    bestLabelY1 = scoreLabelY1
    bestLabelX2 = bestLabelX1
    bestLabelY2 = scoreLabelY2

    # at the start no board exists
    score = 0
    highScore = 0

    if app.mode == 'classic':
        score = app.classicBoard.getScore()
        highScore = app.classicBoard.getHighScore()
    elif app.mode == 'ai':
        score = app.aiBoard.getScore()
        highScore = app.aiBoard.getHighScore()    

    drawLabel('SCORE', scoreLabelX1, scoreLabelY1, bold=True, size=scoreHeight*0.25)    
    drawLabel(f'{score}', scoreLabelX2, scoreLabelY2, fill='white', bold=True, size=scoreHeight*0.45)

    drawLabel('BEST', bestLabelX1, bestLabelY1, bold=True, size=scoreHeight*0.25)
    drawLabel(f'{highScore}', bestLabelX2, bestLabelY2, fill='white', bold=True, size=bestHeight*0.4)

def drawScoresMtp(app):
    # outline
    cellWidth, cellHeight = getCellSize(app, app.mtpBoard1)

    scoreX1 = app.mtpBoardLeft1 + app.mtpBoardWidth//4.5
    scoreY1 = app.mtpBoardTop*0.75
    scoreX2 = app.mtpBoardLeft2 + app.mtpBoardWidth//4.5
    scoreY2 = scoreY1
    scoreWidth = cellWidth*1.1
    scoreHeight= cellHeight*0.6

    bestX1 = scoreX1 + scoreWidth + 20
    bestY1 = scoreY1
    bestX2 = scoreX2 + scoreWidth + 20
    bestY2 = scoreY2
    bestWidth = scoreWidth
    bestHeight = scoreHeight

    drawRect(scoreX1, scoreY1, scoreWidth, scoreHeight, fill=app.colors[0])
    drawRect(bestX1, bestY1, bestWidth, bestHeight, fill=app.colors[0])
    drawRect(scoreX2, scoreY2, scoreWidth, scoreHeight, fill=app.colors[0])
    drawRect(bestX2, bestY2, bestWidth, bestHeight, fill=app.colors[0])
    
    # values

    # player 1
    scoreLabelX1P1 = scoreX1 + scoreWidth // 2
    scoreLabelY1P1 = scoreY1 + scoreHeight // 4
    scoreLabelX2P1 = scoreLabelX1P1
    scoreLabelY2P1 = scoreY1 + scoreHeight // 1.5

    bestLabelX1P1 = bestX1 + bestWidth // 2
    bestLabelY1P1 = scoreLabelY1P1
    bestLabelX2P1 = bestLabelX1P1
    bestLabelY2P1 = scoreLabelY2P1

    # player 2
    scoreLabelX1P2 = scoreX2 + scoreWidth // 2
    scoreLabelY1P2 = scoreY2 + scoreHeight // 4
    scoreLabelX2P2 = scoreLabelX1P2
    scoreLabelY2P2 = scoreY2 + scoreHeight // 1.5

    bestLabelX1P2 = bestX2 + bestWidth // 2
    bestLabelY1P2 = scoreLabelY1P2
    bestLabelX2P2 = bestLabelX1P2
    bestLabelY2P2 = scoreLabelY2P2

    score1 = app.mtpBoard1.getScore()
    highScore1 = app.mtpBoard1.getHighScore()
    score2 = app.mtpBoard2.getScore()
    highScore2 = app.mtpBoard2.getHighScore()

    # player 1
    drawLabel('SCORE', scoreLabelX1P1, scoreLabelY1P1, bold=True, size=scoreHeight*0.25)    
    drawLabel(f'{score1}', scoreLabelX2P1, scoreLabelY2P1, fill='white', bold=True, size=scoreHeight*0.45)

    drawLabel('BEST', bestLabelX1P1, bestLabelY1P1, bold=True, size=scoreHeight*0.25)
    drawLabel(f'{highScore1}', bestLabelX2P1, bestLabelY2P1, fill='white', bold=True, size=bestHeight*0.4)

    # player 2
    drawLabel('SCORE', scoreLabelX1P2, scoreLabelY1P2, bold=True, size=scoreHeight*0.25)    
    drawLabel(f'{score2}', scoreLabelX2P2, scoreLabelY2P2, fill='white', bold=True, size=scoreHeight*0.45)

    drawLabel('BEST', bestLabelX1P2, bestLabelY1P2, bold=True, size=scoreHeight*0.25)
    drawLabel(f'{highScore2}', bestLabelX2P2, bestLabelY2P2, fill='white', bold=True, size=bestHeight*0.4)

def drawHomeButton(app):
    drawRect(app.homeRectX, app.homeRectY, app.homeRectWidth, app.homeRectHeight, fill=app.homeRectColor, border='black')
    drawLabel('HOME', app.homeLabelX, app.homeLabelY, size=app.homeLabelSize, bold=True)

def drawRestartButton(app, mtp=False):
    if mtp:
        drawRect(app.restartRectX, app.restartRectYMtp, app.restartRectWidth, app.restartRectHeight, 
             fill=app.restartRectColor, border='black')
        drawLabel('RESTART', app.restartLabelX, app.restartLabelYMtp, size=app.restartLabelSize, bold=True)
    else:
        drawRect(app.restartRectX, app.restartRectY, app.restartRectWidth, app.restartRectHeight, 
                fill=app.restartRectColor, border='black')
        drawLabel('RESTART', app.restartLabelX, app.restartLabelY, size=app.restartLabelSize, bold=True)

def drawStatsButton(app):
    pass
    # drawRect()
    # drawLabel('STATS')

# work in progress
def drawInstructions(app):
    drawLabel('INSTRUCTIONS:', app.instructionsLabelX1, app.instructionsLabelY1, size=app.instructionsLabelSize1, bold=True)
    instructions = ''
    if app.mode == 'classic':
        instructions = 'Use your arrow keys to move and merge the tiles \nto reach 2048.'
    elif app.mode == 'ai':
        instructions = 'AI solves 2048'
    drawLabel(instructions, app.instructionsLabelX2, app.instructionsLabelY2, size=app.instructionsLabelSize2, align='right')

def drawStartButton(app):
    drawRect(app.startRectX, app.startRectY, app.startRectWidth, app.startRectHeight, 
             fill=app.startRectColor, border='black')
    drawLabel('START', app.startLabelX, app.startLabelY, size=app.startLabelSize, bold=True)

#=================================================================================================
#                                   CONTROLLER
#=================================================================================================

def onKeyPress(app, key):
    player1Init = app.mtpBoard1.getScore()
    player2Init = app.mtpBoard2.getScore()
    if app.mode == 'classic':
        app.classicBoard.performMove(key)
    elif app.mode == 'multiplayer':
        if not (app.mtpBoard1.gameOver() or app.mtpBoard2.gameOver()):
            if key in ['left', 'right', 'up', 'down']:
                app.mtpBoard2.performMove(key)
            elif key in ['w', 'a', 's', 'd']:
                if key == 'w':
                    move = 'up'
                elif key == 'a':
                    move = 'left'
                elif key == 's':
                    move = 'down'
                elif key == 'd':
                    move = 'right'
                app.mtpBoard1.performMove(move)
    if app.mtpBoard1.getScore() > player1Init and app.mtpBoard2.getScore() == player2Init:
        app.mtpBoard2.addTile()
    elif app.mtpBoard1.getScore() == player1Init and app.mtpBoard2.getScore() > player2Init:
        app.mtpBoard1.addTile()

# TODO: combine onASDFMode into one function and include input values for buttons in parameter
# OR find more efficient/cleaner way to organize button press

def onMouseMove(app, mouseX, mouseY):
    # classic mode  
    if onClassicMode(app, mouseX, mouseY): 
        app.classicRectColor = rgb(220, 220, 220) # light gray
    else: 
        app.classicRectColor = None   
    # multiplayer mode 
    if onMtpMode(app, mouseX, mouseY):
        app.mtpRectColor = rgb(220, 220, 220)
    else:
        app.mtpRectColor = None
    # ai solver mode  
    if onAIMode(app, mouseX, mouseY):
        app.aiRectColor = rgb(220, 220, 220)
    else:
        app.aiRectColor = None
    # home button
    if onHomeButton(app, mouseX, mouseY):
        app.homeRectColor = rgb(220, 220, 220)
    else:
        app.homeRectColor = None
    # restart button   
    if onRestartButton(app, mouseX, mouseY):
        app.restartRectColor = rgb(220, 220, 220)
    else:
        app.restartRectColor = None
    # ai start button
    if onStartButton(app, mouseX, mouseY):
        app.startRectColor = rgb(220, 220, 220)
    else:
        app.startRectColor = None

def onMousePress(app, mouseX, mouseY):
    if onHomeButton(app, mouseX, mouseY):
        app.mode = 'home'
    elif app.mode == 'home':
        if onClassicMode(app, mouseX, mouseY):
            app.mode = 'classic'
        elif onAIMode(app, mouseX, mouseY):
            app.mode = 'ai'
        elif onMtpMode(app, mouseX, mouseY):
            app.mode = 'multiplayer'
    elif app.mode == 'classic' or app.mode == 'ai':
        if onRestartButton(app, mouseX, mouseY):
            if app.mode == 'classic':
                app.classicBoard = Board(False, True)
            elif app.mode == 'ai':
                app.aiBoard = aiBoard(False, True)
                app.AISolver = AISolver(app.aiBoard)           
        elif onStartButton(app, mouseX, mouseY):
            app.startAI = True
    elif app.mode == 'multiplayer':
        if onRestartButton(app, mouseX, mouseY):
            app.mtpBoard1 = mtpBoard1(False, True)
            app.mtpBoard2 = mtpBoard2(False, True)

def onStep(app):
    app.stepsPerSecond = 1000
    if app.mode == 'classic':
        if app.classicBoard.gameOver():
            app.endLabel = 'GAME OVER'
        elif app.classicBoard.winGame():
            app.endLabel = 'YOU WON!'
        else:
            app.endLabel = ''
    elif app.mode == 'multiplayer':
        if app.mtpBoard1.winGame():
            app.endLabel = 'Player 1 won!'
        elif app.mtpBoard2.winGame():
            app.endLabel = 'Player 2 won!'
        elif app.mtpBoard1.gameOver():
            if app.mtpBoard1.getScore() < app.mtpBoard2.getScore():
                app.endLabel = 'Player 2 won!'
            elif app.mtpBoard1.getScore() >= app.mtpBoard2.getScore():
                app.endLabel = 'Player 1 won!'
        elif app.mtpBoard2.gameOver():
            if app.mtpBoard2.getScore() < app.mtpBoard1.getScore():
                app.endLabel = 'Player 1 won!'
            elif app.mtpBoard2.getScore() >= app.mtpBoard1.getScore():
                app.endLabel = 'Player 2 won!'
        else:
            app.endLabel = ''
    elif app.mode == 'ai':
        # if app.startAI and not (app.aiBoard.gameOver() or app.aiBoard.winGame()):
        if app.startAI:
            aiMove = app.AISolver.getNextMove(app.aiBoard)
            if not aiMove:
                app.startAI = False
            # aiMove, _ = app.AISolver.minimax(app.aiBoard)
            app.aiBoard.performMove(aiMove)
            app.endLabel = ''
        else:
            app.startAI = False
            if app.aiBoard.gameOver():
                app.endLabel = 'GAME OVER'
            elif app.aiBoard.winGame():
                app.endLabel = 'WOOHOO!'
            else:
                app.endLabel = ''

def onClassicMode(app, mX, mY):
    classicRectX1 = app.classicRectX + app.classicRectWidth
    classicRectY1 = app.classicRectY + app.classicRectHeight
    if app.classicRectX <= mX <= classicRectX1 and \
       app.classicRectY <= mY <= classicRectY1:
        return True
    return False

def onAIMode(app, mX, mY):
    aiRectX1 = app.aiRectX + app.aiRectWidth
    aiRectY1 = app.aiRectY + app.aiRectHeight
    if app.aiRectX <= mX <= aiRectX1 and \
       app.aiRectY <= mY <= aiRectY1:
        return True
    return False

def onMtpMode(app, mX, mY):
    mtpRectX1 = app.mtpRectX + app.mtpRectWidth
    mtpRectY1 = app.mtpRectY + app.mtpRectHeight
    if app.mtpRectX <= mX <= mtpRectX1 and \
       app.mtpRectY <= mY <= mtpRectY1:
        return True
    return False

def onHomeButton(app, mX, mY):
    homeRectX1 = app.homeRectX + app.homeRectWidth
    homeRectY1 = app.homeRectY + app.homeRectHeight
    if app.homeRectX <= mX <= homeRectX1 and \
       app.homeRectY <= mY <= homeRectY1:
        return True
    return False

def onRestartButton(app, mX, mY):    
    if app.mode == 'multiplayer':
        restartRectX1 = app.restartRectX + app.restartRectWidth
        restartRectY1 = app.restartRectYMtp + app.restartRectHeight        
        if app.restartRectX <= mX <= restartRectX1 and \
           app.restartRectYMtp <= mY <= restartRectY1:
            return True
        return False
    else: # classic or ai mode
        restartRectX1 = app.restartRectX + app.restartRectWidth
        restartRectY1 = app.restartRectY + app.restartRectHeight
        if app.restartRectX <= mX <= restartRectX1 and \
           app.restartRectY <= mY <= restartRectY1:
            return True
        return False

def onStartButton(app, mX, mY):
    startRectX1 = app.startRectX + app.startRectWidth
    startRectY1 = app.startRectY + app.startRectHeight
    if app.startRectX <= mX <= startRectX1 and \
       app.startRectY <= mY <= startRectY1:
        return True
    return False       

def main():
    runApp()

main()