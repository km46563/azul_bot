import tkinter as tk

from gui.player_board import PlayerBoard


class PlayersPanel(tk.Frame):
    def __init__(self, master, adapter, num_players):
        super().__init__(master)
        self.adapter = adapter
        self.players = []
        self.num_players = num_players

        for i in range(self.num_players):
            if self.adapter.get_current_player() == i:
                continue
            player = PlayerBoard(self, i, adapter, False)
            player.pack(side=tk.LEFT, padx=5)
            self.players.append(player)

    def draw(self):
        for player in self.players:
            pattern = self.adapter.get_pattern_to_draw(player.player_id)
            player.pattern_lines.draw(pattern)
            player.wall.draw(self.adapter.get_placed_tiles(player.player_id))
            player.player_label.config(text=f'Player {player.player_id}')
            player.points.set(self.adapter.get_player_points(player.player_id))


class CurrentPlayerPanel(tk.Frame):
    def __init__(self, master, adapter, player_id):
        super().__init__(master)
        self.adapter = adapter
        self.player = PlayerBoard(self, player_id, adapter, True)
        self.player.pack(side=tk.TOP, pady=10)

    def draw(self):
        pattern = self.adapter.get_pattern_to_draw(self.player.player_id)
        floor, first_tile = self.adapter.get_floor(self.player.player_id)

        self.player.pattern_lines.draw(pattern)
        self.player.wall.draw(self.adapter.get_placed_tiles(self.player.player_id))
        self.player.player_label.config(text='Player ' + str(self.player.player_id))
        self.player.points.set(self.adapter.get_player_points(self.player.player_id))
        self.player.floor.draw(floor, first_tile)