from graphics import Graphics
from game import Board, aiBoard
from ai import Minimax, Expectimax

from cmu_graphics import *

#=================================================================================================
#                                   MODEL
# NOTE: MAKE SURE NO MAGIC NUMBERS (ARE ALL RELATIVE TO BOARD/SCREEN SIZE), SO EASY TO RESIZE
#=================================================================================================

def onAppStart(app):
    # board object
    app.classicBoard = Board(False, True)
    app.aiBoard = aiBoard(False, True)   
    app.expectimaxDepth = 3
    # app.minimax = Minimax(app.aiBoard, 2)
    app.expectimax = Expectimax(app.aiBoard, app.expectimaxDepth)

    app.startAI = False

    # screen
    app.width = 1000
    app.height = 800
    
    app.modes = ['home', 'classic', 'ai']
    app.mode = 'home'

    #=================================================================================================
    #                                   HOME SCREEN
    #=================================================================================================
    # title
    app.titleX = app.width//2
    app.titleY = app.height*0.2
    app.titleSize = app.width//20
    # classic
    app.classicRectX = app.width//5
    app.classicRectY = app.height*0.45
    app.classicRectWidth = app.width//5*3
    app.classicRectHeight = app.height*0.1
    app.classicRectColor = None
    app.classicLabelX = app.titleX
    app.classicLabelY = app.height*0.5
    app.classicLabelSize = app.titleSize*0.7
    # ai    
    app.aiRectX = app.classicRectX
    app.aiRectY = app.height*0.65
    app.aiRectWidth = app.classicRectWidth
    app.aiRectHeight = app.classicRectHeight
    app.aiRectColor = None
    app.aiLabelX = app.titleX
    app.aiLabelY = app.height*0.7
    app.aiLabelSize = app.classicLabelSize    

    #=================================================================================================
    #                                   CLASSIC MODE
    #=================================================================================================
    # board outline
    app.rows = len(app.classicBoard.getBoard())
    app.cols = len(app.classicBoard.getBoard(row=0))
    app.boardWidth = app.boardHeight = 0.6*app.height
    app.boardLeft = app.width*0.4 - app.boardWidth//2
    app.boardTop = app.height*0.3
    
    # tiles
    app.cellBorderWidth = 2
    # presets
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
    #=================================================================================================
    #                                   AI MODE
    #=================================================================================================
    app.someVariable = 0

    #=================================================================================================
    #                                   MISC
    #=================================================================================================

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
    app.restartRectColor = None
    app.restartLabelX = app.restartRectX + app.restartRectWidth//2
    app.restartLabelY = app.restartRectY + app.restartRectHeight//2
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

#=================================================================================================
#                                   VIEW
#=================================================================================================

def redrawAll(app):
    if app.mode == 'home':
        drawHomeScreen(app)
    else: # (app.mode == 'classic' or app.mode == 'ai')
        drawBoard(app)        
        drawScores(app)
        drawHomeButton(app)
        drawRestartButton(app)
        # drawInstructions(app)
        if app.mode == 'ai':
            drawStartButton(app)
            drawStatsButton(app)

def drawHomeScreen(app):
    # title    
    drawLabel('2048 AI', app.titleX, app.titleY, size=app.titleSize, bold=True)
    # classic    
    drawRect(app.classicRectX, app.classicRectY, app.classicRectWidth, app.classicRectHeight, fill=app.classicRectColor, border='black')
    drawLabel('CLASSIC', app.classicLabelX, app.classicLabelY, size=app.classicLabelSize, bold=True)
    # ai    
    drawRect(app.aiRectX, app.aiRectY, app.aiRectWidth, app.aiRectHeight, fill=app.aiRectColor, border='black')
    drawLabel('AI SOLVER', app.aiLabelX, app.aiLabelY, size=app.aiLabelSize, bold=True)   

def drawBoard(app):
    if app.mode == 'classic':
        board = app.classicBoard
    elif app.mode == 'ai':
        board = app.aiBoard
    for row in range(len(board.getBoard())):
        for col in range(len(board.getBoard(0))):
            drawCell(app, row, col)
    drawBoardBorder(app)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=app.cellBorderWidth*2)

