import random
from sys import exception
from typing import Any, Optional

from azulGame import AzulGame
import logging
import threading

from player_model import AzulPlayer

logger = logging.getLogger(__name__)

class GameAdapter:
    def __init__(self, game: AzulGame, root):
        self.game = game
        self.root = root
        self.views: dict[str, Any] = {}
        self.lock = threading.RLock()


    # Views-------------------------------------------------------------------------------
    def register_view(self, name, view):
        self.views[name] = view

    def update_views(self):
        try:
            state = self.game.get_state()
            self.root.after(0, lambda: self._apply_state(state))
        except Exception:
            logger.exception("Error in update_views")

    def _apply_state(self, state):
        try:
            if state is None:
                return
            board_view = self.views.get('board')
            if board_view:
                board_view.set_state(state, current_player=self.get_current_player())
            if 'players' in state and 'players' in self.views:
                self.views['players'].set_state(state['players'])
        except Exception:
            logger.exception("Error in update_views")

    # Getters-----------------------------------------------------------------------------
    def get_pattern_to_draw(self, player_id: int):
        player = self.game.get_player(player_id)
        pattern = player.pattern_lines.get_state_to_draw()
        return pattern

    def get_floor(self, player_id: int):
        player = self.game.get_player(player_id)
        return player.floor, player.first_tile

    def get_current_player(self) -> int:
        return self.game.current_player

    def get_player_points(self, player_id: int) -> int:
        return self.game.players[player_id].score

    def get_num_players(self) -> int:
        return self.game.num_players

    def get_picked_colors(self):
        return self.game.get_picked_colors()

    def get_placed_tiles(self, player_id: int):
        return self.game.players[player_id].wall.placed_tiles

    # Checkers-----------------------------------------------------------------------------
    def is_first_tile_available(self) -> bool:
        if self.game.first_tile == -1:
            return True
        else:
            return False

    # Widget clicked-----------------------------------------------------------------------
    def factory_clicked(self, factory_id: int, color: str = None):
        board = self.views.get("board")
        if board is None:
            logger.warning("No board registered")
            return
        if color is None:
            return
        with self.lock:
            try:
                factory = None
                if hasattr(board, 'factories_panel'):
                    if 0 <= factory_id < len(board.factories_panel.factories):
                        factory = board.factories_panel.factories[factory_id]
                if factory is None:
                    logger.warning("Factory %s not found", factory_id)
                    return
                factory.highlight_color(color)
                self.game.selection_change(factory_id, color)
                board.factories_panel.unhighlight_colors(factory_id)
                board.center.unhighlight()
            except Exception:
                logger.exception("Error in factory_clicked")

    def center_clicked(self, color: str = None):
        if color is None:
            return
        board = self.views.get("board")
        if board is None:
            logger.warning("No board registered")
            return
        with self.lock:
            try:
                self.game.selection_change(-1, color)
                if hasattr(board, 'center'):
                    board.center.highlight_color(color)
                    board.factories_panel.unhighlight_colors(None)

            except Exception:
                logger.exception("Error in center_clicked")
                return

    def floor_clicked(self):
        board = self.views.get("board")
        if board is None:
            logger.warning("No board registered")
            return

        with self.lock:
            try:
                selection = self.game.get_selection()
                if selection is None:
                    return
                if selection['factory'] == -1:
                    factory = self.game.center
                else:
                    factory = self.game.factories[selection['factory']]
                player = self.game.get_player(self.game.current_player)
                player.extend_floor(selection['count'], selection['color'])

                if selection['factory'] != -1:
                    other = [c for c in factory if c != selection['color']]
                    self.game.add_to_center(other)
                else:
                    # Player gets first_tile, if it's available
                    if self.is_first_tile_available():
                        self.game.first_tile = self.game.current_player
                        self.game.players[self.get_current_player()].first_tile = True

                # Clean factory
                if selection['factory'] != -1:
                    self.game.clean_factory(selection['factory'])
                else:
                    self.game.remove_from_center(selection['color'])

                # Reset selection
                self.game.selection_reset()

                # End of turn
                if self.game.current_player != self.game.get_bot_id():
                    self.game.next_turn()
                    self.bots_turn()

            except Exception:
                logger.exception("Error in pattern_clicked")


    def pattern_clicked(self, line_idx: Optional[int]):
        board = self.views.get("board")
        if board is None:
            logger.warning("No board registered")
            return
        if line_idx is None:
            return
        with self.lock:
            try:
                selection = self.game.get_selection()
                if selection is None:
                    return
                if selection['factory'] == -1:
                    factory = self.game.center
                else:
                    factory = self.game.factories[selection['factory']]
                player = self.game.get_player(self.game.current_player)
                if player.can_place_tiles(line_idx, selection['count'], selection['color']):
                    # Adding plates to player board
                    overflow = player.pattern_lines.place_tiles(line_idx, selection['count'], selection['color'])
                    if overflow != 0:
                        player.extend_floor(overflow, selection['color'])

                    # Adding other plates to center
                    if selection['factory'] != -1:
                        other = [c for c in factory if c != selection['color']]
                        self.game.add_to_center(other)
                    else:
                        # Player gets first_tile, if it's available
                        if self.is_first_tile_available():
                            self.game.first_tile = self.game.current_player
                            self.game.players[self.get_current_player()].first_tile = True

                    # Clean factory
                    if selection['factory'] != -1:
                        self.game.clean_factory(selection['factory'])
                    else:
                        self.game.remove_from_center(selection['color'])

                    # Reset selection
                    self.game.selection_reset()

                    # End of turn
                    if self.game.current_player != self.game.get_bot_id():
                        self.game.next_turn()
                        self.bots_turn()


                else:
                    logger.warning("Invalid move")
                    return

            except Exception:
                logger.exception("Error in pattern_clicked")

    def picked_color(self, color: str):
        # Using PlatePicker to get plates
        board = self.views.get('board')
        self.game.append_picked_colors(color)
        if hasattr(board, 'plate_picker'):
            board.plate_picker.update_preview()
        if len(self.game.get_picked_colors()) == 20:
            board.plate_picker.destroy()
            self.game.set_factories()
            self.start_round()

    def randomize_plates(self):
        board = self.views.get('board')
        colors = ['red', 'green', 'blue', 'yellow', 'white']
        for _ in range(20):
            color = random.choice(colors)
            self.game.append_picked_colors(color)
        board.plate_picker.destroy()
        self.game.set_factories()
        self.start_round()

    # Game flow---------------------------------------------------------------------------
    def start_round(self):
        state = self.game.get_state()
        self._apply_state(state)

        if self.game.current_player == self.game.get_bot_id():
            self.bots_turn()


    def next_turn(self):
        board = self.views.get('board')
        self.game.next_turn()
        board.current_player.player.player_id = self.get_current_player()

        non_current_players = self.game.get_non_current_player_ids()
        for i, player in enumerate(board.players.players):
            player.player_id = non_current_players[i]
        print(board.players.players[0].player_id)
        self.update_views()

        if self.get_current_player() == self.game.get_bot_id():
            self.bots_turn()

        if self.game.is_round_over():
            self.next_round()

    def next_round(self):
        board = self.views.get('board')
        self.game.round_over()

        if self.game.is_game_over():
            self.game_over()
        board.create_plate_picker()

    def game_over(self):
        board = self.views.get('board')
        self.game.game_over()
        board.destroy()

    # Bot--------------------------------------------------------------------------------
    def bots_turn(self):
        if self.game.is_round_over():
            self.next_round()

        move = self.game.players[self.game.get_bot_id()].greedy_ai(self.game.get_state())
        if move['source'] == -1:
            self.center_clicked(move['color'])
        else:
            self.factory_clicked(move['source'], move['color'])

        if move['line'] == -1:
            self.floor_clicked()
        else:
            self.pattern_clicked(move['line'])

        board = self.views.get('board')
        self.game.next_turn()
        board.current_player.player.player_id = self.get_current_player()

        non_current_players = self.game.get_non_current_player_ids()
        for i, player in enumerate(board.players.players):
            player.player_id = non_current_players[i]
        self.update_views()

        if self.game.is_round_over():
            self.next_round()