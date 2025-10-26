import tkinter as tk


class PatternLinesWidget(tk.Canvas):
    def __init__(self, master, adapter, is_current, width=100, height=100):
        super().__init__(master, width=width, height=height)
        self.adapter = adapter
        self.is_current = is_current
        self.width = width
        self.height = height
        self.on_click = adapter.pattern_clicked
        self.bind("<Button-1>", self._handle_click)

    def draw(self, colors):
        self.delete("all")
        radius = self.width / 10
        offset = radius * 2
        for i in range(5):
            for j in range(i + 1):
                x = radius + j * offset
                y = radius + i * offset
                self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=colors[i][j], tags=f'{i}x{j}')

    def _handle_click(self, event):
        if self.is_current is False:
            return
        x = event.x
        y = event.y
        if self.on_click:
            if 0 < x < 20 and 0 < y < 20:
                line_idx = 0
            elif 0 < x < 40 and 20 < y < 40:
                line_idx = 1
            elif 0 < x < 60 and 40 < y < 60:
                line_idx = 2
            elif 0 < x < 80 and 60 < y < 80:
                line_idx = 3
            elif 0 < x < 100 and 80 < y < 100:
                line_idx = 4
            else:
                return
            print("kliknięto linię ", line_idx)
            print(x, y)

            self.on_click(line_idx=line_idx)