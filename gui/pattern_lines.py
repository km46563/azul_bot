import tkinter as tk


class PatternLinesWidget(tk.Canvas):
    def __init__(self, master, width=100, height=100):
        super().__init__(master, width=width, height=height)
        self.width = width
        self.height = height

    def draw(self):
        radius = self.width / 10
        offset = radius * 2
        for i in range(5):
            for j in range(i + 1):
                x = radius + j * offset
                y = radius + i * offset
                self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill='bisque', tags=f'{i}x{j}')
