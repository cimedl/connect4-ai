import numpy as np

MAX_ROWS = 6
MAX_COLUMNS = 7
MAX_DEPTH = 4

# drops piece on board 
def drop_piece(board, column, player):
    for row in range(MAX_ROWS):
        if board[row][column] == 0:
            board[row][column] = player
            return

# returns a single array of all valid columns indices
def get_valid_locations(board):
    valid_columns = []
    for c in range(MAX_COLUMNS):
        if board[MAX_ROWS - 1][c] == 0:
            valid_columns.append(c)
    return valid_columns

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

# checks if no more valid locations or a player won
def is_terminal_node(board):
    return (
        winning_move(board, 1) or winning_move(board, 2) or
        len(get_valid_locations(board)) == 0
    )

# sliding window to check scores depending on given window
def score_window(window, player):
    opponent = 2 if player == 1 else 1
    
    player_count = 0
    opponent_count = 0
    empty_count = 0

    for piece in window:
        if piece == player:
            player_count += 1
        elif piece == opponent:
            opponent_count += 1
        else:
            empty_count += 1


    score = 0
    if player_count == 4:
        score += 100000
    elif player_count == 3 and empty_count == 1:
        score += 100
    elif player_count == 2 and empty_count == 2:
        score += 10

    if opponent_count == 3 and empty_count == 1:
        score -= 100
    if opponent_count == 4:
        score -= 100000

    return score

def evaluate_board(board, player):
    score = 0

    # Center column preference (expanded loop)
    center_column_index = MAX_COLUMNS // 2
    center_count = 0
    for r in range(MAX_ROWS):
        if board[r][center_column_index] == player:
            center_count += 1
    score += center_count * 6

    # checking score horizontally
    for r in range(MAX_ROWS):
        for c in range(MAX_COLUMNS - 3):
            window = []
            for i in range(4):
                window.append(board[r][c + i])
            score += score_window(window, player)

    # checking score vertically
    for c in range(MAX_COLUMNS):
        for r in range(MAX_ROWS - 3):
            window = []
            for i in range(4):
                window.append(board[r + i][c])
            score += score_window(window, player)

    # checking score diagonally
    for r in range(MAX_ROWS - 3):
        for c in range(MAX_COLUMNS - 3):
            window = []
            for i in range(4):
                window.append(board[r + i][c + i])
            score += score_window(window, player)

    # checking score on negative diagonally
    for r in range(3, MAX_ROWS):
        for c in range(MAX_COLUMNS - 3):
            window = []
            for i in range(4):
                window.append(board[r - i][c + i])
            score += score_window(window, player)

    return score

# minimax implementation
def minimax(board, player, depth, alpha, beta, maximizing_player, root_player=1):
    if depth == 0 or is_terminal_node(board):
        if winning_move(board, root_player):
            return 100000000
        elif winning_move(board, 2 if root_player == 1 else 1):
            return -100000000
        else:
            return evaluate_board(board, root_player)

    valid_locations = get_valid_locations(board)

    if maximizing_player:
        score = -np.inf
        for column in valid_locations:

            new_board = np.copy(board)
            drop_piece(new_board, column, player)

            child_player = 2 if player == 1 else 1
            score = max(score, minimax(new_board, child_player, depth - 1, alpha, beta, False, root_player))

            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
    elif not maximizing_player:
        score = np.inf

        for column in valid_locations:
            new_board = np.copy(board)

            drop_piece(new_board, column, player)
            child_player = 1 if player == 2 else 2

            score = min(score, minimax(new_board, child_player, depth - 1, alpha, beta, True, root_player))

            beta = min(beta, score)
            if alpha >= beta:
                break
        return score

# pseudo main function 
def aiplayer1(board):
    root_player = 1
    player = 1

    best_score = -np.inf
    best_col = 0

    valid_locations = get_valid_locations(board)
    for col in valid_locations:

        new_board = np.copy(board)
        drop_piece(new_board, col, player)

        score = minimax(new_board, 2 if player == 1 else 1, MAX_DEPTH, -np.inf, np.inf, False, root_player)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col