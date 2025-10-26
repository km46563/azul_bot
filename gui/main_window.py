import tkinter as tk
from PIL import Image, ImageTk

from adapters import GameAdapter
from azulGame import AzulGame
from gui.board_widget import BoardWidget


def main():
    root = tk.Tk()
    root.title("Azul")
    root.geometry("660x800+200+200")
    root.resizable(True, True)
    ico = Image.open("icons/ikonka.jpg")
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    game = AzulGame(2)
    adapter = GameAdapter(game, root)
    board = BoardWidget(root, adapter)
    adapter.register_view("board", board)
    board.pack(fill=tk.BOTH, expand=True)


    adapter.update_views()

    root.mainloop()


if __name__ == "__main__":
    main()
