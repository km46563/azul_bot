from player import AzulPlayer

wall = [['b', 'y', 'r', 'g', 'w'],
        ['w', 'b', 'y', 'r', 'g'],
        ['g', 'w', 'b', 'y', 'r'],
        ['r', 'g', 'w', 'b', 'y'],
        ['y', 'r', 'g', 'w', 'b']]
floor = [-1, -1, -2, -2, -2, -3, -3]

# Koniec rundy - posprzątaj, przydziel punkty
def end_round(player: AzulPlayer) -> None:
    gain = 0
    for i, line in enumerate(player.pattern_lines):
        if len(line) == player.pattern_capacity[i]:
            color = line[0]
            col = wall[i].index(color)
            player.wall[i][col] = color
            player.pattern_lines[i] = []

            # Punkt za ułożony kafelek
            gain += 1

            # Punkty za sąsiadujące kafelki
            j = 1
            while col - j >= 0 and player.wall[i][col - j] is not None:
                gain += 1
                j += 1
            j = 1
            while col + j <= 4 and player.wall[i][col + j] is not None:
                gain += 1
                j += 1
            j = 1
            while i - j >= 0 and player.wall[i - j][col] is not None:
                gain += 1
                j += 1
            j = 1
            while i + j <= 4 and player.wall[i + j][col] is not None:
                gain += 1
                j += 1
    player.score += gain


    #Punkty ujemne za podłogę
    for i in range(len(player.floor)):
        player.score += floor[i % len(floor)]

    player.floor = []

def end_game(player: AzulPlayer) -> None:
    is_vert_full = [1, 1, 1, 1, 1]  # Punkty za pełną linię pionową
    is_hor_full = [1, 1, 1, 1, 1]   # Punkty za pełną linię poziomą
    is_color_full = [0, 0, 0, 0, 0] # Punkty za wszystkie kafelki jednego koloru
    gain = 0

    for i in range(5):
        if any(player.wall[i][col] is None for col in range(5)):
            # Którekolwiek miejsce w rzędzie 'i' jest puste - brak punktów za ten rząd
            is_hor_full[i] = 0
        if any(player.wall[row][i] is None for row in range(5)):
            # Którekolwiek miejsce w kolumnie 'i' jest puste - brak punktów za tę kolumnę
            is_vert_full[i] = 0

    # Sprawdzanie kolorów
    if player.wall[0][0] is not None and player.wall[1][1] is not None and player.wall[2][2] is not None and player.wall[3][3] is not None and player.wall[4][4] is not None:
        is_color_full[0] = 1
    if player.wall[0][1] is not None and player.wall[1][2] is not None and player.wall[2][3] is not None and player.wall[3][4] is not None and player.wall[4][0] is not None:
        is_color_full[1] = 1
    if player.wall[0][2] is not None and player.wall[1][3] is not None and player.wall[2][4] is not None and player.wall[3][0] is not None and player.wall[4][1] is not None:
        is_color_full[2] = 1
    if player.wall[0][3] is not None and player.wall[1][4] is not None and player.wall[2][0] is not None and player.wall[3][1] is not None and player.wall[4][2] is not None:
        is_color_full[3] = 1
    if player.wall[0][4] is not None and player.wall[1][0] is not None and player.wall[2][1] is not None and player.wall[3][2] is not None and player.wall[4][3] is not None:
        is_color_full[4] = 1

    gain += sum(is_vert_full) * 7   # 7 punktów za każdą ułożoną linię pionową
    gain += sum(is_hor_full) * 2    # 2 punkty za każdą ułożoną linię poziomą
    gain += sum(is_color_full) * 10 # 10 punktów za zebrany pełny kolor

    player.score += gain