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

    def draw(self, placed_tiles):
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
                if f'{i}x{j}' in placed_tiles:
                    self.create_rectangle(x1, y1, x2, y2,
                                          fill=self.colors[i][j],
                                          outline='magenta2',
                                          width=outline_w + 1,
                                          tags=f'{i}x{j}')
                else:
                    self.create_rectangle(x1, y1, x2, y2,
                                          fill=self.colors[i][j],
                                          outline='gray70',
                                          width=outline_w,
                                          tags=f'{i}x{j}')
