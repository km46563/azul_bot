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

    def draw(self):
        radius = self.width / 10
        offset = radius * 2
        for i in range(5):
            for j in range(5):
                x = radius + j * offset
                y = radius + i * offset
                self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=self.colors[i][j], tags=f'{i}x{j}')
