import tkinter as tk


# Factories
class FactoryWidget(tk.Canvas):
    def __init__(self, master, factory_id, on_click=None, width=90, height=90):
        super().__init__(master, width=width, height=height)
        self.config(bg="lightyellow", highlightthickness=1, highlightbackground="black")
        self.tiles = []
        self.item_map = {}
        self.factory_id = factory_id
        self.on_click = on_click
        self.bind("<Button-1>", self._handle_click)

    def set_tiles(self, colors):
        self.tiles = colors

    def draw(self):
        self.delete("all")
        radius = 15
        offset = 40
        for idx, color in enumerate(self.tiles):
            row = idx // 2
            col = idx % 2
            x = 25 + col * offset
            y = 25 + row * offset
            item = self.create_rectangle(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=color,
                tags=("tile", color),
                width=1,
                outline=""
            )
            self.item_map[item] = (idx, color)

    def _handle_click(self, event):
        x = event.x
        y = event.y
        if self.on_click:
            if 10 < x < 40 and 10 < y < 40:
                color = self.tiles[0]
            elif 50 < x < 80 and 10 < y < 40:
                color = self.tiles[1]
            elif 10 < x < 40 and 50 < y < 80:
                color = self.tiles[2]
            elif 50 < x < 80 and 50 < y < 80:
                color = self.tiles[3]
            else:
                color = None
            print("kliknięto kafelek ", color)

            self.on_click(factory_id=self.factory_id, color=color)

    def highlight_color(self, color):
        for id in self.find_withtag("tile"):
            self.itemconfig(id, width=1, outline="")
        for id in self.find_withtag(color):
            self.itemconfig(id, width=3, outline="magenta2")

    def unhighlight_colors(self):
        for id in self.find_withtag("tile"):
            self.itemconfig(id, width=1, outline="")


class FactoriesPanel(tk.Frame):
    def __init__(self, master, adapter):
        super().__init__(master)
        self.adapter = adapter
        self.factories = []

        for i in range(5):
            factory = FactoryWidget(self, i, on_click=self.adapter.factory_clicked)
            factory.pack(side=tk.LEFT, padx=20, pady=20)
            factory.factory_id = i
            self.factories.append(factory)

        for factory in self.factories:
            factory.pack(side=tk.LEFT, padx=20, pady=20)

    def create_factories(self):
        if self.factories:
            self.destroy()

        for i in range(5):
            factory = FactoryWidget(self, i, on_click=self.adapter.factory_clicked)
            factory.pack(side=tk.LEFT, padx=20, pady=20)
            factory.factory_id = i
            self.factories.append(factory)

    def unhighlight_colors(self, to_continue: int):
        for i in range(len(self.factories)):
            if i == to_continue:
                continue
            self.factories[i].unhighlight_colors()