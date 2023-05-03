import argparse
import math
from setup import *


def parse_arguments():
    """
    Parses arguments from the command line of the form "sudoku.py --puzzle [puzzle name]
    Required: [puzzle name] is one of the available puzzles
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--puzzle", help="Desired puzzle name", type=str, choices=PUZZLES, required=True)

    args = vars(arg_parser.parse_args()) # Creates a dictionary of key = argument flag, value = argument
    return args['puzzle']


def safe_set(lst):
    """Determines if a set of nine integers is safe for Sudoku, 
    where each element in the set can be a unique integer from 1-9 or 0"""

    if set(lst) == set(range(1,10)):
        return True
    missing = 0
    for num in range(1,10): 
        if not num in lst:
            missing += 1
    if lst.count(0) == missing:
        return True
    return False



def safe(board, row, col, num): 
    """Determines if it is safe to place num at board[row][col]"""

    check_row = []
    for c in range(0,9): # check the row
        if c == col:
            check_row.append(num)
        else: 
            check_row.append(board[row][c])
    if not safe_set(check_row):
        return False

    check_col = []
    for r in range(0,9): # check the column
        if r == row: 
            check_col.append(num)
        else: 
            check_col.append(board[r][col])
    if not safe_set(check_col):
        return False

    top_left = (math.floor(row / 3) * 3, math.floor(col / 3) * 3) # get position of top left corner of current box
    check_box = []
    for r in range(top_left[0], top_left[0] + 3): # check the box
        for c in range(top_left[1], top_left[1] + 3):
            if r == row and c == col: 
                check_box.append(num)
            else: 
                check_box.append(board[r][c])
    return safe_set(check_box)


def first_unsolved(board):
    """Returns the first unsolved (row, col) position in board or (-1, -1) if no unsolved position exists"""

    pos = (-1, -1)
    for r in range(0, 9): 
        for c in range (0, 9): 
            if board[r][c] == 0: 
                pos = (r, c)
                return pos
    return pos


def new_board(board, row, col, num):
    """Creates a copy of board with the position (row, col) equal to num"""

    new_board = []
    for i in range(9):
        new_board.append([])
        for j in range(9):
            new_board[i].append(board[i][j])
    new_board[row][col] = num
    return new_board


def neighbours(board): 
    """Returns a list of boards which are "neighbours" of board, where a neighbour is 
    defined a Sudoku board that is the same as board, but contains a safe number in the
    first unsolved position on board"""

    nbrs = []
    pos = first_unsolved(board)
    if pos == (-1, -1): 
        return nbrs
    row = pos[0]
    col = pos[1]
    for i in range(1, 10): 
        if safe(board, pos[0], pos[1], i):
            nbrs.append(new_board(board, row, col, i))
    return nbrs
