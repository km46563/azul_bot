import tkinter as tk

from gui.center import CenterWidget
from gui.factories import FactoriesPanel
from gui.plate_picker import PlatePicker
from gui.player_panel import PlayersPanel, CurrentPlayerPanel


class BoardWidget(tk.Frame):
    def __init__(self, master, adapter, plate_picker_mode):
        super().__init__(master)

        self.adapter = adapter

        # Factories-----------------------------------------
        self.factories_panel = FactoriesPanel(self, adapter)
        self.factories_panel.pack(side=tk.TOP, pady=20)

        # Center--------------------------------------------
        self.center = CenterWidget(self, adapter)
        self.center.pack(side=tk.TOP, pady=20)

        # Player boards-------------------------------------
        self.players = PlayersPanel(self, adapter, self.adapter.get_num_players())
        self.players.pack(side=tk.TOP, pady=20)

        self.current_player = CurrentPlayerPanel(self, adapter, self.adapter.get_current_player())
        self.current_player.pack(side=tk.TOP, pady=20)

        # Plate Picker--------------------------------------
        self.plate_picker_mode = plate_picker_mode
        self.plate_picker = PlatePicker(self, adapter, self.plate_picker_mode)
        self.plate_picker.pack(side=tk.TOP, fill=tk.X)


    def set_state(self, state, current_player):
        factories_state = state['factories']
        center_state = state['center']

        for factory, color in zip(self.factories_panel.factories, factories_state):
            factory.set_tiles(color)
            factory.draw()

        self.center.set_tiles(center_state)
        self.center.draw(self.adapter.is_first_tile_available())
        self.display_players()

    def create_plate_picker(self):
        self.plate_picker.destroy()
        self.plate_picker = PlatePicker(self, self.adapter, self.plate_picker_mode)
        self.plate_picker.pack(side=tk.BOTTOM, pady=20)

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

    def display_players(self):
        for player in self.players.players:
            floor, first_tile = self.adapter.get_floor(player.player_id)
            player.floor.draw(floor, first_tile)
        player = self.current_player.player
        floor, first_tile = self.adapter.get_floor(player.player_id)
        player.floor.draw(floor, first_tile)

        self.players.draw()
        self.current_player.draw()


