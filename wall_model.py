from typing import List, Tuple

wall_pattern = [['blue', 'yellow', 'red', 'green', 'white'],
                ['white', 'blue', 'yellow', 'red', 'green'],
                ['green', 'white', 'blue', 'yellow', 'red'],
                ['red', 'green', 'white', 'blue', 'yellow'],
                ['yellow', 'red', 'green', 'white', 'blue']]

class Wall:
    def __init__(self):
        self.wall = [[None for _ in range(5)] for _ in range(5)]
        self.placed_tiles = []

    def can_place_tiles(self, line_idx: int, color: str) -> bool:
        if color in self.wall[line_idx]:
            return False
        return True

    def place_in_wall(self, line_idx: int, color: str) -> Tuple[int, List[int]]:
        col = wall_pattern[line_idx].index(color)
        self.wall[line_idx][col] = color
        points_added = self.points_for_tile(line_idx, col)
        idx = [line_idx, col]
        self.placed_tiles.append(f'{line_idx}x{col}')
        return points_added

    def points_for_tile(self, row: int, col: int) -> int:
        # +1 for line completion
        gain = 1

        # Point for neighbors
        j = 1
        while col - j >= 0 and self.wall[row][col - j] is not None:
            gain += 1
            j += 1
        j = 1
        while col + j <= 4 and self.wall[row][col + j] is not None:
            gain += 1
            j += 1
        j = 1
        while row - j >= 0 and self.wall[row - j][col] is not None:
            gain += 1
            j += 1
        j = 1
        while row + j <= 4 and self.wall[row + j][col] is not None:
            gain += 1
            j += 1

        return gain

    def endgame_points(self) -> int:
        is_vert_full = [1, 1, 1, 1, 1]  # Points for vertical lines filled
        is_hor_full = [1, 1, 1, 1, 1]  # Points for horizontal lines filled
        is_color_full = [0, 0, 0, 0, 0]  # Points for each plate of one color collected
        gain = 0

        # Checking lines
        for i in range(5):
            if any(self.wall[i][col] is None for col in range(5)):
                # Any place in row 'i' is empty - no points for the row
                is_hor_full[i] = 0
            if any(self.wall[row][i] is None for row in range(5)):
                # any place in column 'i' is empty - no points for the column
                is_vert_full[i] = 0

        # Checking colors
        if self.wall[0][0] is not None and self.wall[1][1] is not None and self.wall[2][2] is not None and \
                self.wall[3][3] is not None and self.wall[4][4] is not None:
            is_color_full[0] = 1
        if self.wall[0][1] is not None and self.wall[1][2] is not None and self.wall[2][3] is not None and \
                self.wall[3][4] is not None and self.wall[4][0] is not None:
            is_color_full[1] = 1
        if self.wall[0][2] is not None and self.wall[1][3] is not None and self.wall[2][4] is not None and \
                self.wall[3][0] is not None and self.wall[4][1] is not None:
            is_color_full[2] = 1
        if self.wall[0][3] is not None and self.wall[1][4] is not None and self.wall[2][0] is not None and \
                self.wall[3][1] is not None and self.wall[4][2] is not None:
            is_color_full[3] = 1
        if self.wall[0][4] is not None and self.wall[1][0] is not None and self.wall[2][1] is not None and \
                self.wall[3][2] is not None and self.wall[4][3] is not None:
            is_color_full[4] = 1

        gain += sum(is_vert_full) * 7  # 7 points for every vertical line filled
        gain += sum(is_hor_full) * 2  # 2 points for every horizontal line filled
        gain += sum(is_color_full) * 10  # 10 points for each color fully collected

        return gain