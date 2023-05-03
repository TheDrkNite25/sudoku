import math
import tkinter as tk
import customtkinter as ctk
from solver import *
from setup import *
from helperFunctions import *


CELL_SIZE = 50 # width of each cell
MARGIN = 20 # margin around the board
WIDTH = MARGIN * 2 + CELL_SIZE * 9 
HEIGHT = MARGIN * 2 + CELL_SIZE * 9
BUTTONS_HEIGHT = 60
BUTTON_WIDTH = 10


class SudokuError(Exception): 
    """Error class for this program"""

    pass


class SudokuGUI(tk.Frame): 
    """A Tkinter GUI class that draws the Sudoku game and accepts user input"""

    def __init__(self, parent, game):
        """SudokuUI constructor"""

        self.game = game
        self.parent = parent
        self.row, self.col = -1, -1

        self.__initialize_ui()

    def __initialize_ui(self):
        """Initializes the UI with a blank canvas and buttons"""

        # Create the top frame with a canvas
        top_frame = tk.Frame(self.parent, width=WIDTH, height=HEIGHT)#, bg="#2b2b2b")
        top_frame.pack(side="top", fill="both", expand=True)
        self.canvas = tk.Canvas(top_frame, width=500, height=500, highlightthickness=0, bg="#2b2b2b")
        self.canvas.pack(fill="both", expand=True)

        # Create the bottom frame with three buttons
        bottom_frame_background = tk.Frame(self.parent, width=WIDTH, height=BUTTONS_HEIGHT, bg="#2b2b2b")
        bottom_frame_background.pack(side="bottom", fill="x")

        bottom_frame = tk.Frame(bottom_frame_background, width=WIDTH, height=BUTTONS_HEIGHT, bg="#2b2b2b")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 20))

        reset_button = ctk.CTkButton(bottom_frame, text="Reset", cursor="hand2", width=BUTTON_WIDTH, command=self.__reset)
        reset_button.pack(side="left", padx=(0, 7))
        hint_button = ctk.CTkButton(bottom_frame, text="Hint", cursor="hand2", width=BUTTON_WIDTH, command=self.__hint)
        hint_button.pack(side="left", padx=7)
        solve_button = ctk.CTkButton(bottom_frame, text="Solve", cursor="hand2", width=BUTTON_WIDTH, command=self.__solve)
        solve_button.pack(side="right", padx=(7, 0))

        bottom_frame.grid_columnconfigure(0, weight=1)
        reset_button.pack(side="left", fill="x", expand=True)
        solve_button.pack(side="left", fill="x", expand=True)
        hint_button.pack(side="left", fill="x", expand=True)

        self.__draw_grid()
        self.__draw_puzzle()

        # Bind left click and key press
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self): 
        """Draws the Sudoku grid"""

        for i in range(10):
            colour = "#878787"

            if i % 3 != 0:
                # Draw vertical lines
                x0 = MARGIN + i * CELL_SIZE
                y0 = MARGIN
                x1 = MARGIN + i * CELL_SIZE
                y1 = HEIGHT - MARGIN
                self.canvas.create_line(x0, y0, x1, y1, fill=colour)

                # Draw horizontal lines
                x0 = MARGIN 
                y0 = MARGIN + i * CELL_SIZE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * CELL_SIZE
                self.canvas.create_line(x0, y0, x1, y1, fill=colour)

        for i in range(10):
            colour = "#356fa9"

            if i % 3 == 0:
                # Draw vertical lines
                x0 = MARGIN + i * CELL_SIZE
                y0 = MARGIN
                x1 = MARGIN + i * CELL_SIZE
                y1 = HEIGHT - MARGIN
                self.canvas.create_line(x0, y0, x1, y1, fill=colour, width=1.5)

                # Draw horizontal lines
                x0 = MARGIN 
                y0 = MARGIN + i * CELL_SIZE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * CELL_SIZE
                self.canvas.create_line(x0, y0, x1, y1, fill=colour, width=1.5)


    def __draw_puzzle(self): 
        """Draws the current state of the Sudoku game"""

        self.canvas.delete("numbers") # remove previous numbers

        for i in range(9): # iterate over rows and columns to create a cell
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0: # if answer isn't blank, then save x,y coordinates of cell and fill in the number
                    x = MARGIN + j * CELL_SIZE + CELL_SIZE / 2
                    y = MARGIN + i * CELL_SIZE + CELL_SIZE / 2
                    original = self.game.start_puzzle[i][j]
                    if answer == original: # prefilled numbers are black, inputed numbers are green
                        colour = "#dde4ef"
                    else: 
                        colour = "orange"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=colour) # set text of canvas to answer

    def __hightlight_cell(self): 
        """Highlights the cell the user clicks on with a red box"""

        self.canvas.delete("highlight")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * CELL_SIZE
            y0 = MARGIN + self.row * CELL_SIZE
            x1 = MARGIN + (self.col + 1) * CELL_SIZE
            y1 = MARGIN + (self.row + 1) * CELL_SIZE
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="orange", width=1.5, tags="highlight")

    def __draw_victory(self):
        """Draw the "You Win!" message"""

        x0 = y0 = MARGIN + CELL_SIZE * 2
        x1 = y1 = MARGIN + CELL_SIZE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        x = y = MARGIN + 4 * CELL_SIZE + CELL_SIZE / 2
        self.canvas.create_text(x, y, text="You win!", tags="victory", fill="white", font=("Arial", 32)) 

    def __draw_no_solution(self):
        """Draw the "No Solution" message"""

        x0 = y0 = MARGIN + CELL_SIZE * 2
        x1 = y1 = MARGIN + CELL_SIZE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags="fail", fill="dark orange", outline="orange")
        x = y = MARGIN + 4 * CELL_SIZE + CELL_SIZE / 2
        self.canvas.create_text(x, y, text="No solution!", tags="fail", fill="white", font=("Arial", 26))

    def __cell_clicked(self, event):
        """Take action if a cell is clicked"""

        if self.game.game_over:
            return

        x, y = event.x, event.y # get x,y location of the click
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            row, col = int(math.floor((y - MARGIN) / CELL_SIZE)), int(math.floor((x - MARGIN) / CELL_SIZE)) # get row,col from x,y coordinates
            if (row, col) == (self.row, self.col): # deselect the cell if it's already selected
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] >= 0 and self.game.puzzle_dup[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__hightlight_cell()

    def __key_pressed(self, event):
        """Take action if a key is pressed"""

        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890": # set the cell value to the input and redraw the board
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__hightlight_cell()
            if self.game.check_win(): # check if this new value completes the Sudoku
                self.__draw_victory()

    def __reset(self):
        """Remove any messages and reset the puzzle"""

        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("fail")
        self.__draw_puzzle()

    def __solve(self):
        """Solve the Sudoku puzzle"""

        solution = solve(self.game.puzzle) # call the solve algorithm and get the actual solution
        if not solution: # handle the no solution case
            self.__draw_no_solution()
        else: 
            self.game.puzzle = solution
            if not self.game.check_win(): # another no solution case (full starting board, but a not correct solution)
                self.__draw_no_solution()
            self.__draw_puzzle()

    def __hint(self):
        """Provide a hint by filling out one square of the puzzle"""

        first_step = get_hint(self.game.puzzle)[0] # call the solve algorithm for only the first step
        if not first_step: # handle the no solution case
            self.__draw_no_solution()
        else:
            self.game.puzzle = first_step
            self.__draw_puzzle()


class SudokuBoard(object): 
    """An Python object representation of a Sudoku puzzle"""

    def __init__(self, board_file):
        """SudokuBoard constructor"""

        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        """Create the starting Sudoku board from board_file"""

        board = [] # initial board matrix

        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError("Each line in the sudoku puzzle must be 9 chars long.")
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError("Valid characters for a sudoku puzzle must be in 0-9")
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")

        return board


class SudokuGame(object): 
    """A Python object representation of a Sudoku game"""

    def __init__(self, board_file):
        """SudokuGame constructor"""

        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board # create the board

    def start(self):
        """Start the Sudoku game"""

        self.game_over = False
        self.puzzle = []
        self.puzzle_dup = [] # duplicate board to differentiate b/w starting values and user-inputed values
        for i in range(9):
            self.puzzle.append([])
            self.puzzle_dup.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])
                self.puzzle_dup[i].append(self.start_puzzle[i][j])

    def check_win(self):
        """Check if the Sudoku board has been solved"""

        for row in range(9): # check each row
            if not self.__check_row(row):
                return False
        for column in range(9): # check each column
            if not self.__check_column(column):
                return False
        for row in range(3): # check each 3x3 square
            for column in range(3):
                if not self.__check_square(row, column):
                    return False       

        self.game_over = True
        return True

    # Helper functions for check_win:

    def __check_block(self, block): 
        """Checks if block is solved"""

        return set(block) == set(range(1,10))

    def __check_row(self, row):
        """Checks if a row is solved"""

        return self.__check_block(self.puzzle[row])

    def __check_column(self, col):
        """Checks if a column is solved"""

        return self.__check_block(
            [self.puzzle[row][col] for row in range(9)]
        )

    def __check_square(self, row, col):
        """Checks if the 3x3 block containing (row,col) is solved"""

        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(col * 3, (col + 1) * 3)
            ]
        )
