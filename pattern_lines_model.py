class PatternLines:
    def __init__(self):
        self.pattern_lines = [[] for _ in range(5)]
        self.pattern_capacity = [i + 1 for i in range(5)]

    def get_state(self):
        return {'pattern_lines': self.pattern_lines,
                'pattern_capacity': self.pattern_capacity}

    def get_color(self, line_idx):
        return self.pattern_lines[line_idx][0]

    # Function is returning a list of colors to help the pattern line widget draw the tiles
    # List includes colors of existing tiles, or 'bisque': that color indicates that there is no tile in this place
    def get_state_to_draw(self):
        all_colors = []
        for i in range(5):
            colors = []
            for j in range(i + 1):
                if len(self.pattern_lines[i]) > j:
                    colors.append(self.pattern_lines[i][j])
                else:
                    colors.append('bisque')
            all_colors.append(colors)
        return all_colors

    def can_place_tiles(self, line_idx: int, count: int, color: str) -> bool:
        if self.is_line_full(line_idx):
            print("pattern line is already full")
            return False
        if self.pattern_lines[line_idx] and self.pattern_lines[line_idx][0] != color:
            print("pattern line has different color")
            return False
        return True

    def is_line_full(self, line_idx: int) -> bool:
        if self.pattern_capacity[line_idx] == 0:
            return True
        return False

    def place_tiles(self, line_idx: int, count: int, color: str):
        if (self.pattern_capacity[line_idx] - count) < 0:
            overflow = abs(self.pattern_capacity[line_idx] - count)
            tiles = [color for _ in range(self.pattern_capacity[line_idx])]
            self.pattern_lines[line_idx].extend(tiles)
            self.pattern_capacity[line_idx] = 0
            return overflow
        else:
            tiles = [color for _ in range(count)]
            self.pattern_lines[line_idx].extend(tiles)
            self.pattern_capacity[line_idx] = self.pattern_capacity[line_idx] - count
            return 0

    # When line is full, clear the pattern line and set its capacity to max value
    def pop_full_lines(self):
        is_full = []
        colors = []
        for i in range(5):
            if self.is_line_full(i):
                is_full.append(True)
                colors.append(self.pattern_lines[i][0])
                self.pattern_lines[i] = []
                self.pattern_capacity[i] = i + 1
            else:
                is_full.append(False)
                colors.append(None)
        return is_full, colors
