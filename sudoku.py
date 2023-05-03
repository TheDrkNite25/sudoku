from tkinter import Tk
import customtkinter
from sudokuClasses import *
from helperFunctions import *


if __name__ == '__main__':
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # Parse arguments to read from the correct board file
    board_name = parse_arguments()

    with open('boards/%s.sudoku' % board_name, 'r') as board_file:

        # Create and start the game
        game = SudokuGame(board_file)
        game.start()

        # Create the window and frames
        app = customtkinter.CTk(fg_color="#2b2b2b")
        app.geometry("%dx%d" % (WIDTH, HEIGHT + BUTTONS_HEIGHT))
        app.resizable(False, False)
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)
        SudokuGUI(app, game)

        # Launch the window
        app.mainloop()
