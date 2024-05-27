
import tkinter as tk
from tkinter import messagebox
import math

dx = [0, 0, -1, 1, 1, 1, -1, -1]
dy = [1, -1, 0, 0, -1, 1, 1, -1]
HUMAN = 'B'
AI = 'W'
class DifficultySelector:
    def __init__(self):
        self.maximumDepth = None

        self.window = tk.Tk()
        self.window.title("Select Difficulty")
        self.window.geometry("400x400")  # Set window size to 400x400
        self.window.configure(bg="medium sea green")  # Set background color

        self.selected_difficulty = tk.IntVar()
        self.selected_difficulty.set(1)  # Default value for the selected difficulty

        button_width = 20
        button_height = 2

        easy_radio = tk.Radiobutton(self.window, text="Easy", variable=self.selected_difficulty, value=1, width=button_width, height=button_height, bg="medium sea green")
        easy_radio.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        medium_radio = tk.Radiobutton(self.window, text="Medium", variable=self.selected_difficulty, value=3, width=button_width, height=button_height, bg="medium sea green")
        medium_radio.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        hard_radio = tk.Radiobutton(self.window, text="Hard", variable=self.selected_difficulty, value=5, width=button_width, height=button_height, bg="medium sea green")
        hard_radio.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        start_button = tk.Button(self.window, text="Start Playing", command=self.start_playing, width=button_width, height=button_height, bg="white")
        start_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def start_playing(self):
        self.maximumDepth = self.selected_difficulty.get()
        self.window.destroy()

    def run(self):
        self.window.mainloop()


