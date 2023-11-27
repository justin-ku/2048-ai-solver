from graphics import Graphics
from game import Board

from pynput import keyboard
from pynput.keyboard import Key

initialBoard = [[0] * 4 for i in range(4)]
board = Board(initialBoard)
print('Initial state... ')
print(board)

def move_(board, dir, n):
    for i in range(n):
        print('' + dir + ' arrow key pressed...')
        board.performMove(dir)
        print(board)

def on_key_release(key):
    if key == Key.esc or board.win() or board.gameOver():
        exit()
    elif key == Key.right:
        move_(board, 'RIGHT', 1)
    elif key == Key.left:
        move_(board, 'LEFT', 1)
    elif key == Key.up:
        move_(board, 'UP', 1)
    elif key == Key.down:
        move_(board, 'DOWN', 1)

with keyboard.Listener(on_release=on_key_release) as listener:
    listener.join()

def main():
    print('Game ended')
main()