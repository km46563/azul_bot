import tkinter as tk

# Factories
class FactoryWidget(tk.Canvas):
    def __init__(self, master, on_click=None, width=90, height=90):
        super().__init__(master, width=width, height=height)
        self.config(bg="lightyellow", highlightthickness=1, highlightbackground="black")
        self.tiles = []
        self.factory_id = None
        if on_click:
            self.bind("<Button-1>", on_click)

    def set_tiles(self, colors):
        self.tiles = colors

    def draw(self):
        radius = 15
        offset = 40
        color = 0
        for i in range(2):
            for j in range(2):
                x = 25 + j * offset
                y = 25 + i * offset
                self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=self.tiles[color])
                color += 1

class FactoriesPanel(tk.Frame):
    def __init__(self, master, on_click=None):
        super().__init__(master)
        self.factories = []
        for i in range(5):
            factory = FactoryWidget(self, on_click=on_click)
            factory.pack(side=tk.LEFT, padx=20, pady=20)
            factory.factory_id = i
            self.factories.append(factory)
        for i, factory in enumerate(self.factories):
            #factory.master = top_frame
            factory.pack(side=tk.LEFT, padx=20, pady=20)