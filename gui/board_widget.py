import tkinter as tk

from gui.center import CenterWidget
from gui.factories import FactoriesPanel
from gui.plate_picker import PlatePicker
from gui.player_panel import PlayersPanel, CurrentPlayerPanel


class BoardWidget(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_colors = []
        self.plate_picker = PlatePicker(self)
        self.plate_picker.pack(side=tk.BOTTOM, fill=tk.X)

        # Factories-----------------------------------------
        self.factories_panel = FactoriesPanel(self, self.on_plate_click)
        self.factories_panel.pack(side=tk.TOP, pady=20)

        # Center--------------------------------------------
        self.center = CenterWidget(self)
        self.center.pack(side=tk.TOP, pady=20)

        # Player boards-------------------------------------
        self.players = PlayersPanel(self, 3)
        self.players.pack(side=tk.TOP, pady=20)

        self.current_player = CurrentPlayerPanel(self)
        self.current_player.pack(side=tk.TOP, pady=20)

        #self.set_state()


    def set_state(self):
        self.plate_picker.destroy()
        colors = []
        for i in range(5):
            color_group = []
            for j in range(4):
                color_group.append(self.selected_colors[j + 4*i])
            colors.append(color_group)
        for factory, color in zip(self.factories_panel.factories, colors):
            factory.set_tiles(color)
            factory.draw()
        self.after_idle(self.center.draw)
        self.display_players()

    # Clicking on center
    def on_center_click(self, handler):
        x = handler.x

        if x > len(self.center.tiles) * 30:
            return
        if x == 0:
            tile = 0
        else:
            tile = x // 30
        print(self.center.tiles[tile])

    # Clicking on factory & plate
    def on_plate_click(self, handler):
        print("Kliknięto fabrykę ", handler.widget.factory_id)

        x = handler.x
        y = handler.y
        if 10 < x < 40 and 10 < y < 40:
            print('Kliknięto kafelek 1')
            self.center.get_new_tiles(['red', 'green', 'blue'])
        elif 50 < x < 80 and 10 < y < 40:
            print('kliknięto kafelek 2')
        elif 10 < x < 40 and 50 < y < 80:
            print('Kliknięto kafelek 3')
        elif 50 < x < 80 and 50 < y < 80:
            print('kliknięto kafelek 4')

    # Using PlatePicker to get plates
    def on_color_click(self, color: str):
        self.selected_colors.append(color)
        self.update_preview()

        if len(self.selected_colors) == 20:
            self.set_state()

    def update_preview(self):
        self.plate_picker.show_counter()
        self.plate_picker.show_preview()
        self.plate_picker.place()

    def display_players(self):
        self.players.draw()
        self.current_player.draw()


