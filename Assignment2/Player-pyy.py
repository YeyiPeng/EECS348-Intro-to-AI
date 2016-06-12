# File: Player.py
# Author(s) names AND netid's:
# Date:
# Group work statement: <please type the group work statement
#      given in the pdf here>
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
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        score = -INFINITY
        move = -1
        alpha = -INFINITY
        beta = INFINITY
        turn = self
        
        for m in board.legalMoves(self):
            if ply == 0:
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)
            opponent = Player(self.opp, self.type, self.ply)
            nb = deepcopy(board)
            nb.makeMove(self, m)
            s = opponent.minValueAB(nb, ply - 1, turn, alpha, beta)
            if s > score:
                move = m
                score = s
        return (score, move)
        

    def maxValueAB(self, board, ply, turn, alpha, beta):
        # if board.gameOver() or ply == 0:
        #     return self.score(board)
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY    

        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            nb = deepcopy(board)
            nb.makeMove(self, m)
            opponent = Player(self.opp, self.type, self.ply)
            score = max(score, opponent.minValueAB(nb, ply - 1, turn, alpha, beta))
            if (score >= beta):
                return score
            alpha = max(alpha, score)
        return score

    def minValueAB(self, board, ply, turn, alpha, beta):
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            nb = deepcopy(board)
            nb.makeMove(self, m)
            opponent = Player(self.opp, self.type, self.ply)
            score = min(score, opponent.maxValueAB(nb, ply - 1, turn, alpha, beta))
            if (score <= alpha):
                return score
            beta = min(beta, score)
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
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class ysj784(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
    def __init__(self, playerNum, playerType, ply=0):
        Player.__init__(self, playerNum, playerType, ply)

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # if board.hasWon(self.num):
        #     return 100.0
        # elif board.hasWon(self.opp):
        #     return 0.0
        # else: 
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

        
