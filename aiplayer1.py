import numpy as np

MAX_ROWS = 6
MAX_COLUMNS = 7
MAX_DEPTH = 4

# returns a single row of all valid columns
def get_valid_locations(board):
    valid_columns = []

    for column in range(MAX_COLUMNS):
        if board[MAX_ROWS - 1][column] == 0:
            valid_columns.append(column)

    return valid_columns

# checks if no more valid locations or a player won
def is_terminal_node(board):
    if (len(get_valid_locations(board)) == 0 or winning_move(board, 1) or winning_move(board, 2)):
        return True
    return False

# drops piece on board 
def drop_piece(board, column, player):
    for row in range(MAX_ROWS):
        if board[row][column] == 0:
            board[row][column] = player
            return

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(MAX_COLUMNS-3):
        for r in range(MAX_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check vertical locations for win
    for c in range(MAX_COLUMNS):
        for r in range(MAX_ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(MAX_COLUMNS-3):
        for r in range(MAX_ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(MAX_COLUMNS-3):
        for r in range(3, MAX_ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True 

# sliding window to check scores depending on given window
def window_score(window, player):
    opponent = 2 if player == 1 else 1

    opponent_score = 0
    player_score = 0
    zero_score = 0

    for column in window:
        if column == player:
            player_score += 1
        elif column == opponent:
            opponent_score += 1
        else:
            zero_score += 1

    total_score = 0

    if player_score == 4:
        total_score += 10000
    elif player_score == 3 and zero_score == 1:
        total_score += 100
    elif player_score == 2 and zero_score == 2:
        total_score += 10

    if opponent_score == 4:
        total_score += -10000
    elif opponent_score == 3 and zero_score == 1:
        total_score += -100

    return total_score

# evaluation function to check for horizontal, vertical and diagonal scores
def evaluate_board(board, player):
    score = 0

    # checking score horizontally
    for row in range(MAX_ROWS):
        for column in range(MAX_COLUMNS - 3):
            window = []

            for index in range(4):
                window.append(board[row][column + index])
            
            score += window_score(window, player)

    # checking score vertically
    for column in range(MAX_COLUMNS):
        for row in range(MAX_ROWS - 3):
            window = []

            for index in range(4):
                window.append(board[row + index][column])
            
            score += window_score(window, player)

    # checking score diagonally
    for row in range(MAX_ROWS - 3):
        for column in range(MAX_COLUMNS - 3):
            window = []

            for index in range(4):
                window.append(board[row + index][column + index])

            score += window_score(window, player)

    return score

# minimax implementation
def minimax(board, player, depth, maximizing_player, root_player):
    if depth == 0 or is_terminal_node(board):
        if winning_move(board, root_player):
            return 1000000
        elif winning_move(board, 2 if player == 1 else 1):
            return -1000000
        else:
            return evaluate_board(board, root_player)

    if maximizing_player:
        score = -np.inf

        for column in get_valid_locations(board):
            new_board = np.copy(board)

            drop_piece(new_board, column, player)

            next_player = 2 if player == 1 else 1

            score = max(score, minimax(new_board, next_player, depth - 1, False, root_player))

        return score

    elif not maximizing_player:
        score = np.inf

        for column in get_valid_locations(board):
            new_board = np.copy(board)

            drop_piece(new_board, column, player)
            next_player = 1 if player == 2 else 2

            score = min(score, minimax(new_board, next_player, depth - 1, True, root_player))

        return score

# pseudo main function 
def aiplayer1(board):
    root_player = 1
    player = 2

    best_score = -np.inf
    best_column = 0

    for column in get_valid_locations(board):
        new_board = np.copy(board)

        drop_piece(new_board, column, player)
        score = minimax(board, player, MAX_DEPTH, False, root_player)

        if score >= best_score:
            best_score = score
            best_column = column

    return best_column