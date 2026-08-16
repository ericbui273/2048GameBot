import random
import tkinter as tk
from tkinter import font as tkfont
 
from game2048.AI import AI
 
# ---------------------------------------------------------------------------
# Visual styling (classic 2048 palette)
# ---------------------------------------------------------------------------
BG_COLOR = "#faf8ef"
BOARD_BG = "#bbada0"
EMPTY_CELL = "#cdc1b4"
CELL_SIZE = 100
CELL_PAD = 12
 
TILE_COLORS = {
    0: ("#cdc1b4", "#cdc1b4"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
DEFAULT_TILE_COLOR = ("#3c3a32", "#f9f6f2")
 
BOARD_PIXELS = CELL_SIZE * 4 + CELL_PAD * 5
 
 
class App(tk.Tk):
    """
Simple Tkinter GUI for watching the 2048 expectimax AI play.

Attributes:
    mode: user can choose one from two modes from the start screen:
        + Continuous: the AI plays move after move on its own (a short delay
        between moves so you can actually watch it happen). No keys do anything.
        + Step: the AI computes and makes exactly one move each time you press
        the SPACE bar. Nothing else advances the game.
    max_depth: defined based on the optimal level that user chooses from the start screen
        + Default: the search has maximum depth according to the function best_move() 
        in class AI
        + Level 2-5: max depth 2-5
    after_id: handle for the scheduled continuous move, set back to None when a new game is started or the game is over
    game_active: whether a game is going on, set to True when a new game is started and set to False when the game is over
    
"""
    def __init__(self):
        super().__init__()
        self.title("2048 AI Watcher")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
 
        self.title_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=14)
        self.button_font = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.tile_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
 
        self.mode = None
        self.max_depth = None 
        self.ai = None
        self.after_id = None
        self.game_active = False
 
        self.level_var = tk.StringVar(value="Default")
 
        self._build_start_screen()

    def _build_start_screen(self):
        """Build the start screen, where user gets to choose how the AI should play and at which optimal level
        """
        self.start_frame = tk.Frame(self, bg=BG_COLOR, padx=40, pady=40)
        self.start_frame.pack()
 
        tk.Label(self.start_frame, text="2048 AI Watcher", font=self.title_font,
                 bg=BG_COLOR, fg="#776e65").pack(pady=(0, 10))
        tk.Label(self.start_frame,
                 text="Watch an AI bot play 2048.\nChoose how you'd like it to play:",
                 font=self.label_font, bg=BG_COLOR, fg="#776e65", justify="center").pack(pady=(0, 20))
 
        level_frame = tk.Frame(self.start_frame, bg=BG_COLOR)
        level_frame.pack(pady=(0, 20))
        tk.Label(level_frame, text="Optimal level", font=("Helvetica", 12, "bold"),
                 bg=BG_COLOR, fg="#776e65").pack()
        tk.Label(level_frame, text="Higher = smarter but slower",
                 font=("Helvetica", 10), bg=BG_COLOR, fg="#9b9187").pack(pady=(0, 8))
 
        radio_row = tk.Frame(level_frame, bg=BG_COLOR)
        radio_row.pack()
        for label in ("Default", "2", "3", "4", "5"):
            tk.Radiobutton(radio_row, text=label, variable=self.level_var, value=label,
                           font=self.label_font, bg=BG_COLOR, fg="#776e65",
                           selectcolor="#eee4da", activebackground=BG_COLOR,
                           indicatoron=True, padx=6).pack(side="left")
 
        tk.Button(self.start_frame, text="Watch Continuously", font=self.button_font,
                  bg="#8f7a66", fg="white", activebackground="#9f8b76", activeforeground="white",
                  relief="flat", padx=20, pady=12, width=22,
                  command=lambda: self._start_game("continuous")).pack(pady=6)
 
        tk.Button(self.start_frame, text="Step Mode (press SPACE)", font=self.button_font,
                  bg="#edc22e", fg="white", activebackground="#f0d15a", activeforeground="white",
                  relief="flat", padx=20, pady=12, width=22,
                  command=lambda: self._start_game("step")).pack(pady=6)
 

    def _start_game(self, mode):
        self.mode = mode
        level = self.level_var.get()
        self.max_depth = None if level == "Default" else int(level)
        self.start_frame.destroy()
 
        self.game_frame = tk.Frame(self, bg=BG_COLOR, padx=20, pady=20)
        self.game_frame.pack()
 
        header = tk.Frame(self.game_frame, bg=BG_COLOR)
        header.pack(fill="x", pady=(0, 15))
 
        tk.Label(header, text="2048 AI Watcher", font=self.title_font,
                 bg=BG_COLOR, fg="#776e65").pack(side="left")
 
        score_box = tk.Frame(header, bg=BOARD_BG, padx=15, pady=6)
        score_box.pack(side="right")
        tk.Label(score_box, text="SCORE", font=("Helvetica", 10, "bold"),
                 bg=BOARD_BG, fg="#eee4da").pack()
        self.score_var = tk.StringVar(value="0")
        tk.Label(score_box, textvariable=self.score_var, font=("Helvetica", 18, "bold"),
                 bg=BOARD_BG, fg="white").pack()
 
        level_label = "default (adaptive)" if self.max_depth is None else f"level {self.max_depth}"
        self.status_var = tk.StringVar(
            value=(f"AI is playing on its own... ({level_label})" if mode == "continuous"
                   else f"Press SPACE to make the next move ({level_label})"))
        tk.Label(self.game_frame, textvariable=self.status_var, font=self.label_font,
                 bg=BG_COLOR, fg="#776e65").pack(pady=(0, 10))
 
        self.canvas = tk.Canvas(self.game_frame, width=BOARD_PIXELS, height=BOARD_PIXELS,
                                 bg=BOARD_BG, highlightthickness=0)
        self.canvas.pack()
 
        controls = tk.Frame(self.game_frame, bg=BG_COLOR)
        controls.pack(pady=(15, 0))
        tk.Button(controls, text="New Game", font=self.button_font, bg="#8f7a66", fg="white",
                  relief="flat", padx=14, pady=8, command=self._new_game).pack(side="left", padx=5)
        tk.Button(controls, text="Back to Menu", font=self.button_font, bg="#bbada0", fg="white",
                  relief="flat", padx=14, pady=8, command=self._back_to_menu).pack(side="left", padx=5)
 
        self.bind("<space>", self._on_space)
        self.focus_set()
 
        self._new_game()
 
    def _new_game(self):
        """A function called when user clicks "New game", after which scheduling for the next move is cancelled, after_id is set back to None, 
        and a new game in the same mode and level with the current game starts
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
 
        self.ai = AI()
        self.ai.new_game()
        self.game_active = True
        self._draw_board()
 
        level_label = "default (adaptive)" if self.max_depth is None else f"level {self.max_depth}"
        if self.mode == "continuous":
            self.status_var.set(f"AI is playing on its own... ({level_label})")
            self.after_id = self.after(250, self._continuous_step)
        else:
            self.status_var.set(f"Press SPACE to make the next move ({level_label})")
 
    def _back_to_menu(self):
        """A function called when the user clicks "Back to menu", after which scheduling for the next move is cancelled, after_id is set back to None, and the screen returns to the start screen
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.unbind("<space>")
        self.game_frame.destroy()
        self._build_start_screen()
 

    def _on_space(self):
        """A function called when the user presses SPACE, which tells the AI to make the next move if the step mode was chosen and the game is not over
        """
        if self.mode != "step" or not self.game_active:
            return
        self._make_one_move()
 
    def _continuous_step(self):
        """A function letting the AI continuously make a new move until the game is over and game_active becomes False
        """
        if not self.game_active:
            return
        self._make_one_move()
        if self.game_active:
            self.after_id = self.after(250, self._continuous_step)
 
    def _make_one_move(self):
        game = self.ai.game
        if game.game_over():
            self._end_game()
            return
 
        move = self.ai.best_move(self.max_depth)
        game.make_move(move)
        self._draw_board()
 
        if game.game_over():
            self._end_game()
        elif self.mode == "step":
            level_label = "default (adaptive)" if self.max_depth is None else f"level {self.max_depth}"
            self.status_var.set(f"Press SPACE to continue")
 
    def _end_game(self):
        self.game_active = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.status_var.set(f"Game over! Final score: {self.ai.game.score}")
 
    def _draw_board(self):
        """A function called after each time a move is made to update the board
        """
        self.canvas.delete("all")
        board = self.ai.game.board.board
        self.score_var.set(str(self.ai.game.score))
 
        for r in range(4):
            for c in range(4):
                value = board[r][c]
                x0 = CELL_PAD + c * (CELL_SIZE + CELL_PAD)
                y0 = CELL_PAD + r * (CELL_SIZE + CELL_PAD)
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
 
                bg, fg = TILE_COLORS.get(value, DEFAULT_TILE_COLOR) if value else (EMPTY_CELL, EMPTY_CELL)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="")
 
                if value:
                    size = 28 if value < 1024 else (22 if value < 10240 else 18)
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value),
                                             fill=fg, font=("Helvetica", size, "bold"))