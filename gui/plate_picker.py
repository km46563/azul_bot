import tkinter as tk

# Choosing plates for the round
class PlatePicker(tk.Frame):
    def __init__(self, master, adapter, width=510, height=100):
        super().__init__(master, width=width, height=height)

        self.adapter = adapter

        # Canvas - plate preview
        self.canvas = tk.Canvas(self, width=width, height=50, bg='lightyellow')
        self.canvas.pack()

        # Buttons
        self.colors = ['red', 'blue', 'green', 'yellow', 'white']
        self.b_red = tk.Button(self, text='Red', command=lambda: self.adapter.picked_color('red'))
        self.b_red.pack(side=tk.LEFT)
        self.b_green = tk.Button(self, text='Green', command=lambda: self.adapter.picked_color('green'))
        self.b_green.pack(side=tk.LEFT)
        self.b_yellow = tk.Button(self, text='Yellow', command=lambda: self.adapter.picked_color('yellow'))
        self.b_yellow.pack(side=tk.LEFT)
        self.b_white = tk.Button(self, text='White', command=lambda: self.adapter.picked_color('white'))
        self.b_white.pack(side=tk.LEFT)
        self.b_blue = tk.Button(self, text='Blue', command=lambda: self.adapter.picked_color('blue'))
        self.b_blue.pack(side=tk.LEFT)

        # Label - plate counter
        self.cnt = tk.IntVar(value=0)
        self.counter = tk.Label(self, textvariable=self.cnt)
        self.counter.pack(side=tk.BOTTOM)
        #self.show_counter()

        self.config(bg="lightyellow", highlightthickness=1, highlightbackground="black")


    def show_counter(self):
        self.cnt.set(len(self.adapter.get_picked_colors()))

    def show_preview(self):
        picked_colors = self.adapter.get_picked_colors()

        if len(picked_colors):
            radius = 10
            offset = 20
            for i, color in enumerate(picked_colors):
                x = 50 + i * offset
                y = 50
                self.canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=color, tags='preview')
        else:
            return

    def update_preview(self):
        self.show_counter()
        self.show_preview()
        #self.place()