import tkinter as tk

from gui.wall import WallWidget
from gui.pattern_lines import PatternLinesWidget


class PlayerBoard(tk.Frame):
    def __init__(self, master, player_id):
        super().__init__(master)
        self.pattern_lines = PatternLinesWidget(self)
        self.pattern_lines.pack(side=tk.LEFT, pady=10)
        self.wall = WallWidget(self)
        self.wall.pack(side=tk.LEFT, pady=10)
        self.player_id = player_id
        self.player_label = tk.Label(self, text=f'Player {self.player_id}')
        self.player_label.pack(side=tk.LEFT)
