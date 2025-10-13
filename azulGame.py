from typing import List

from bot import greedy_ai
from player import AzulPlayer


class AzulGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.factories = [[] for _ in range(5)]
        self.center = []
        self.players = [AzulPlayer(i) for i in range(num_players)]
        self.current_player = 0
        self.first_tile = -1

    def deal_tiles(self, bag: List[str]):
        self.center.clear()
        for f in self.factories:
            f.clear()
            for _ in range(4):
                if bag:
                    f.append(bag.pop())

    def next_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def is_round_over(self) -> bool:
        if any(self.factories):
            return False
        if self.center:
            return False

        if self.first_tile != -1:
            self.current_player = self.first_tile
            self.first_tile = -1
        return True

    def is_game_over(self) -> bool:
        for player in self.players:
            for row in player.wall:
                if all(cell is not None for cell in row):
                    return True
        return False

