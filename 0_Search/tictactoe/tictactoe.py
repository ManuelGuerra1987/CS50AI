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

    if board[0][0] == board[0][1] == board[0][2]:
        if board[0][0] == "X":
            return "X"
        elif board[0][0] == "O":
            return "O"

    if board[1][0] == board[1][1] == board[1][2]:
        if board[1][0] == "X":
            return "X"
        elif board[1][0] == "O":
            return "O"    

    if board[2][0] == board[2][1] == board[2][2]:
        if board[2][0] == "X":
            return "X"
        elif board[2][0] == "O":
            return "O"  
        
    if board[0][0] == board[1][0] == board[2][0]:
        if board[0][0] == "X":
            return "X"
        elif board[0][0] == "O":
            return "O"    

    if board[0][1] == board[1][1] == board[2][1]:
        if board[0][1] == "X":
            return "X"
        elif board[0][1] == "O":
            return "O"  

    if board[0][2] == board[1][2] == board[2][2]:
        if board[0][2] == "X":
            return "X"
        elif board[0][2] == "O":
            return "O"  

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == "X":
            return "X"
        elif board[0][0] == "O":
            return "O"   

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == "X":
            return "X"
        elif board[0][2] == "O":
            return "O"                                         
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    result = winner(board)

    if result == "X" or result == "O":
        return True
    
    empty_counter = 0

    for i in range(3):
        for j in range(3):    
            if board[i][j] == EMPTY:
                empty_counter += 1

    if empty_counter == 0:
        return True

    return False            




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    result = winner(board)

    if result == "X":
        return 1
    elif result == "O":
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
