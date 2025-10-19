import tkinter as tk

from gui.player_board import PlayerBoard


class PlayersPanel(tk.Frame):
    def __init__(self, master, num_players):
        super().__init__(master)
        self.players = []

        for i in range(num_players - 1):
            player = PlayerBoard(self, i)
            player.pack(side=tk.LEFT, padx=5)
            self.players.append(player)

    def draw(self):
        for player in self.players:
            player.pattern_lines.draw()
            player.wall.draw()
            player.player_label.config(text=f'Player {player.player_id}')


class CurrentPlayerPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.player = PlayerBoard(self, 0)
        self.player.pack(side=tk.TOP, pady=10)
        #self.player_label = tk.Label(self)
        #self.player_label.pack(side=tk.TOP)

    def draw(self):
        self.player.pattern_lines.draw()
        self.player.wall.draw()
        #self.player_label.config(text='Player ' + str(self.player.player_id))
