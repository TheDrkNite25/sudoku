# sudoku

## Overview

A Sudoku game built with the Python Tkinter library. Allows you to create custom Sudoku puzzles, and then solve them. Includes some default puzzles to get you started and a solver in case you get stuck!

## Features

- Solve the included Sudoku puzzles with a graphical interface
- Create your own custom Sudoku puzzles as plain text files, and save them so you can solve them (or have them solved for you!)
  - Validate the puzzles you create using the solver - if it does not find a solution, then your puzzle is invalid!
- Reset your work with the "Reset" button
- If you get stuck, the computer can give you a hint with the "Hint" button
  - Finds the solution and fills in one cell of the solution for you
- If you get REALLY stuck, computer solve the whole Sudoku for you with the "Solve" button

## Usage Notes

- To run: 
  - `pip install -r requirements.txt`
  - `python sudoku.py --puzzle [puzzle name]`, where "[puzzle name]" is one of the available puzzles
- To get usage help: `python sudoku.py --help` or `python sudoku.py -h`
- To save your own puzzle, create a plain text file in "boards" directory and name it "[YourBoardName].sudoku"
  - [YourBoardName] should not contain spaces - use camelCase, snake_case, or hyphens instead
  - The puzzle must be a 9x9 grid of integers (see the available puzzles for an example)
  - 0 represents an empty cell
  - Next, add your board name to the "PUZZLES" list in setup.py
  - Run the program with your new board!
- If you filled out a cell but want to change it, just click that cell and enter 0

## About the Solver

- This program uses a backtracking algorithm to solve the puzzle (depth-first search).
  - Gets the first unsolved cell (starting at the top-left)
  - Puts the first possible integer (1-9) in that cell, and then attempts to solve the resulting puzzle
  - If it can't find a solution, it moves to the next possible integer and repeats
- To visualize how the solver works, run `python sudoku.py --puzzle blank` and click "Solve". The cells will be filled out left-to-right, top-to-bottom as described above.
- The run-time of the program can increase significantly in the worst case (for typical puzzles it is quite fast). Not much I can do about that, because making an algorithm that could solve the Sudoku in polynomial time would also solve one of the biggest open problems in computer science (P = NP)!
