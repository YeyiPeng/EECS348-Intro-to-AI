#!/usr/bin/env python
import struct, string, math, copy, Queue

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep


def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def is_consistent(sudoku_board, row, col, value):
    """Takes in a sudoku board and tests to see if it meets the constraints."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    for i in range(size):
        if(BoardArray[i][col] == value):
            return False

    for j in range(size):
        if(BoardArray[row][j] == value):
            return False

    SquareRow = row // subsquare
    SquareCol = col // subsquare

    for i in range(subsquare):
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == value)):
                return False
    return True

def back_tracking(initial_board):
    if is_complete(initial_board):
        return True
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if(initial_board.CurrentGameBoard[i][j] == 0):
                for k in range(initial_board.BoardSize):
                    if(is_consistent(initial_board, i, j, k+1)):
                        initial_board.set_value(i, j, k+1)
                        if back_tracking(initial_board):
                            return True
                        initial_board.set_value(i, j, 0)
                return False

def init_domainTable(initial_board):
    """initialize the domain of the unassigned variable in the board"""
    print "in init_domainTable"
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    domainTable = [[[i+1 for i in range(size)] for j in range(size)] for k in range(size)]
    # q = Queue.Priority_Queue()

    for i in range(size):
        for j in range(size):
            if (initial_board.CurrentGameBoard[i][j] == 0):
                for k in range(size):
                    if (not is_consistent(initial_board, i, j, k+1)):
                        domainTable[i][j].remove(k+1)
    return domainTable

def forward_checking(initial_board, domainTable, row, col, value):
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    for i in range(size):
        if (BoardArray[i][col] == 0 and (value in domainTable[i][col]) and i != row):
            if(not is_consistent(initial_board, i, col, value)):
                domainTable[i][col].remove(value)

    for j in range(size):
        if (BoardArray[row][j] == 0 and (value in domainTable[row][j]) and j!= col):
            if(not is_consistent(initial_board, row, j, value)):
                domainTable[row][j].remove(value)

    SquareRow = row // subsquare
    SquareCol = col // subsquare

    for i in range(subsquare):
        for j in range(subsquare):
            if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0 and (value in domainTable[SquareRow*subsquare+i][SquareCol*subsquare+j])):
                if ((not is_consistent(initial_board, SquareRow*subsquare+i, SquareCol*subsquare+j, value))
                    and (SquareRow*subsquare + i != row)
                    and (SquareCol*subsquare + j != col)):
                    domainTable[SquareRow*subsquare+i][SquareCol*subsquare+j].remove(value)
    return domainTable

def conflict_valueNum(initial_board, domainTable, row, col, value):
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    num = 0

    for i in range(size):
        if (BoardArray[i][col] == 0 and (value in domainTable[i][col]) and i != row):
            num = num+1

    for j in range(size):
        if (BoardArray[row][j] == 0 and (value in domainTable[row][j]) and j!= col):
            num = num+1

    SquareRow = row // subsquare
    SquareCol = col // subsquare

    for i in range(subsquare):
        for j in range(subsquare):
            if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0 and (value in domainTable[SquareRow*subsquare+i][SquareCol*subsquare+j])):
                if ((SquareRow*subsquare + i != row)
                    and (SquareCol*subsquare + j != col)):
                    num = num+1
    return num

def conflict_num(initial_board, row, col):
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    num = 0
    for i in range(size):
        if (BoardArray[i][col] == 0 and i != row):
            num = num+1

    for j in range(size):
        if (BoardArray[row][j] == 0 and j != col):
            num = num+1

    SquareRow = row // subsquare
    SquareCol = col // subsquare

    for i in range(subsquare):
        for j in range(subsquare):
            if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0 
                    and (SquareRow*subsquare + i != row)
                    and (SquareCol*subsquare + j != col)):
                    num  = num+1
    return num

def back_trackingFC(initial_board, domainTable, MRV = False, Degree = False, LCV = False):
    if is_complete(initial_board):
        return True
    if MRV:
        minLen = initial_board.BoardSize + 1

        for i in range(initial_board.BoardSize):
           for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    if (len(domainTable[i][j])  < minLen):
                            # print domainTable[i][j]
                        minLen = len(domainTable[i][j])
                        row = i
                        col = j
        if LCV:
            q = Queue.PriorityQueue()
            for k in domainTable[row][col]:
                num = conflict_valueNum(initial_board, domainTable, row, col, k)
                q.put((num, k))
            while not q.empty():
                # print q.get()
                value = q.get()[1]
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, value)
                domainTable = forward_checking(initial_board, domainTable, row, col, value)
                if(back_trackingFC(initial_board, domainTable, MRV, False, LCV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
        else:
                            # print row, col
            for k in domainTable[row][col]:
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, k)
                # initial_board.print_board()
                domainTable = forward_checking(initial_board, domainTable, row, col, k)
                if (back_trackingFC(initial_board, domainTable, MRV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
    elif Degree:
        maxNum = -1

        for i in range(initial_board.BoardSize):
            for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    if (conflict_num(initial_board, i, j) > maxNum):
                        maxNum = conflict_num(initial_board, i, j)
                        row = i
                        col = j
                # print i, j
        # print row, col, maxNum
        if LCV:
            q = Queue.PriorityQueue()
            for k in domainTable[row][col]:
                num = conflict_valueNum(initial_board, domainTable, row, col, k)
                q.put((num, k))
            while not q.empty():
                # print q.get()
                value = q.get()[1]
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, value)
                domainTable = forward_checking(initial_board, domainTable, row, col, value)
                if(back_trackingFC(initial_board, domainTable, False, Degree, LCV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
        else:
            for k in domainTable[row][col]:
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, k)
                # initial_board.print_board()
                domainTable = forward_checking(initial_board, domainTable, row, col, k)
                if (back_trackingFC(initial_board, domainTable, False, Degree)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
        return False
    elif LCV:
        for row in range(initial_board.BoardSize):
            for col in range(initial_board.BoardSize):
                if(initial_board.CurrentGameBoard[row][col] == 0):
                    q = Queue.PriorityQueue()
                    for k in domainTable[row][col]:
                        num = conflict_valueNum(initial_board, domainTable, row, col, k)
                        q.put((num, k))
                    while not q.empty():
                        # print q.get()
                        value = q.get()[1]
                        tmpTable = copy.deepcopy(domainTable)
                        initial_board.set_value(row, col, value)
                        domainTable = forward_checking(initial_board, domainTable, row, col, value)
                        if(back_trackingFC(initial_board, domainTable, False, False, LCV)):
                            return True
                        initial_board.set_value(row, col, 0)
                        domainTable = tmpTable
                    return False

    else:
        for i in range(initial_board.BoardSize):
            for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    for k in domainTable[i][j]:
                        # print i, j, k
                        tmpTable = copy.deepcopy(domainTable)
                        initial_board.set_value(i, j, k)
                        domainTable = forward_checking(initial_board, domainTable, i, j, k)
                        if(back_trackingFC(initial_board, domainTable)):
                            return True
                        initial_board.set_value(i, j, 0)
                        domainTable = tmpTable
                    return False


def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    # print "Your code will solve the initial_board here!"
    # print "Remember to return the final board (the SudokuBoard object)."
    # print "I'm simply returning initial_board for demonstration purposes."

    if forward_checking == False:
        if (back_tracking(initial_board)):
            return initial_board
    else:
        if MRV == True:
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, MRV, False, LCV)):
                return initial_board
        elif Degree == True:
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, False, Degree, LCV)):
                return initial_board
        elif LCV == True:
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, False, False, LCV)):
                return initial_board
        else:
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable)):
                return initial_board
