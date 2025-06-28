import tkinter as tk
from tkinter import simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - InternPe Project")
        self.root.configure(bg="#222222")

        self.game_mode = tk.StringVar(value="Two Players")
        self.difficulty = "Easy"
        self.player_names = {"X": "X", "O": "O"}
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.score = {"X": 0, "O": 0}
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.timer_seconds = 10
        self.remaining_time = 10
        self.timer_id = None
        self.started = False

        self.create_ui()

    def create_ui(self):
        menu = tk.OptionMenu(self.root, self.game_mode, "Two Players", "Single Player", command=self.on_mode_change)
        menu.config(font=("Helvetica", 12), bg="#dddddd")
        menu.grid(row=0, column=1, pady=(10, 0))

        self.x_frame = tk.Frame(self.root, bg="#222222")
        self.x_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        tk.Label(self.x_frame, text="👤", bg="#222222", fg="white").pack(side="left")
        self.name_x_btn = tk.Button(self.x_frame, text="X", font=("Helvetica", 12, "bold"),
                                    bg="#444444", fg="white", command=lambda: self.set_name("X"))
        self.name_x_btn.pack(side="left")

        self.o_frame = tk.Frame(self.root, bg="#222222")
        self.o_frame.grid(row=0, column=2, sticky="e", padx=10, pady=(10, 0))
        self.name_o_btn = tk.Button(self.o_frame, text="O", font=("Helvetica", 12, "bold"),
                                    bg="#444444", fg="white", command=lambda: self.set_name("O"))
        self.name_o_btn.pack(side="left")
        tk.Label(self.o_frame, text="👤", bg="#222222", fg="white").pack(side="left")

        self.score_label = tk.Label(self.root, text="", font=("Helvetica", 16, "bold"), fg="#00ffcc", bg="#222222")
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 14), fg="yellow", bg="#222222")
        self.timer_label.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Helvetica", 32, "bold"), width=5, height=2,
                                bg="#333333", fg="#ffffff", activebackground="#00cc99",
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i + 3, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        self.restart_button = tk.Button(self.root, text="🔁 Restart Game", font=("Helvetica", 12),
                                        bg="#444444", fg="white", command=self.reset_board)
        self.restart_button.grid(row=6, column=0, pady=15)

        self.close_button = tk.Button(self.root, text="🚪 Close Game", font=("Helvetica", 12),
                                      bg="#999999", fg="white", command=self.root.destroy)
        self.close_button.grid(row=6, column=1, pady=15)

        self.reset_score_button = tk.Button(self.root, text="🔄 Reset Score", font=("Helvetica", 12),
                                            bg="#cc4444", fg="white", command=self.reset_game)
        self.reset_score_button.grid(row=6, column=2, pady=15)

        self.start_btn = tk.Button(self.root, text="✅ Start Game", font=("Helvetica", 12),
                                   bg="#00aa00", fg="white", command=self.start_game)
        self.start_btn.grid(row=7, column=1, pady=(5, 15))

        self.banner_frame = tk.Frame(self.root, bg="#333333", height=30)
        self.banner_frame.grid(row=8, column=0, columnspan=3, sticky="nsew")
        self.banner_frame.grid_propagate(False)
        self.banner_label = tk.Label(self.banner_frame, text="", font=("Helvetica", 20, "bold"),
                                     bg="#333333", fg="white", justify="center")
        self.banner_label.pack(expand=True)

    def on_mode_change(self, value):
        if value == "Single Player":
            level = simpledialog.askstring("Choose Difficulty", "Select AI difficulty (Easy / Medium / Hard):")
            if level in ["Easy", "Medium", "Hard"]:
                self.difficulty = level
            else:
                self.difficulty = "Easy"

    def set_name(self, player):
        new_name = simpledialog.askstring("Enter Name", f"Enter name for Player {player}:")
        if new_name:
            self.player_names[player] = new_name
            (self.name_x_btn if player == "X" else self.name_o_btn).config(text=new_name)
            self.update_score()

    def start_game(self):
        self.started = True
        self.update_score()
        self.reset_board()
        self.start_timer()

    def on_click(self, row, col):
        if not self.started or self.buttons[row][col]["text"] != "":
            return
        self.stop_timer()
        self.make_move(row, col, self.current_player)
        if self.check_game_over(): return
        self.switch_player()
        if self.game_mode.get() == "Single Player" and self.current_player == "O":
            self.root.after(500, self.ai_move)
        else:
            self.start_timer()

    def make_move(self, row, col, player):
        self.buttons[row][col]["text"] = player
        self.board[row][col] = player

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_score()

    def ai_move(self):
        row, col = self.get_ai_move()
        self.make_move(row, col, "O")
        if not self.check_game_over():
            self.switch_player()
            self.start_timer()

    def get_ai_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if self.difficulty == "Easy":
            return random.choice(empty)
        elif self.difficulty == "Medium":
            for i, j in empty:
                self.board[i][j] = "O"
                if self.check_win("O"):
                    self.board[i][j] = ""
                    return i, j
                self.board[i][j] = ""
            for i, j in empty:
                self.board[i][j] = "X"
                if self.check_win("X"):
                    self.board[i][j] = ""
                    return i, j
                self.board[i][j] = ""
            return random.choice(empty)
        else:
            return self.minimax(True)[1]

    def minimax(self, is_maximizing):
        winner = self.check_winner()
        if winner == "O": return 1, None
        if winner == "X": return -1, None
        if self.is_draw(): return 0, None

        best = (-float("inf"), None) if is_maximizing else (float("inf"), None)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O" if is_maximizing else "X"
                    score, _ = self.minimax(not is_maximizing)
                    self.board[i][j] = ""
                    if (is_maximizing and score > best[0]) or (not is_maximizing and score < best[0]):
                        best = (score, (i, j))
        return best

    def check_game_over(self):
        if self.check_win(self.current_player):
            self.score[self.current_player] += 1
            self.update_score()
            self.show_banner(f"🎯 GAME OVER - {self.player_names[self.current_player]} Wins!", "green")
            self.stop_timer()
            self.disable_board()
            return True
        elif self.is_draw():
            self.show_banner("🎯 GAME OVER - It's a Draw!", "yellow")
            self.stop_timer()
            self.disable_board()
            return True
        return False

    def highlight_cells(self, cells):
        for i, j in cells:
            self.buttons[i][j].config(bg="#00ff99")

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                self.highlight_cells([(i, j) for j in range(3)])
                return True
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                self.highlight_cells([(i, j) for i in range(3)])
                return True
        if all(self.board[i][i] == player for i in range(3)):
            self.highlight_cells([(i, i) for i in range(3)])
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            self.highlight_cells([(i, 2 - i) for i in range(3)])
            return True
        return False

    def check_winner(self):
        for player in ["X", "O"]:
            if self.check_win(player): return player
        return None

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["bg"] = "#333333"
                self.buttons[i][j]["state"] = "normal"
                self.board[i][j] = ""
        self.current_player = "X"
        self.stop_timer()

    def reset_game(self):
        self.reset_board()
        self.score = {"X": 0, "O": 0}
        self.update_score()
        self.banner_label.config(text="")
        self.banner_frame.config(height=30)
        self.started = False

    def update_score(self):
        self.score_label.config(
            text=f"🏆 Score - {self.player_names['X']}: {self.score['X']} | {self.player_names['O']}: {self.score['O']}"
        )

    def disable_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = "disabled"

    def show_banner(self, message, color):
        self.banner_label.config(text=message, fg=color)
        self.expand_banner(height=30, target=100)
        self.root.after(7000, lambda: self.shrink_banner(height=100, target=30))

    def expand_banner(self, height, target):
        if height <= target:
            self.banner_frame.config(height=height)
            self.root.after(10, lambda: self.expand_banner(height + 5, target))

    def shrink_banner(self, height, target):
        if height >= target:
            self.banner_frame.config(height=height)
            self.root.after(10, lambda: self.shrink_banner(height - 5, target))
        else:
            self.banner_frame.config(height=target)
            self.banner_label.config(text="")
            self.reset_board()

    def start_timer(self):
        self.remaining_time = self.timer_seconds
        self.update_timer_display()
        self.run_timer()

    def run_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_display()
            self.timer_id = self.root.after(1000, self.run_timer)
        else:
            self.timer_label.config(text="⏰ Time's up!")
            self.switch_player()
            if self.game_mode.get() == "Single Player" and self.current_player == "O":
                self.root.after(500, self.ai_move)
            else:
                self.start_timer()

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer_display(self):
        self.timer_label.config(
            text=f"⏳ {self.player_names[self.current_player]}'s Turn - {self.remaining_time}s left"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
