from helperFunctions import *


def solve(board):
    """Finds a route from the starting Sudoku board to a solved board."""

    pos = first_unsolved(board) # get (row, col) indices for first unsolved cell
    if pos == (-1, -1): # indicates no unsolved position
        return board
    else: 
        
        return solve_list(neighbours(board))


def solve_list(boards):
    """Finds a route from a list of Sudoku boards to a solved board"""

    if len(boards) == 0:
        return False
    else: 
        first = solve(boards[0])
        if not first == False:
            return first
        else: 
            return solve_list(boards[1:])


def get_hint(board):
    """Finds a route from the starting Sudoku board to a solved board."""

    pos = first_unsolved(board) # get (row, col) indices for first unsolved cell
    if pos == (-1, -1): # indicates no unsolved position
        return board, True
    else:
        for nbr in neighbours(board):
            solved_board, is_valid = get_hint(nbr)
            if is_valid:
                return nbr, True # return the first valid board encountered
        return False, False
