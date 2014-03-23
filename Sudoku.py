# the display need to be improved _yu
#!/usr/bin
# Sudoku solver
# Authors: Josiah Matlack and Jason Lee
# Usage: python Sudoku.py <filename> <b, f>

import struct, string, math
import sys
import copy
import time

# This will be the game object your player will manipulate
class SudokuBoard:

    # The constructor for the SudokuBoard
    def __init__(self, size, board):
        self.BoardSize = size #the size of the board
        self.CurrentGameboard = board #the current state of the game board
        self.SquareSize = int(math.sqrt(self.BoardSize)) #the size of a subsquare on the board
        self.empty_squares = [] #the list of empty squares
        self.possible_values = {} #a dictionary mapping possible values to empty squares
        self.ConsistencyChecks = 0 #a counter for the total number of consistency checks

    # This function will create a new sudoku board object with
    # with the input value placed on the GameBoard row and col are
    # both zero-indexed
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col] = value #add the value to the appropriate position on the board
   
    # Get the value on the board at position (row, col)
    def get_value(self, row, col):
        return self.CurrentGameboard[row][col]

    # Get the squares on the board that are empty at initialization
    def get_empty_squares(self):
        empty_squares = []
        for i in range(0, self.BoardSize):
            for j in range(0, self.BoardSize):
                if (self.get_value(i, j) == 0):
                    empty_squares.append((i, j))
        return empty_squares

    # Get a set of valid values for the square at position (row, col)
    def get_values(self, row, col):
        values = []
        for num in range(1, self.BoardSize + 1):
            if (self.check_rowcol(row, col, num) and self.check_subsquare(row, col, num)):
                values.append(num)
        return values

    # Store the valid values of each empty square into a dictionary
    def check_values(self):
        for es in self.empty_squares:
            pv = self.get_values(es[0], es[1])
            self.possible_values[es] = pv

    # Get the empty squares from the same row and column as the current square
    def get_rowcol_squares(self, row, col):
        squares = []
        for i in range(0, self.BoardSize):
            if (self.get_value(row, i) == 0):
                squares.append((row, i))
            if (self.get_value(i, col) == 0):
                squares.append((i, col))
        return squares

    # Get the empty squares from the same square as the current square
    def get_square_squares(self, row, col):
        squares = []
        row = int((row / self.SquareSize)) * self.SquareSize
        col = int((col / self.SquareSize)) * self.SquareSize
        row = int(row)
        col = int(col)

        for i in range(0, self.SquareSize):
            for j in range(0, self.SquareSize):
                if (self.get_value((row + i), (col + j)) == 0):
                    squares.append((row + i, col + j))
        return squares

    # Check the validity of num over row and column (row, col)
    def check_rowcol(self, row, col, num):
        self.ConsistencyChecks += 1
        for i in range(0, self.BoardSize):
            if ((self.get_value(row, i) == num) or (self.get_value(i, col) == num)):
                return False
        return True

    # Check the validity of num over subsquare s
    def check_subsquare(self, row, col, num):
        row = int((row / self.SquareSize)) * self.SquareSize
        col = int((col / self.SquareSize)) * self.SquareSize
        row = int(row)
        col = int(col)

        for i in range(0, self.SquareSize):
            for j in range(0, self.SquareSize):
                if (self.get_value((row + i), (col + j)) == num):
                    return False
        return True

    # Get the neighboring blank squares to position (row, col)
    def get_neighboring_squares(self, row, col):
        neighbor_squares = []
        blanks = self.get_rowcol_squares(row, col) + self.get_square_squares(row, col)
        for b in blanks:
            if ((b not in neighbor_squares) and (b != (row, col))):
                neighbor_squares.append(b)
        return neighbor_squares

    # Perform forward checking on the neighboring blank squares of position (row, col)
    def validate(self, row, col, num):
        neighbor_squares = self.get_neighboring_squares(row, col)
        for n in neighbor_squares:
            self.ConsistencyChecks += 1
            valid = self.possible_values[n]
            if (num in valid):
                self.possible_values[n].remove(num)
                if (len(self.possible_values[n]) == 0):
                    return False
        return True

    def mvc(self):
        next_square = [0, 0]
        temp = -1
        for i in range (0, self.BoardSize):
            for j in range (0, self.BoardSize):
                if self.get_value(i, j) != 0:
                    continue
                restric = 0;
                for num in range (0, self.BoardSize):
                    if self.get_value(num, j) != 0:
                        restric += 1
                    if self.get_value(i, num) != 0:
                        restric += 1
                if restric > temp:
                    next_square.pop()
                    next_square.pop()
                    next_square.append(i)
                    next_square.append(j)
                    temp = restric
        if temp == -1:
            return False
        return next_square
                 
    # Solve the puzzle using backtracking
    def solve_backtracking(self):
        if (self.ConsistencyChecks > 120000000):
            print ("Consistency checks exceed a reasonable number, terminating program")
            sys.exit(0)
        if self.mvc() == False:
            return True
        else:    
            row = self.mvc()[0]
            col = self.mvc()[1]
            for num in range(1, self.BoardSize + 1):
                if (self.check_rowcol(row, col, num) and self.check_subsquare(row, col, num)):
                    self.set_value(row, col, num)
                    if (self.solve_backtracking()): # recursive call until the end of the board
                        return True

        self.set_value(row, col, 0)
        return False

    # Solve the puzzle using forward checking
    def solve_forwardchecking(self):
        if (self.ConsistencyChecks > 5000000):
            print ("Consistency checks exceed a reasonable number, terminating program")
            sys.exit(0)

        if self.mvc() == False:
            return True
       
        row = self.mvc()[0]
        col = self.mvc()[1]
        blanks = copy.deepcopy(self.possible_values[row, col])

        for num in blanks:
            temp_blanks = copy.deepcopy(self.possible_values) #backup possible values
            valid = self.validate(row, col, num)
            if (valid):
                self.set_value(row, col, num)

                if (self.solve_forwardchecking()):
                    return True

            self.possible_values = temp_blanks

        self.set_value(row, col, 0)
        return False

    # Print out the puzzle
    def write_grid(self):
        for i in range(0, self.BoardSize):
            for j in range(0, self.BoardSize):
                num = self.get_value(i, j)
                print (num, end = " ")
            print()
        print()
        return

# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements with a value of 0 are considered to be empty
def parse_file(filename):
    print("start parsing file")
    f = open(filename, 'r')
    print("file opened")
    BoardSize = int(f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board = [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        linearr = f.readline().strip().split()
        row = int(linearr[0])
        col = int(linearr[1])
        val = int(linearr[2])
        board[row-1][col-1] = val
    print("after parsing file")
    return board
    
# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board(file_name):
    board = parse_file(file_name)
    print(file_name)
    return SudokuBoard(len(board), board)

# Main method accepts a filename and option as input, and runs the appropriate
# solve method based on the option. Exceptions are thrown for invalid filenames
# and invalid argument counts. The board is also printed before and after it is
# solved, along with the total number of consistency checks
# Use "b" for backtracking and "f" for forward checking
# (ex. `python3.2 Sudoku.py 4x4.sudoku b`)
def main(argv = None):
    runtime = time.clock()
    if argv is None:
        argv = sys.argv

    if (len(argv) != 3):
        print("Wrong number of arguments")
        return

    try:
        sb = init_board(argv[1]) #initialize the board from input
        # Solve the board using backtracking or forward checking
        print()
        print("original board: ")
        sb.write_grid()
        if (argv[2] == "b"):
            sb.solve_backtracking()
            print("solved by back tracking:")
        elif (argv[2] == "f"):
            sb.empty_squares = sb.get_empty_squares()
            sb.check_values()
            sb.solve_forwardchecking()
            print("solved by forward checking: ")
        elif (argv[2] == "s"):
            print("original board")

        sb.write_grid() #display the board results
        #display the total number of consistency checks
        print ("Total number of consistency checks:", sb.ConsistencyChecks)
        runtime = time.clock() - runtime
        #display the total time taken to find a solution
        print ("Solution found in:", runtime, "seconds")
    except IOError as e:
        print("No inputtttttt file!")

    return

if __name__ == '__main__':
    main()
