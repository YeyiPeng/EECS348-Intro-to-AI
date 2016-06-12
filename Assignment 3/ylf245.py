### Author(s) names AND netid's:
### Yamin Li, ylf245; Yuanqi Shen, ysj784; Yeyi Peng, ypg016
### Group work statement:
### All group members were present and contributing during all work on this project

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
    """Takes in a sudoku board and tests to see if setting value in (row, col) meets the constraints."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #whether there is the same value in the same col
    for i in range(size):
        if(BoardArray[i][col] == value):
            return False

    #whether there is the same value in the same row
    for j in range(size):
        if(BoardArray[row][j] == value):
            return False

    SquareRow = row // subsquare
    SquareCol = col // subsquare

    #whether there is the same value in the same square
    for i in range(subsquare):
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == value)):
                return False
    return True

#global number of consistency it makes, global upper bound for the number of checks
numOfChecks = 0
numofChecksLimit = 4000000
reachUpperBound = False

def back_tracking(initial_board):
    """plain backtracking algorithm to recursivly solve the Sudoku"""
    #return when the board is complete
    if is_complete(initial_board):
        return True

    global numOfChecks
    global numofChecksLimit
    global reachUpperBound

    #return when the number of checks made reach the upper bound
    if numOfChecks > numofChecksLimit:
        reachUpperBound = True
        return True

    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            #choose a unassigned value
            if(initial_board.CurrentGameBoard[i][j] == 0):
                #test each possible value in this position(i, j)
                for k in range(initial_board.BoardSize):
                    #check whether the value made is consistent
                    if(is_consistent(initial_board, i, j, k+1)):
                        #increase number of checks have made
                        numOfChecks = numOfChecks + 1
                        initial_board.set_value(i, j, k+1)
                        if back_tracking(initial_board):
                            return True
                        initial_board.set_value(i, j, 0)
                return False

def init_domainTable(initial_board):
    """initialize the domain of the unassigned variable in the board"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    #initialize the domain table all the possible values for each position
    domainTable = [[[i+1 for i in range(size)] for j in range(size)] for k in range(size)]

    for i in range(size):
        for j in range(size):
            if (initial_board.CurrentGameBoard[i][j] == 0):
                #remove the inconsistent values from (i,j)'s domain table
                for k in range(size):
                    if (not is_consistent(initial_board, i, j, k+1)):
                        domainTable[i][j].remove(k+1)
    return domainTable

