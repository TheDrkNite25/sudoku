import math
from tkinter import Canvas, Frame, BOTH
import customtkinter
from solver import *
from setup import *
from helperFunctions import *


CELL_SIZE = 50 # width of each cell
MARGIN = 20 # margin around the board
WIDTH = MARGIN * 2 + CELL_SIZE * 9 
HEIGHT = MARGIN * 2 + CELL_SIZE * 9
BUTTONS_HEIGHT = 100


class SudokuError(Exception): 
    """Error class for this program"""

    pass


class SudokuGUI(Frame): 
    """A Tkinter GUI class that draws the Sudoku game and accepts user input"""

    def __init__(self, parent, game):
        """SudokuUI constructor"""

        self.game = game
        self.parent = parent
        self.row, self.col = -1, -1

        self.__initialize_ui()

    def __initialize_ui(self):
        """Initializes the UI with a blank board_canvas and buttons"""

        self.parent.title("Sudoku")

        self.window_frame = customtkinter.CTkFrame(self.parent, width=WIDTH, height=HEIGHT, border_width=2, border_color="purple")
        #self.window_frame.pack(fill=BOTH, expand=True)
        self.window_frame.grid(row=0, column=0)
        self.window_frame.grid_rowconfigure(0, weight=1)
        self.window_frame.grid_columnconfigure(0, weight=1)

        self.board_canvas = Canvas(self.window_frame, width=WIDTH, height=HEIGHT, bg="#2b2b2b", highlightthickness=0)
        #self.board_canvas.pack(fill=BOTH, expand=True)
        self.board_canvas.grid(row=0, column=0)

        self.button_container = customtkinter.CTkFrame(self.parent, width=WIDTH, height=BUTTONS_HEIGHT, border_width=2, border_color="purple")
        self.button_container.grid(row=1, column=0, padx=15)
        self.button_container.grid_rowconfigure(0, weight=1)
        self.button_container.grid_columnconfigure(0, weight=1)

        reset_button = customtkinter.CTkButton(self.button_container, text="Reset", cursor="hand2", command=self.__reset)
        reset_button.grid(row=0, column=0, padx=5, pady=20)

        solve_button = customtkinter.CTkButton(self.button_container, text="Solve", cursor="hand2", command=self.__solve)
        solve_button.grid(row=0, column=1, padx=5, pady=20)

        self.__draw_grid()
        self.__draw_puzzle()

        self.board_canvas.bind("<Button-1>", self.__cell_clicked) # binding for left click
        self.board_canvas.bind("<Key>", self.__key_pressed) # binding for key press

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
                self.board_canvas.create_line(x0, y0, x1, y1, fill=colour)

                # Draw horizontal lines
                x0 = MARGIN 
                y0 = MARGIN + i * CELL_SIZE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * CELL_SIZE
                self.board_canvas.create_line(x0, y0, x1, y1, fill=colour)

        for i in range(10):
            colour = "#356fa9"

            if i % 3 == 0:
                # Draw vertical lines
                x0 = MARGIN + i * CELL_SIZE
                y0 = MARGIN
                x1 = MARGIN + i * CELL_SIZE
                y1 = HEIGHT - MARGIN
                self.board_canvas.create_line(x0, y0, x1, y1, fill=colour, width=1.5)

                # Draw horizontal lines
                x0 = MARGIN 
                y0 = MARGIN + i * CELL_SIZE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * CELL_SIZE
                self.board_canvas.create_line(x0, y0, x1, y1, fill=colour, width=1.5)


    def __draw_puzzle(self): 
        """Draws the current state of the Sudoku game"""

        self.board_canvas.delete("numbers") # remove previous numbers

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
                    self.board_canvas.create_text(x, y, text=answer, tags="numbers", fill=colour) # set text of board_canvas to answer

    def __hightlight_cell(self): 
        """Highlights the cell the user clicks on with a red box"""

        self.board_canvas.delete("highlight")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * CELL_SIZE
            y0 = MARGIN + self.row * CELL_SIZE
            x1 = MARGIN + (self.col + 1) * CELL_SIZE
            y1 = MARGIN + (self.row + 1) * CELL_SIZE
            self.board_canvas.create_rectangle(x0, y0, x1, y1, outline="orange", width=1.5, tags="highlight")

    def __draw_victory(self):
        """Draw the "You Win!" message"""

        x0 = y0 = MARGIN + CELL_SIZE * 2
        x1 = y1 = MARGIN + CELL_SIZE * 7
        self.board_canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        x = y = MARGIN + 4 * CELL_SIZE + CELL_SIZE / 2
        self.board_canvas.create_text(x, y, text="You win!", tags="victory", fill="white", font=("Arial", 32)) 

    def __draw_no_solution(self):
        """Draw the "No Solution" message"""

        x0 = y0 = MARGIN + CELL_SIZE * 2
        x1 = y1 = MARGIN + CELL_SIZE * 7
        self.board_canvas.create_oval(x0, y0, x1, y1, tags="fail", fill="dark orange", outline="orange")
        x = y = MARGIN + 4 * CELL_SIZE + CELL_SIZE / 2
        self.board_canvas.create_text(x, y, text="No solution!", tags="fail", fill="white", font=("Arial", 26))

    def __cell_clicked(self, event):
        """Take action if a cell is clicked"""

        if self.game.game_over:
            return

        x, y = event.x, event.y # get x,y location of the click
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.board_canvas.focus_set()
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
        """Remove any messages and reset the board"""

        self.game.start()
        self.board_canvas.delete("victory")
        self.board_canvas.delete("fail")
        self.__draw_puzzle()

    def __solve(self):
        """Solve the Sudoku board"""

        solution = solve(self.game.puzzle) # call the solve algorithm
        if not solution: # handle the no solution case
            self.__draw_no_solution()
        else: 
            self.game.puzzle = solution
            if not self.game.check_win(): # another no solution case (full starting board, but a not correct solution)
                self.__draw_no_solution()
            self.__draw_puzzle()


class SudokuBoard(object): 
    """An Python object representation of a Sudoku board"""

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
