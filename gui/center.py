import tkinter as tk

# Center
class CenterWidget(tk.Canvas):
    def __init__(self, master, adapter, width=660, height=30):
        super().__init__(master, width=width, height=height)
        self.config(bg="lightblue", highlightthickness=1, highlightbackground="black")
        self.width = width
        self.height = height
        self.tiles = []
        self.adapter = adapter
        self.bind("<Button-1>", self.on_center_click)

    def set_adapter(self, adapter):
        self.adapter = adapter

    def set_tiles(self, colors):
        self.tiles = colors

    def draw(self, first_tile=True):
        print('rysuje sie')
        self.delete('all')
        radius = 15
        offset = 30
        for i, tile in enumerate(self.tiles):
            x = 15 + i * offset
            y = 15
            self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=tile, tags=('tile', tile))
        if first_tile:
            self.create_rectangle(self.width - offset, 0, self.width, offset, fill='gray25', tags=('tile', '-'))


    # Clicking on center
    def on_center_click(self, handler):
        x = handler.x

        if x > len(self.tiles) * 30:
            return
        if x == 0:
            tile = 0
        else:
            tile = x // 30
        print(self.tiles[tile])

        self.adapter.center_clicked(self.tiles[tile])

    def highlight_color(self, color):
        for id in self.find_withtag("tile"):
            self.itemconfig(id, width=1, outline="black")
        for id in self.find_withtag(color):
            self.itemconfig(id, width=3, outline="magenta2")

    def unhighlight(self):
        for id in self.find_withtag("tile"):
            self.itemconfig(id, width=1, outline="black")

'''
    def get_new_tiles(self, colors):
        self.delete("all")
        for color in colors:
            print("rozszerzono o ", color)
            self.tiles.append(color)
        self.draw()
'''