def drawCell(app, row, col):
    if app.mode == 'classic':
        board = app.classicBoard
    elif app.mode == 'ai':
        board = app.aiBoard
    # outline
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # values
    labelX = cellLeft + cellWidth//2
    labelY = cellTop + cellHeight//2
    value = board.getBoard(row, col)
    valueString = f'{value}' if value else ''
    labelColor = 'black' if value < 8 else 'white'
    # draw
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=app.colors[value], border='black',
             borderWidth=app.cellBorderWidth)
    # TODO: MAKE FONT SIZE GLOBAL
    drawLabel(valueString, labelX, labelY, font='arial', size=app.boardWidth//8, bold=True, fill=labelColor)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# tp2+: in the original 2048 game, size of score window changed as score updates
# TODO: make dimensions global
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

    # TODO: make sizes relative (build off each other, so don't need to change all)
    drawLabel('SCORE', scoreLabelX1, scoreLabelY1, bold=True, size=scoreHeight*0.25)
    if app.mode == 'classic':
        score = app.classicBoard.getScore()
    elif app.mode == 'ai':
        score = app.aiBoard.getScore()
    drawLabel(f'{score}', scoreLabelX2, scoreLabelY2, fill='white', bold=True, size=scoreHeight*0.45)
    
    if app.mode == 'classic':
        board = app.classicBoard
    elif app.mode == 'ai':
        board = app.aiBoard

    drawLabel('BEST', bestLabelX1, bestLabelY1, bold=True, size=scoreHeight*0.25)
    drawLabel(f'{board.getHighScore()}', bestLabelX2, bestLabelY2, fill='white', bold=True, size=bestHeight*0.4)

def drawHomeButton(app):
    drawRect(app.homeRectX, app.homeRectY, app.homeRectWidth, app.homeRectHeight, fill=app.homeRectColor, border='black')
    drawLabel('HOME', app.homeLabelX, app.homeLabelY, size=app.homeLabelSize, bold=True)        

def drawRestartButton(app):
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
    app.classicBoard.performMove(key)

# TODO: combine onASDFMode into one function and include input values for buttons in parameter
# OR find more efficient/cleaner way to organize button press

def onMouseMove(app, mouseX, mouseY):    
    # classic
    if onClassicMode(app, mouseX, mouseY):
        app.classicRectColor = rgb(220, 220, 220) # light gray
    else:
        app.classicRectColor = None
    
    # ai
    if onAIMode(app, mouseX, mouseY):
        app.aiRectColor = rgb(220, 220, 220) # light gray
    else:
        app.aiRectColor = None
    
    if onHomeButton(app, mouseX, mouseY):
        app.homeRectColor = rgb(220, 220, 220) # light gray
    else:
        app.homeRectColor = None

    if onRestartButton(app, mouseX, mouseY):
        app.restartRectColor = rgb(220, 220, 220) # light gray
    else:
        app.restartRectColor = None

    if onStartButton(app, mouseX, mouseY):
        app.startRectColor = rgb(220, 220, 220) # light gray
    else:
        app.startRectColor = None

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

def onHomeButton(app, mX, mY):
    homeRectX1 = app.homeRectX + app.homeRectWidth
    homeRectY1 = app.homeRectY + app.homeRectHeight
    if app.homeRectX <= mX <= homeRectX1 and \
       app.homeRectY <= mY <= homeRectY1:
        return True
    return False

def onRestartButton(app, mX, mY):
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

def onMousePress(app, mouseX, mouseY):
    if onHomeButton(app, mouseX, mouseY):
        app.mode = 'home'
        app.board = app.classicBoard
    elif onClassicMode(app, mouseX, mouseY):
        app.mode = 'classic'
    elif onAIMode(app, mouseX, mouseY):
        app.mode = 'ai'
        app.board = app.aiBoard
    elif onRestartButton(app, mouseX, mouseY):
        if app.mode == 'classic':
            app.classicBoard = Board(False, True)
            app.board = app.classicBoard
        elif app.mode == 'ai':
            app.aiBoard = aiBoard(False, True)
            app.expectimax = Expectimax(app.aiBoard, app.expectimaxDepth)
            app.board = app.aiBoard
    if onStartButton(app, mouseX, mouseY):
        app.startAI = True
    else:
        app.startAI = False

def onStep(app):
    app.stepsPerSecond = 2
    
    if app.startAI:
        aiMove = app.expectimax.getAIMove()
        if aiMove:
            app.aiBoard.performMove(aiMove)
        else:            
            app.startAI = False
            print('game over')

def main():
    runApp()

main()