import tkinter as tk
from PIL import Image, ImageTk

from adapters import GameAdapter
from azulGame import AzulGame
from gui.board_widget import BoardWidget
from gui.menu import Menu


def main():
    root = tk.Tk()
    dlg = Menu(root)
    dlg.wait_window(dlg)
    root.withdraw()
    config = dlg.result

    if config is None:
        root.destroy()
        return

    root.deiconify()
    root.title("Azul")
    root.geometry("660x800+200+200")
    root.resizable(True, True)
    ico = Image.open("gui/icons/ikonka.jpg")
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    num_players = config["num_players"]
    bots_turn = config["turn"]
    plate_picker_mode = config["plate_picker_mode"]

    game = AzulGame(num_players, bots_turn)
    adapter = GameAdapter(game, root)
    board = BoardWidget(root, adapter, plate_picker_mode)
    adapter.register_view("board", board)
    board.pack(fill=tk.BOTH, expand=True)


    adapter.update_views()

    root.mainloop()


if __name__ == "__main__":
    main()
