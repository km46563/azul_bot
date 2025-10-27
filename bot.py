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
                if player.can_place_tiles(line_idx, count, color):
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

        state = self.pattern_lines.get_state()
        pattern_lines = state["pattern_lines"]
        pattern_capacity = state["pattern_capacity"]
        in_line = len(pattern_lines[line]) if line != -1 else 0
        capacity = pattern_capacity[line] if line != -1 else 0

        # Wszytkie kafelki idą na podłogę (0 punktów)
        if line == -1:
            return 0, count

        space_left = capacity - in_line
        to_place = min(space_left, count)       # Ile kafelków położymy (max tyle, ile brakuje)
        overflow = max(0, count - space_left)   # ile kafelków zostanie (minimum 0)

        gain = 0
        if to_place == space_left and space_left > 0:   # Zamkniemy linię
            col = self.wall.wall_pattern[line].index(color)

            # Counting points for neighborous tiles
            gain += self.wall.points_for_tile(line, col)
            # Counting points for collecting full column/line/color
            gain += self.wall.line_completion(line, col)

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
            state = self.pattern_lines.get_state()
            pattern_lines = state["pattern_lines"]
            pattern_capacity = state["pattern_capacity"]
            if move["line"] >= 0 and len(pattern_lines[move["line"]]) + move["count"] == pattern_capacity[move["line"]]:
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
