from typing import List

from bot import Bot
from player_model import AzulPlayer


def players_setup(num_players, bots_turn):
    players = []
    for i in range(num_players):
        if i == bots_turn:
            players.append(Bot(i))
        else:
            players.append(AzulPlayer(i))
    return players


class AzulGame:
    def __init__(self, num_players, bots_turn):
        self.num_players = num_players
        self.bots_turn = bots_turn
        self.factories = [[] for _ in range(5)]
        self.center = []
        self.players = players_setup(num_players, bots_turn)
        self.current_player = 0
        self.first_tile = -1
        self.picked_colors = []
        self.selection = None

    #Players---------------------------------------------------------------------------

    def get_player(self, player_id: int)-> AzulPlayer:
        return self.players[player_id]

    def get_bot_id(self):
        return self.bots_turn

    def get_non_current_player_ids(self):
        ids = []
        for i in range(self.num_players):
            if i != self.current_player:
                ids.append(i)
        return ids


    def next_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def round_over(self):
        for player in self.players:
            player.round_over()
            if player.first_tile:
                self.current_player = player.id

        self.factories = [[] for _ in range(5)]
        self.center = []
        self.picked_colors = []
        self.first_tile = -1

    def game_over(self):
        for player in self.players:
            player.game_over()

    # Factories------------------------------------------------------------------------
    def set_factories(self):
        for factory in range(5):
            for plate in range(4):
                self.factories[factory].append(self.picked_colors[4 * factory + plate])

    def clean_factory(self, factory_id):
        self.factories[factory_id] = []

    # Center--------------------------------------------------------------------------
    def get_center(self):
        return self.center

    def get_first_tile(self):
        return self.first_tile

    def add_to_center(self, colors):
        for color in colors:
            self.center.append(color)

    def remove_from_center(self, color):
        self.center = [c for c in self.center if c != color]

    # PlatePicker----------------------------------------------------------------------
    def get_picked_colors(self):
        return self.picked_colors

    def append_picked_colors(self, color):
        self.picked_colors.append(color)

    # State&Selections-----------------------------------------------------------------
    def get_state(self):
        return {'factories': self.factories,
                'center': self.center,
                'players': self.players,}

    def get_selection(self):
        return self.selection

    def selection_change(self, factory_id, color):
        if self.selection is None:
            self.selection = {}
        self.selection['factory'] = factory_id
        self.selection['color'] = color
        count = 0
        if factory_id == -1:
            factory = self.center
        else:
            factory = self.factories[factory_id]
        for c in factory:
            if c == color:
                count += 1
        self.selection['count'] = count

    def selection_reset(self):
        self.selection = None

    # Checkers-------------------------------------------------------------------------
    def is_round_over(self) -> bool:
        if any(self.factories):
            return False
        if self.center:
            return False

        # Reset the 'first tile' tile
        # Player having 'first_tile' tile, have the first move in the next round
        if self.first_tile != -1:
            self.current_player = self.first_tile
            self.first_tile = -1
        return True

    def is_game_over(self) -> bool:
        for player in self.players:
            for row in player.wall.wall:
                if all(cell is not None for cell in row):
                    return True
        return False


    # Not in GUI-----------------------------------------------------------------------
    def deal_tiles(self, bag: List[str]):
        self.center.clear()
        for f in self.factories:
            f.clear()
            for _ in range(4):
                if bag:
                    f.append(bag.pop())
