from typing import List

from azulGame import AzulGame
from bot import greedy_ai
from scoring import end_round


def input_bag() -> List[str]:
    raw = input("Podaj kolory kafelków w bag (oddzielone spacją):\n")
    bag = raw.strip().split()
    return bag

def display(game: AzulGame) -> None:
    print("Faktorie: ", game.factories)
    print("Centrum: ", game.center)
    for p in game.players:
        print(f"Gracz: {p.id} Wynik: {p.score}\n")
        print("  patterny: ", p.pattern_lines)
        print("  wall: ", p.wall)
        print("  floor: ", p.floor)
        print("-"*30)

def bot_id() -> int:
    id = input("Kolejka bota: \n")
    return int(id)

def player_move(game: AzulGame, player_id: int, source: int, color: str, line: int):
    player = game.players[player_id]

    if source == -1:
        tiles = [t for t in game.center if t == color]
        game.center = [t for t in game.center if t != color]
        if game.first_tile == -1:
            player.floor.extend("-")
            game.first_tile = player_id
    else:
        factory = game.factories[source]
        tiles = [t for t in factory if t == color]
        remaining = [t for t in factory if t != color]
        game.factories[source] = []
        game.center.extend(remaining)

    if player.can_place_tile(line, color):
        space_left = player.pattern_capacity[line] - len(player.pattern_lines[line])
        to_place = tiles[:space_left]
        overflow = tiles[space_left:]
        player.pattern_lines[line].extend(to_place)
        player.floor.extend(overflow)
    else:
        player.floor.extend(tiles)

def main(bot_ai=greedy_ai):
    game = AzulGame(num_players=2)
    bot = bot_id()
    while True:
        bag = input_bag()
        bag.reverse()
        game.deal_tiles(bag)
        # TODO: Wybór miejsce w kolejce bota,
        # TODO: Realistyczne kolory na planszy graczy:
        # b y r g w
        # w b y r g
        # g w b y r
        # r g w b y
        # y r g w b
        # TODO: wybór floor
        # TODO: kafelek -1
        # TODO: punkty dodatnie za sąsiedztwo
        # TODO: punkty ujemne za kafelek -1, floor

        while not game.is_round_over():
            display(game)
            player = game.players[game.current_player]

            if bot_ai and player.id == bot:
                move = bot_ai(player, game.factories, game.center)
                player_move(
                    game, player.id, move["source"], move["color"], move["line"]
                )
                print(
                    f"Ruch kompa: source: {move['source']}, kolor: {move['color']}, linia: {move['line']}"
                )
            else:
                # ruch gracza
                print(
                    f"Ruch gracza {player.id}, dostępne fabryki: {game.factories}, center: {game.center}"
                )
                src = int(input("Fabryka (-1 dla center): "))
                col = input("Kolor: ")
                line = int(input("Linia (0-4): "))
                player_move(game, player.id, src, col, line)
            game.next_turn()
        for p in game.players:
            end_round(p)
        #if any(all(cell is not None for cell in row) for p in game.players for row in p.wall):
        #    break
        if game.is_game_over():

            break
    winner = max(game.players, key=lambda p: p.score)
    print(winner)