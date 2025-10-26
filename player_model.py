from pattern_lines_model import PatternLines
from wall_model import Wall

floor_scores = [-1, -1, -2, -2, -2, -3, -3]

class AzulPlayer:
    def __init__(self, player_id):
        self.id = player_id
        self.pattern_lines = PatternLines()
        self.wall = Wall()
        self.floor = []
        self.score = 0
        self.first_tile = False

    def can_place_tiles(self, line_idx: int, count: int, color: str) -> bool:
        #if not self.pattern_lines.can_place_tiles(line_idx, count, color):
        #    return False
        if not self.wall.can_place_tiles(line_idx, color):
            return False
        return True

    def round_over(self):
        is_full, colors = self.pattern_lines.pop_full_lines()
        idxs = []
        for line_idx in range(len(is_full)):
            if is_full[line_idx]:
                points, idx = self.wall.place_in_wall(line_idx, colors[line_idx])
                self.score += points
                idxs.append(idx)
            else:
                idxs.append(None)

        for i in range(len(self.floor)):
            if i >= len(floor_scores):
                self.score -= 3
            else:
                self.score += floor_scores[i]

        if self.first_tile:
            self.score -= 1
            self.first_tile = False

        self.floor = []
        return idxs

    def extend_floor(self, overflow, color):
        for i in range(overflow):
            self.floor.append(color)