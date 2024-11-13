"""
Tic Tac Toe Player
"""

import math

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

    counter_x = 0
    counter_o = 0

    for i in range(3):
        for j in range(3):

            if board[i][j] == "X":
                counter_x += 1
            if board[i][j] == "O":    
                counter_o += 1

    if counter_x <= counter_o:
        return X  
    else:
        return O    
 


def actions(board):

    actions_set = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i,j))

    return actions_set            
    


def result(board, action):

    row, col = action

    if (row or col) not in [0,1,2]:

        raise Exception
    if board[row][col] != EMPTY:
        raise Exception
    
    player_turn = player(board)

    board_copy = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    
    for i in range(3):
        for j in range(3):
            board_copy[i][j] = board[i][j]


    board_copy[row][col] = player_turn

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
