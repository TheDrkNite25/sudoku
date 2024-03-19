from tkinter import Tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sudokuClasses import *
from helperFunctions import *


if __name__ == '__main__':
    #ctk.set_appearance_mode("dark")
    #ctk.set_default_color_theme("blue")

    # Parse arguments to read from the correct board file
    board_name = parse_arguments()

    with open('puzzles/%s.sudoku' % board_name, 'r') as board_file:

        # Create and start the game
        game = SudokuGame(board_file)
        game.start()

        # Create the window and frames
        #app = ctk.CTk()
        app = Tk()
        app.title("Sudoku")

        #app.geometry("%dx%d" % (WIDTH, HEIGHT + BUTTONS_HEIGHT))
        app.resizable(False, False)
        SudokuGUI(app, game)

        # Launch the window
        app.mainloop()
