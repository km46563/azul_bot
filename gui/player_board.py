import tkinter as tk

from gui.floor import FloorWidget
from gui.wall import WallWidget
from gui.pattern_lines import PatternLinesWidget


class PlayerBoard(tk.Frame):
    def __init__(self, master, player_id, adapter, is_current):
        super().__init__(master)
        self.adapter = adapter
        self.player_id = player_id

        # Top row: pattern + wall + label/points
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.pattern_lines = PatternLinesWidget(top_frame, adapter, is_current)
        self.pattern_lines.pack(side=tk.LEFT, pady=10)

        self.wall = WallWidget(top_frame)
        self.wall.pack(side=tk.LEFT, pady=10)

        info_frame = tk.Frame(top_frame)
        info_frame.pack(side=tk.LEFT, padx=10)
        self.player_label = tk.Label(info_frame, text=f'Player {self.player_id}')
        self.player_label.pack(anchor='w')
        self.points = tk.IntVar()
        self.points_label = tk.Label(info_frame, textvariable=self.points)
        self.points_label.pack(anchor='w')

        # Bottom row: floor occupies full width under top_frame
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.floor = FloorWidget(bottom_frame)
        self.floor.pack(side=tk.LEFT, padx=10)