class OthelloGUI:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.buttons = []
        self.board_size = 8
        self.player_score = 0
        self.ai_score = 0
        self.window = tk.Tk()
        self.window.title('Othello')
        self.board = []

        self.player_score_label = tk.Label(self.window, text="Player Score: 2", font=('Courier New', 16))
        self.ai_score_label = tk.Label(self.window, text="AI Score: 2", font=('Courier New', 16))

        self.invalid_move_displayed = False

        self.init_game()

    def init_game(self):
        self.buttons = []
        self.board = [['-' for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        for row in range(self.board_size):
            row_buttons = []
            for col in range(self.board_size):
                button = tk.Button(self.window, text=' ', font=('Arial', 24), width=3, height=1,
                                   command=lambda r=row, c=col: self.play_turn(r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(bg="mediumseagreen")
                self.buttons[row][col].grid(row=row, column=col)

        self.buttons[3][3].config(bg="white")
        self.buttons[4][4].config(bg="white")
        self.buttons[3][4].config(bg="black")
        self.buttons[4][3].config(bg="black")

        self.board[3][3] = 'W'
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'

        self.player_score_label.grid(row=self.board_size, column=0, columnspan=self.board_size // 2, sticky=tk.W)
        self.ai_score_label.grid(row=self.board_size, column=self.board_size // 2, columnspan=self.board_size // 2,
                                 sticky=tk.E)

    def play_turn(self, x, y):
        # check for valid moves

        # human turn
        human_can_play = self.has_valid_cells(HUMAN)
        if human_can_play:
            self.get_human_move(x, y)
        else:
            messagebox.showerror("No Valid Moves", "Black has no valid moves, switching turns")

        # ai turn
        ai_can_play = self.has_valid_cells(AI)
        if ai_can_play:
            print(f"AI Playing with Max Depth = {self.max_depth}")
            self.board = self.get_ai_move(self.max_depth)
        else:
            messagebox.showerror("No Valid Moves", "White has no valid moves, switching turns")

        # if human can't play and ai can
        ai_can_play = self.has_valid_cells(AI)
        human_can_play = self.has_valid_cells(HUMAN)
        while ai_can_play and not human_can_play:
            messagebox.showerror("No Valid Moves", "Black has no valid moves, switching turns")

            ai_can_play = self.has_valid_cells(AI)
            human_can_play = self.has_valid_cells(HUMAN)

            print(f"AI Playing with Max Depth = {self.max_depth}")
            self.board = self.get_ai_move(self.max_depth)

        self.update_state()
        self.print_board()

        if self.is_full() or (not ai_can_play and not human_can_play):
            self.check_win()
            return

    def update_state(self):
        # updating the board if the board
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != '-':
                    cell = "black" if self.board[x][y] == 'B' else "white"
                    self.buttons[x][y].config(bg=cell)
                else:
                    self.buttons[x][y].config(bg="mediumseagreen")

        black, white = self.calculate_board_score()
        self.update_player_score(black)
        self.update_ai_score(white)

    def update_scores(self):
        # Update the text of the player score label
        self.player_score_label.config(text=f"Player Score: {self.player_score}")

        # Update the text of the AI score label
        self.ai_score_label.config(text=f"AI Score: {self.ai_score}")

    # Method to update the player score
    def update_player_score(self, score):
        self.player_score = score
        self.update_scores()

    # Method to update the AI score
    def update_ai_score(self, score):
        self.ai_score = score
        self.update_scores()

    def is_valid_cell(self, x, y):
        return not (x < 0 or x >= self.board_size or y < 0 or y >= self.board_size)

    def is_valid_move(self, x, y, player, board=None):
        if board is None:
            board = self.board

        if board[x][y] != '-':
            return False

        if not self.is_valid_cell(x, y):
            return False

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if self.is_valid_cell(nx, ny) and board[nx][ny] != player and board[nx][ny] != '-':
                old = [row[:] for row in board]
                old[x][y] = player
                new_board = self.make_move(x, y, board, player)
                if old != new_board:
                    return True
                else:
                    return False

        return False

    def make_move(self, x, y, board, player):
        new_board = [row[:] for row in board]  # Make a deep copy of the board

        # Check if the move is valid
        if not self.is_valid_cell(x, y) or new_board[x][y] != '-':
            # If the move is invalid, return the original board
            return board

        new_board[x][y] = player

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            # find first cell in direction not equal player
            while self.is_valid_cell(nx, ny) and new_board[nx][ny] != player and new_board[nx][ny] != '-':
                nx += dx[k]
                ny += dy[k]

            # if this cell is mine
            # fill all between
            if self.is_valid_cell(nx, ny) and new_board[nx][ny] == player:
                nx = x + dx[k]
                ny = y + dy[k]
                while self.is_valid_cell(nx, ny) and new_board[nx][ny] != player and new_board[nx][ny] != '-':
                    new_board[nx][ny] = player
                    nx += dx[k]
                    ny += dy[k]

        return list(new_board)

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print("")


        #-------

    def get_human_move(self, x, y):
        self.window.var = tk.IntVar()
        while True:
            self.invalid_move_displayed = False
            if self.is_valid_move(x, y, HUMAN):
                self.board = self.make_move(x, y, self.board, HUMAN)
                self.invalid_move_displayed = False  # Reset the flag
                break

            if not self.invalid_move_displayed:
                messagebox.showerror("Invalid Move", "Invalid cell. Try again.")
                self.invalid_move_displayed = True  # Set the flag

            # Wait for the user to click another button
            self.window.wait_variable(self.window.var)

        # Reset the wait_variable
        self.window.var = tk.IntVar()

        # update board
        return True

    def get_ai_move(self, max_depth):
        x, y = (-1, -1)
        best = math.inf
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, AI):
                    old = [row[:] for row in self.board]  # Make a deep copy of the board
                    new_board = self.make_move(i, j, old, AI)
                    score = self.alpha_beta(1, new_board, -math.inf, math.inf, HUMAN, max_depth)
                    if score <= best:
                        best = score
                        x, y = i, j
        if x != -1 or y != -1:
            self.board = self.make_move(x, y, self.board, AI)
            self.update_state()
        return self.board

    def alpha_beta(self, depth, board, alpha, beta, player, max_depth) -> int:
        if depth >= max_depth:
            # base case
            b, w = self.calculate_board_score()
            if b > w:
                return b
            else:
                return -w
        score = math.inf if player == 'W' else -math.inf
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, player, board):
                    old = []
                    for _ in board:
                        old.append(list(_))

                    board = self.make_move(i, j, board, player)
                    # b, w = calculateBoardScore(board)
                    if player == 'W':
                        score = min(score,
                                    self.alpha_beta(depth + 1, board, alpha, beta, 'B', max_depth))
                        beta = min(beta, score)
                    else:
                        score = max(score,
                                    self.alpha_beta(depth + 1, board, alpha, beta, 'W', max_depth))
                        alpha = max(alpha, score)
                    board = old
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return score

    def has_valid_cells(self, player):
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, player):
                    return True  # There's at least one valid move for human
        return False  # No valid moves found

    def is_full(self):
        return all(all(cell != '-' for cell in row) for row in self.board)

    def calculate_board_score(self):
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                black += self.board[i][j] == 'B'
                white += self.board[i][j] == 'W'

        return black, white

    def check_win(self):
        black, white = self.calculate_board_score()
        if not self.is_draw(black - white):
            if black > white:
                self.display_winner("Black")
            else:
                self.display_winner("White")

        return False

    def display_winner(self, player):
        messagebox.showinfo(
            "Othello", f"{str(player)} wins!")

    def is_draw(self, diff):
        if diff == 0:
            messagebox.showinfo(
                "Othello", "It's a tie!")
            return True
        else:
            return False

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    selector = DifficultySelector()
    selector.run()

    othello = OthelloGUI(selector.maximumDepth)
    othello.run()