def forward_checking(initial_board, domainTable, row, col, value):
    """Forward check the domain table after set value in (row, col)"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #forward check the domain table for the position of the same col
    for i in range(size):
        if (BoardArray[i][col] == 0 and (value in domainTable[i][col]) and i != row):
            if(not is_consistent(initial_board, i, col, value)):
                domainTable[i][col].remove(value)

    #forward check the domain table for the position of the same row
    for j in range(size):
        if (BoardArray[row][j] == 0 and (value in domainTable[row][j]) and j!= col):
            if(not is_consistent(initial_board, row, j, value)):
                domainTable[row][j].remove(value)

    #forward check the domain table for the position of the same square
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
    """count the number that setting value at (row, col) rules out for other unassigned variable"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    num = 0

    #count the ruling out number in the same col
    for i in range(size):
        if (BoardArray[i][col] == 0 and (value in domainTable[i][col]) and i != row):
            num = num+1

    #count the ruling out number in the same row
    for j in range(size):
        if (BoardArray[row][j] == 0 and (value in domainTable[row][j]) and j!= col):
            num = num+1

    #count the ruling out number in the same square
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
    """count the number of constrians (row, col) has involved in other's unassigned variables"""
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #number of constrains involved in the same col
    num = 0
    for i in range(size):
        if (BoardArray[i][col] == 0 and i != row):
            num = num+1

    #number of constrains involved in the same row
    for j in range(size):
        if (BoardArray[row][j] == 0 and j != col):
            num = num+1

    #number of constrains involved in the same square
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
    """choose a Heuristic and do the backtracking + forward checking"""

    global numOfChecks
    global numofChecksLimit
    global reachUpperBound

    #return if the board is complet
    if is_complete(initial_board):
        return True
    #MRV Heuristic
    if MRV:
        if numOfChecks > 267000:
            reachUpperBound = True
            return True
        #initialize the minimum number for the Minimum Remaining Variable
        minLen = initial_board.BoardSize + 1

        #find the MRV
        for i in range(initial_board.BoardSize):
           for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    #update the MRV's position
                    if (len(domainTable[i][j])  < minLen):
                        minLen = len(domainTable[i][j])
                        row = i
                        col = j
        if LCV:
            #MRV+LCV
            #using a priority to order the LCV
            q = Queue.PriorityQueue()
            #re-order to meet LCV's requirement
            for k in domainTable[row][col]:
                num = conflict_valueNum(initial_board, domainTable, row, col, k)
                q.put((num, k))
            #LCV Heuristic
            while not q.empty():
                numOfChecks = numOfChecks + 1
                value = q.get()[1]
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, value)
                domainTable = forward_checking(initial_board, domainTable, row, col, value)
                if(back_trackingFC(initial_board, domainTable, MRV, False, LCV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
        #plain MRV
        else:
            #recursivly checks each value in the MRV's variable's domain table
            for k in domainTable[row][col]:
                numOfChecks = numOfChecks + 1
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, k)
                domainTable = forward_checking(initial_board, domainTable, row, col, k)
                if (back_trackingFC(initial_board, domainTable, MRV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
    #Degree Heuristic
    elif Degree:
        #initialize the value for the maximum number of variable that involed in the other's unassigned one
        maxNum = -1

        if numOfChecks > 400000:
            reachUpperBound = True
            return True

        #find the maximum number for Degree Heristic
        for i in range(initial_board.BoardSize):
            for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    if (conflict_num(initial_board, i, j) > maxNum):
                        maxNum = conflict_num(initial_board, i, j)
                        row = i
                        col = j
        #Degree+LCV Heristic
        if LCV:
            q = Queue.PriorityQueue()
            #re-order to choose the LCV for the Degree Heuristic
            for k in domainTable[row][col]:
                num = conflict_valueNum(initial_board, domainTable, row, col, k)
                q.put((num, k))
            while not q.empty():
                numOfChecks = numOfChecks + 1
                value = q.get()[1]
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, value)
                domainTable = forward_checking(initial_board, domainTable, row, col, value)
                if(back_trackingFC(initial_board, domainTable, False, Degree, LCV)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
            return False
        #plain Degree
        else:
            #recursivly check each value in the Degree's variable's domain table
            for k in domainTable[row][col]:
                numOfChecks = numOfChecks + 1
                tmpTable = copy.deepcopy(domainTable)
                initial_board.set_value(row, col, k)
                domainTable = forward_checking(initial_board, domainTable, row, col, k)
                if (back_trackingFC(initial_board, domainTable, False, Degree)):
                    return True
                initial_board.set_value(row, col, 0)
                domainTable = tmpTable
        return False
    #LCV Heuristic
    elif LCV:
        if numOfChecks > 267000:
            reachUpperBound = True
            return True

        for row in range(initial_board.BoardSize):
            for col in range(initial_board.BoardSize):
                if(initial_board.CurrentGameBoard[row][col] == 0):

                    q = Queue.PriorityQueue()
                    #re-order for LCV for each (row, col)
                    for k in domainTable[row][col]:
                        num = conflict_valueNum(initial_board, domainTable, row, col, k)
                        q.put((num, k))
                    #recursivly check each value in the order of LCV
                    while not q.empty():
                        numOfChecks = numOfChecks + 1
                        value = q.get()[1]
                        tmpTable = copy.deepcopy(domainTable)
                        initial_board.set_value(row, col, value)
                        domainTable = forward_checking(initial_board, domainTable, row, col, value)
                        if(back_trackingFC(initial_board, domainTable, False, False, LCV)):
                            return True
                        initial_board.set_value(row, col, 0)
                        domainTable = tmpTable
                    return False
    #backtracking and forward checing without any heuristics
    else:
        if numOfChecks > 300000:
            reachUpperBound = True
            return True
        for i in range(initial_board.BoardSize):
            for j in range(initial_board.BoardSize):
                if (initial_board.CurrentGameBoard[i][j] == 0):
                    for k in domainTable[i][j]:
                        numOfChecks = numOfChecks + 1
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

    global numOfChecks
    #do the plain backtrackinng
    if forward_checking == False:
        numOfChecks = 0
        if (back_tracking(initial_board)):
            return initial_board

    else:
        #MRV Heuristic(may with LCV)
        if MRV == True:
            numOfChecks = 0
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, MRV, False, LCV)):
                return initial_board
        #Degree Heuristic(may with LCV)
        elif Degree == True:
            numOfChecks = 0
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, False, Degree, LCV)):
                return initial_board
        #plain LCV Heuristic
        elif LCV == True:
            numOfChecks = 0
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable, False, False, LCV)):
                return initial_board
        #backtracking + forward checking
        else:
            domainTable = init_domainTable(initial_board)
            if (back_trackingFC(initial_board, domainTable)):
                return initial_board

