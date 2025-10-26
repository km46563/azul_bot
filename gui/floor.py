import tkinter as tk

class FloorWidget(tk.Canvas):
    def __init__(self, master, adapter, width=200, height=20):
        super().__init__(master, width=width, height=height)
        self.config(bg="lightblue", highlightthickness=1, highlightbackground="black")
        self.adapter = adapter
        self.width = width
        self.height = height
        self.bind("<Button-1>", self._handle_click)

    def draw(self, floor, first_tile):
        self.delete('all')
        radius = 10
        offset = 20
        if first_tile:
            self.create_rectangle(0, 0, offset, offset, fill='gray25', tags=('tile', '-'))
        for i, tile in enumerate(floor):
            if first_tile:
                x = 30 + i * offset
            else:
                x = 10 + i * offset
            y = 10
            self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=tile, tags=('tile', tile))

    def _handle_click(self, event):
        self.adapter.floor_clicked()