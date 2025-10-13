class AzulPlayer:
    def __init__(self, player_id):
        self.id = player_id
        self.pattern_lines = [[] for _ in range(5)]
        self.pattern_capacity = [i + 1 for i in range(5)]
        self.wall = [[None for _ in range(5)] for _ in range(5)]
        self.floor = []
        self.score = 0
        self.first_tile = False

    def can_place_tile(self, line_idx: int, color: str) -> bool:
        if len(self.pattern_lines[line_idx]) >= self.pattern_capacity[line_idx]:
            return False
        if self.pattern_lines[line_idx] and self.pattern_lines[line_idx][0] != color:
            return False
        if color in self.wall[line_idx]:
            return False
        return True