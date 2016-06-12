 def alphaBetaMove( self, board, ply ):
        """ Choose a move with alpha beta pruning """
        # Set up an opposing player to use.
        self.oppPlayer = Player(self.opp, self.type, self.ply)
        # The rest is different from maxValueAB only in that it keeps track
        # of which move produced the max value and returns that move.
        if ply == 0:
          # No ply, so just choose first legal move
            return (self.score(board), board.legalMoves(self)[0])
        if board.gameOver():
            # Game is over, no legal moves
            return (self.score(board), -1)
        alpha = -INFINITY
        beta  =  INFINITY
        score = -INFINITY
        move = -1
        for m in board.legalMoves(self):
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = self.minValueAB(nextBoard, ply-1, alpha, beta)
            if s > score:
                move = m
                score = s
            alpha = max(alpha, score)
        return (score, move)
                
def maxValueAB (self, board, ply, alpha, beta):
    """ Find the minimax value for the next move for this player
        at a given board configuration. """
    if ply == 0 or board.gameOver():
      # No further recursion, so return current board score
        return self.score(board)
    score = -INFINITY
    for m in board.legalMoves(self):
        # Copy the board so that we don't ruin it
        nextBoard = deepcopy(board)
        nextBoard.makeMove(self, m)
        score = max(score, self.minValueAB(nextBoard, ply-1, alpha, beta))
        if (score >= beta):
          return score
        alpha = max(alpha, score)
    return score
    
def minValueAB (self, board, ply, alpha, beta):
    """ Find the minimax value for the next move for the opposing player
        at a given board configuration. """
    if ply == 0 or board.gameOver():
      # No further recursion, so return current board score
        return self.score(board)
    score = INFINITY
    for m in board.legalMoves(self.oppPlayer):
        # Copy the board so that we don't ruin it
        nextBoard = deepcopy(board)
        nextBoard.makeMove(self.oppPlayer, m)
        score = min(score, self.maxValueAB(nextBoard, ply-1, alpha, beta))
        if (score <= alpha):
          return score
        beta = min(beta, score)
    return score
