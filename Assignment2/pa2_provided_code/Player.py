# File: Player.py
# Author(s) names AND netid's:
# Yuanqi Shen(ysj784), Yeyi Peng(ypg016), Yamin Li(ylf245)
# Date:04/17/2016
# Group work statement: All group members were present and
# contributing during all work on this project.
#
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.

    def alphaBetaMove(self, board, ply):
        """ Choose the best alphaBeta move.  Returns score, move """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.ABminValue(nb, ply-1, turn, score) # call the ABminValue to find ABmin balue from next level
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def ABmaxValue(self, board, ply, turn, beta):
        """ Find the ABMax value for the next move for this player
        at a given board configuation, and decide to prune or not. Returns score."""
        if board.gameOver():  # game over, return the score
            return turn.score(board)
        score = -INFINITY  # find ABmax value, so initially score is -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.ABminValue(nextBoard, ply-1, turn, score) # check what is the ABminValue from the next level
            if s >= beta: # ABminValue is greater than the upperbound, so prune
                return s
            if s > score: # get the current ABmaxValue
                score = s
        return score

    def ABminValue(self, board, ply, turn, alpha):
        """ Find the ABmin value for the next move for this player
            at a given board configuation, and decide to prune or not. Returns score."""
        if board.gameOver():  # game over, return the score
            return turn.score(board)
        score = INFINITY  # find ABmin value, so initially score is INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.ABmaxValue(nextBoard, ply-1, turn, score)  # check what is the ABmaxValue from the next level
            if s <= alpha:  # ABmaxValue is less than the lowerbound, so prune
                return s
            elif s < score: # get the current ABminValue
                score = s
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            self.ply = 9
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class ysj784(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board

        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            # get my score, opponent score, my cups and opponent cups
            if self.num == 1:
                MyScore = board.scoreCups[0]
                OppScore = board.scoreCups[1]
                MyCups = board.P1Cups
                OppCups = board.P2Cups
            else:
                MyScore = board.scoreCups[1]
                OppScore = board.scoreCups[0]
                MyCups = board.P2Cups
                OppCups = board.P1Cups

            NetScore = MyScore - OppScore # the net value of more stones I have in my Mancalas than my opponent's Mancalas
            WeightNetScore = 2 # weight for NetScore

            NetStones = 0 # the net value of more stones I have on my side than my oppoent on his or her side
            WeightNetStones = 1.5 # weight for NetStones

            LargeGain = 0 # consider the large gain situation: last stone is in an empty cup and gain my last stone and all
                          # corresponding component's stones
            WeightLargeGain = 1 # weight for LargeGain

            for c in range(board.NCUPS):
                NetStones += MyCups[c] - OppCups[c]
                # consider large gains
                if(MyCups[c] == 0):
                  LargeGain += OppCups[board.NCUPS - c - 1] # the order of cups is opposite for my opponent and myself
                if(OppCups[c] == 0):
                  LargeGain -= MyCups[board.NCUPS - c - 1]  # the order of cups is opposite for my opponent and myself

            # calculate the overall score
            OverallScore = NetScore * WeightNetScore + NetStones * WeightNetStones + LargeGain * WeightLargeGain

            return (50 + OverallScore)
