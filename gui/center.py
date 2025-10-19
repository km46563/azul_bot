import tkinter as tk

# Center
class CenterWidget(tk.Canvas):
    def __init__(self, master, width=660, height=30):
        super().__init__(master, width=width, height=height)
        self.config(bg="lightblue", highlightthickness=1, highlightbackground="black")
        #self.pack()
        self.tiles = []
        self.bind("<Button-1>", self.master.on_center_click)

    def get_new_tiles(self, colors):
        self.delete("all")
        for color in colors:
            print("rozszerzono o ", color)
            self.tiles.append(color)
        self.draw()

    def draw(self):
        print('rysuje sie')
        radius = 15
        offset = 30
        for i, tile in enumerate(self.tiles):
            x = 15 + i * offset
            y = 15
            self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=tile, tags=tile)
