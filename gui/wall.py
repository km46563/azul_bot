import tkinter as tk


class WallWidget(tk.Canvas):
    def __init__(self, master, width=100, height=100):
        super().__init__(master, width=width, height=height)
        self.width = width
        self.height = height
        self.colors = [['blue', 'yellow', 'red', 'green', 'white'],
                       ['white', 'blue', 'yellow', 'red', 'green'],
                       ['green', 'white', 'blue', 'yellow', 'red'],
                       ['red', 'green', 'white', 'blue', 'yellow'],
                       ['yellow', 'red', 'green', 'white', 'blue']]
        self.placed_tiles = []

    def draw(self):
        self.delete('all')

        outline_w = 2  # outline width
        padding = 2
        margin = max(1, outline_w / 2) + padding
        gap = 3

        n = 5
        avail = min(self.width, self.height) - 2 * margin
        total_gap_space = (n - 1) * gap
        cell_size = (avail - total_gap_space) / n

        for i in range(5):
            for j in range(5):
                # środek komórki
                x1 = margin + j * (cell_size + gap)
                y1 = margin + i * (cell_size + gap)
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.create_rectangle(x1, y1, x2, y2,
                                      fill=self.colors[i][j],
                                      outline='gray70',
                                      width=outline_w,
                                      tags=f'{i}x{j}')

        for placed_tile in self.placed_tiles:
            self.mark_placed_tiles(placed_tile)


    def mark_placed_tiles(self, plate):
        for id in self.find_withtag(plate):
            self.itemconfig(id, width=4, outline="magenta2")

    def place_tile(self, plate):
        self.placed_tiles.append(plate)
