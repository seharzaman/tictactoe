import tkinter as tk
from tkinter import messagebox
import copy

# Constants for the game board size
BOARD_SIZE = 3
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

# Create the main window
root = tk.Tk()
root.title('Tic Tac Toe')

# Game state representation
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = PLAYER_X

# Check if the board is full
def is_board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

# Check if a player has won
def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)):
        return True

    return False

# Evaluate the current board state
def evaluate_board(board):
    if check_winner(board, PLAYER_X):
        return 1
    elif check_winner(board, PLAYER_O):
        return -1
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if check_winner(board, PLAYER_X):
        return 1
    elif check_winner(board, PLAYER_O):
        return -1
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = PLAYER_X
                    eval = minimax(new_board, depth + 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = PLAYER_O
                    eval = minimax(new_board, depth + 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# AI makes a move
def ai_move():
    best_move = None
    best_eval = float('-inf')

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                new_board = copy.deepcopy(board)
                new_board[i][j] = PLAYER_X
                move_eval = minimax(new_board, 0, float('-inf'), float('inf'), False)

                if move_eval > best_eval:
                    best_eval = move_eval
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = PLAYER_X
        buttons[best_move[0]][best_move[1]].config(text=PLAYER_X)
        if check_winner(board, PLAYER_X):
            messagebox.showinfo("Game Over", "AI (X) wins!")
            root.quit()
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            root.quit()

# Handle button click events
def on_button_click(row, col):
    if board[row][col] == EMPTY:
        buttons[row][col].config(text=PLAYER_O)
        board[row][col] = PLAYER_O

        if check_winner(board, PLAYER_O):
            messagebox.showinfo("Game Over", "Human (O) wins!")
            root.quit()
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            root.quit()

        ai_move()

# Create buttons for the game board
buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        buttons[i][j] = tk.Button(root, text=EMPTY, font=('normal', 20), width=6, height=2,
                                  command=lambda row=i, col=j: on_button_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Start the game
root.mainloop()
