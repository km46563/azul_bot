from typing import List, Dict, Optional

from player_model import AzulPlayer

wall_pattern = [['b', 'y', 'r', 'g', 'w'],
                ['w', 'b', 'y', 'r', 'g'],
                ['g', 'w', 'b', 'y', 'r'],
                ['r', 'g', 'w', 'b', 'y'],
                ['y', 'r', 'g', 'w', 'b']]

floor_pattern = [-1, -1, -2, -2, -2, -3, -3]

def possible_moves(player, factories, center) -> List[Dict]:
    # TODO: Jeżeli w wallu gracza jest kolor w linii, nie można go układać
    moves = []
    sources = [center] + factories
    for i, source in enumerate(sources):
        colors = set(source)
        for color in colors:
            count = source.count(color)
            for line_idx in range(5):
                if player.can_place_tile(line_idx, color):
                    moves.append({"source": i - 1, "color": color, "line": line_idx, "count": count})
            moves.append({"source": i - 1, "color": color, "line": -1, "count": count})
    return moves


class Bot(AzulPlayer):
    def __init__(self, player_id):
        super().__init__(player_id)

    def floor_minus(self, overflow: int) -> Optional[int]:
        score = 0
        for i in range(overflow):
            score += floor_pattern[i % len(floor_pattern)]
        return score

    def count_points(self, move: dict) -> tuple[int, int]:
        line = move["line"]
        color = move["color"]
        count = move["count"]
        in_line = len(self.pattern_lines[line]) if line != -1 else 0
        capacity = self.pattern_capacity[line] if line != -1 else 0

        # Wszytkie kafelki idą na podłogę (0 punktów)
        if line == -1:
            return 0, count

        space_left = capacity - in_line
        to_place = min(space_left, count)       # Ile kafelków położymy (max tyle, ile brakuje)
        overflow = max(0, count - space_left)   # ile kafelków zostanie (minimum 0)

        gain = 0
        if to_place == space_left and space_left > 0:   # Zamkniemy linię
            col = self.wall[line].index(color)
            placeholder = self.wall[line][col]    # Na chwilę zmieniamy pole w wallu bota
            self.wall[line][col] = color

            # Liczenie punktów za przylegające kafelki
            for i in range(len(self.pattern_lines)):
                j = 1
                while col - j >= 0 and self.wall[i][col - j] is not None:
                    gain += 1
                    j += 1
                j = 1
                while col + j <= 4 and self.wall[i][col + j] is not None:
                    gain += 1
                    j += 1
                j = 1
                while i - j >= 0 and self.wall[i - j][col] is not None:
                    gain += 1
                    j += 1
                j = 1
                while i + j <= 4 and self.wall[i + j][col] is not None:
                    gain += 1
                    j += 1

            if all(self.wall[line][k] is not None for k in range((len(wall_pattern[line])))):
                gain += 2
            if all(self.wall[k][col] is not None for k in range(len(wall_pattern[line]))):
                gain += 7
            if sum(x == color for r in self.wall for x in r) == 5:
                gain += 10


            self.wall[line][col] = placeholder    # Przywracamy proprzednie pole
        else:   # Nie zamkniemy linii
            gain = 0

        return gain, overflow


    def greedy_ai(self, state):
        factories = state["factories"]
        center = state["center"]
        moves = possible_moves(self, factories, center)
        best_score = -999
        best_move = None

        for move in moves:
            gain = 0

            # Premiowanie dopełnienia swojej linii
            if move["line"] >= 0 and len(self.pattern_lines[move["line"]]) + move["count"] == self.pattern_capacity[move["line"]]:
                gain += 10
            # Minus 1 punkt za kafelek '-'
            if move["source"] == -1 and "-" in center:
                gain -= 1
            gain += move["count"]

            # Obliczanie wpływu ruchu na punkty za zajmowane sąsiednie pola na wallu,
            # za nadmiarowe płytki oraz pełne wiersze, kolumny i kolory
            neighbor_score, overflow = self.count_points(move)

            gain += neighbor_score + self.floor_minus(overflow)

            if gain > best_score:
                best_score = gain
                best_move = move
        return best_move
