import tkinter as tk

# Choosing plates for the round
class PlatePicker(tk.Frame):
    def __init__(self, master, width=510, height=100):
        super().__init__(master, width=width, height=height)
        #self.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas - plate preview
        self.canvas = tk.Canvas(self, width=width, height=50, bg='lightyellow')
        self.canvas.pack()

        # Buttons
        self.colors = ['red', 'blue', 'green', 'yellow', 'white']
        self.b_red = tk.Button(self, text='Red', command=lambda: self.master.on_color_click('red'))
        self.b_red.pack(side=tk.LEFT)
        self.b_green = tk.Button(self, text='Green', command=lambda: self.master.on_color_click('green'))
        self.b_green.pack(side=tk.LEFT)
        self.b_yellow = tk.Button(self, text='Yellow', command=lambda: self.master.on_color_click('yellow'))
        self.b_yellow.pack(side=tk.LEFT)
        self.b_white = tk.Button(self, text='White', command=lambda: self.master.on_color_click('white'))
        self.b_white.pack(side=tk.LEFT)
        self.b_blue = tk.Button(self, text='Blue', command=lambda: self.master.on_color_click('blue'))
        self.b_blue.pack(side=tk.LEFT)

        # Label - plate counter
        self.cnt = tk.IntVar(value=0)
        self.counter = tk.Label(self, textvariable=self.cnt)
        self.counter.pack(side=tk.BOTTOM)
        self.show_counter()

        self.config(bg="lightyellow", highlightthickness=1, highlightbackground="black")

    def show_counter(self):
        self.cnt.set(len(self.master.selected_colors))
        #self.counter.destroy()


    def show_preview(self):
        if len(self.master.selected_colors):
            radius = 10
            offset = 20
            for i, color in enumerate(self.master.selected_colors):
                x = 50 + i * offset
                y = 50
                self.canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=color, tags='preview')

        else:
            return
