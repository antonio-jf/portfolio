"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """         
    # Return player according to odd or pair number of moves
    if played(board) == 0:
        return X
    else:
        return X if played(board) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set of possible moves
    moves = set()
    
    # Add to available move set empty cells
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))
    
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Verify that action is valid
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Incorrect value input")
    
    # Define whose turn is it
    plyr = player(board)
    
    # Create copy of board
    board_copy = copy.deepcopy(board)
    # Make move in copy    
    board_copy[action[0]][action[1]] = plyr
    # Return copy
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check all cases
    if check_rows(board):
        return check_rows(board)
    elif check_columns(board):
        return check_columns(board)
    elif check_diagonals(board):
        return check_diagonals(board)
    else:
        # There is no winner
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for winner
    if winner(board):
        return True
    
    # Check for available cells
    if played(board) == 9:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Current player's move
    plyr = player(board)

    # Get set of actions
    actns = actions(board)
    
    # Array of (utility, action) pairs
    results = []

    if plyr is X:
        for action in actns:
            # Get min_value for action
            results.append([min_value(result(board, action)), action])
        # Sort results by utility
        results = sorted(results, key=lambda x: x[0])
        # Return action of last element (the one with the highest utility)
        return results[-1][1]
    else:
        for action in actns:
            # Get max_value for action
            results.append([max_value(result(board, action)), action])
        # Sort results by utility
        results = sorted(results, key=lambda x: x[0])
        # Return action of first element (the one with the least utility)
        return results[0][1]


def max_value(board):
    """
    Return max value
    """
    if terminal(board):
        return utility(board)
        
    # No utility value is lower than 2
    v = -2
    
    # Recursively call fucntions
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
            
    return v
    
    
def min_value(board):
    """
    Return min value
    """
    if terminal(board):
        return utility(board)
        
    # No utility value is higher than 2
    v = 2
    
    # Recursively call fucntions
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
            
    return v


def check_rows(board):
    """
    Check rows to see if there is a winner
    """
    players = [X, O]
    # Amoun of moves in the same row
    count = 0

    # Check board looking for both players moves
    for plyr in players:    
        # Iterate over rows
        for i in range(3):
            # Check to see if all moves in a row are by the same player
            if count == 3:
                return plyr
            # Restart counter
            count = 0
            # Iterate over cells in a row
            for j in range(3):
                # Count player's moves in a row
                if board[i][j] == plyr:
                    count += 1
    
    return None
    

def check_columns(board):
    """
    Check columns to see if there is a winner
    """
    players = [X, O]
    # Amoun of moves in the same column
    count = 0

    # Check board looking for both players moves
    for plyr in players:    
        # Iterate over columns
        for j in range(3):
            # Check to see if all moves in a column are by the same player
            if count == 3:
                return plyr
            # Restart counter
            count = 0
            # Iterate over cells in a column
            for i in range(3):
                # Count player's moves in a column
                if board[i][j] == plyr:
                    count += 1
    
    return None
    

def check_diagonals(board):
    """
    Check diagonals for winner
    """
    players = [X, O]
    # Amount of moves along diagonals
    for plyr in players:
        # If player doesn't have middle cell skip
        if board[1][1] is not plyr:
            continue
        else:
            # Chech both cases
            if board[0][0] == plyr and board[2][2] == plyr:
                return plyr
            elif board[2][0] == plyr and board[0][2] == plyr:
                return plyr
    
    return None
    
    
def played(board):
    """
    Return the amount of cells available in the board
    """
    count = 0
    # Count the moves already taken on the board
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                count += 1
    
    return count
    
