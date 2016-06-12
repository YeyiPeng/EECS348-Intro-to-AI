# Name: Yeyi Peng
# NetID: ypg016

# Problem 1
def binarySearch(L, v):
    """Checks whether a value v is in a sorted list L using binary search, 
    Returns a pair (t, n), t is a Boolean and n is the times of iteration."""
    if len(L) == 0:
        return (False, 0)
    start = 0
    end = len(L) - 1
    itrTimes = 0
    # binary search
    while start + 1 < end:
        if (start + end) % 2 == 0:
            mid = (start + end) / 2
        else:
            mid = (start + end) / 2 + 1
        if v == L[mid]:          
            return (True, itrTimes)
        if v < L[mid]:
            end = mid
        else:
            start = mid
        itrTimes += 1
    # After the loop, start is next to end, so deal with this case
    if L[start] == v:
        return (True, itrTimes)
    if L[end] == v:
        return (True, itrTimes) 
    return (False, itrTimes)

# Problem 2
def mean(L):
    """Returns the average of a list L"""
    # deal with the case that L is an empty list
    if len(L) == 0:
        return 0;
    return float(sum(L)) / float(len(L))

def median(L):
    """Returns the median of a list L"""
    n = len(L)
    # deal with the case that L is an empty list
    if n == 0:
        return 0;
    L.sort()
    if n % 2 == 0:
        # if n is even, the median should be average of the two middle numbers
        return (float(L[n / 2 - 1]) + float(L[n / 2])) / 2
    else:
        # if n is odd, the median is the middle number
        return float(L[(n + 1) / 2 - 1])

# Problem 3
def bfs(tree, elem):
    """Performs a breadth first search on a tree, returns whether 'elem' is in
    'tree' or not."""
    # use the list as a queue, then perform BFS
    myQueue = [tree]
    while len(myQueue) > 0:
        node = myQueue.pop(0)
        if len(node) > 0:
            print node[0]
            if node[0] == elem:
                return True
            myQueue += node[1:]
    return False

def dfs(tree, elem):
    """Performs a depth first search on a tree, returns whether 'elem' is in
    'tree' or not."""
    # use the list as a stack, then perform DFS
    myStack = [tree]
    while len(myStack) > 0:
        node = myStack.pop()
        if len(node) > 0:
            print node[0]
            if node[0] == elem:
                return True
            myStack += node[1:]
    return False

# Problem 4
class TTTBoard:
    """docstring for TTTBoard"""
    def __init__(self):
        """Initialize a 3x3 tic tac toe board""" 
        self.clear()

    def __str__(self):
        """Show the board"""
        return self.board[0] + ' ' + self.board[1] + ' ' + self.board[2] + '\n'\
            + self.board[3] + ' ' + self.board[4] + ' ' + self.board[5] + '\n'\
            + self.board[6] + ' ' + self.board[7] + ' ' + self.board[8] + '\n'

    def makeMove(self, player, pos):
        """Place a move for player in the position 'pos'. Returns True if the 
        move was made and False if not because the spot was full, or outside 
        the boundaries of the board."""
        # rule out cases in which pos is outside the boundaries or that positon
        # is already taken by an X or O 
        if (pos > 8) or (pos < 0) or (self.board[pos] != '*'):
            return False
        else:
            self.board[pos] = player
            return True

    def hasWon(self, player):
        """Returns True if player has won the game, and False if not"""
        # enumerate all 8 possible win situations
        won = [player, player, player]
        if self.board[0 : 3] == won or self.board[3 : 6] == won or\
           self.board[6 : 9] == won:
            return True
        elif self.board[0] == player and self.board[3] == player and\
             self.board[6] == player:
            return True
        elif self.board[1] == player and self.board[4] == player and\
             self.board[7] == player:
            return True
        elif self.board[2] == player and self.board[5] == player and\
             self.board[8] == player:
            return True
        elif self.board[0] == player and self.board[4] == player and\
             self.board[8] == player:
            return True
        elif self.board[2] == player and self.board[4] == player and\
             self.board[6] == player:
            return True
        else:
            return False

    # a helper function to decide whether a board is full, called in gameOver()        
    def isBoardFull(self):
        """Return True if the board is full, False otherwise"""
        for grid in self.board:
            if grid == '*':
                return False
        return True

    def gameOver(self):
        """Return True if someone has won or if the board is full; otherwise 
        return False"""
        # if X wins or Y wins or the board is full, the game is over
        if self.hasWon('X') == True or self.hasWon('Y') == True or\
           self.isBoardFull() == True:
            return True
        else:
            return False

    def clear(self):
        """Clear the board to reset the game"""
        # set all positions to '*'
        self.board = ['*'] * 9
        
