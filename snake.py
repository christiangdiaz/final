import os

def initialize_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    return board

def print_board(board):
    os.system('clear')
    for row in board:
        print(row)

def initialize_snake(board):
    snake = [[3,3],[3,4]]
    for segment in snake:
        board[segment[0]][segment[1]] = 'S'
    return snake

def move_snake(snake):

    return snake

def update_board(board,snake):
    for segment in snake:
        board[segment[0]][segment[1]] = 'S'
    return board


board = initialize_board()
snake = initialize_snake(board)

x=0
while x<5:
    new_snake = move_snake(snake)
    update_board(board,new_snake)
    print_board(board)



