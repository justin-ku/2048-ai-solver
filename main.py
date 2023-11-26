from graphics import Graphics
from game import Board

from pynput import keyboard
from pynput.keyboard import Key

board = Board()
print('Initial state... ')
print(board)

def move_(board, dir, n):
    for i in range(n):
        print('Moving ' + dir + '...')
        board.move(dir)
        print(board)

def on_key_release(key):
    if key == Key.right:
        # print("RIGHT")
        move_(board, 'RIGHT', 1)
    elif key == Key.left:
        # print("LEFT")
        move_(board, 'LEFT', 1)
    elif key == Key.up:
        # print("UP")
        move_(board, 'UP', 1)
    elif key == Key.down:
        # print("DOWN")
        move_(board, 'DOWN', 1)
    elif key == Key.esc:
        exit()

with keyboard.Listener(on_release=on_key_release) as listener:
    listener.join()

def main():
    print('Game ended')
main()