import tkinter as tk

from azulGame import AzulGame


class Menu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.title("Main menu")
        self.transient(self.parent)
        self.grab_set()

        # Number of players
        tk.Label(self, text="Number of players:").grid(row=0, column=0, sticky=tk.W)
        self.num_var = tk.IntVar(value=2)
        for i in range(2, 5):
            rb = tk.Radiobutton(self, text=str(i), variable=self.num_var, value=i)
            rb.grid(row=0, column=i-1, sticky=tk.W)

        # Bot's turn
        tk.Label(self, text="Bot's turn:").grid(row=1, column=0, sticky=tk.W)
        self.turn_var = tk.IntVar(value=1)
        for i in range(1, 5):
            rb = tk.Radiobutton(self, text=str(i), variable=self.turn_var, value=i-1)
            rb.grid(row=1, column=i - 1 + 1, sticky=tk.W)

        # Plate picking mode
        tk.Label(self, text="Plate picking mode:").grid(row=2, column=0, sticky=tk.W)
        self.plate_var = tk.StringVar(value='choose')
        tk.Radiobutton(self, text="random", variable=self.plate_var, value='random').grid(row=2, column=1, sticky=tk.W)
        tk.Radiobutton(self, text="choose", variable=self.plate_var, value='choose').grid(row=2, column=2, sticky=tk.W)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        tk.Button(btn_frame, text='Cancel', command=self._on_cancel).pack(side=tk.RIGHT, padx=6)
        tk.Button(btn_frame, text='Start', command=self._on_start).pack(side=tk.RIGHT)

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def _on_start(self):
        n = self.num_var.get()
        t = self.turn_var.get()
        p = self.plate_var.get()
        self.result = {
            'num_players': n,
            'turn': t,
            'plate_picker_mode': p,
        }
        self.destroy()