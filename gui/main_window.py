import tkinter as tk
from PIL import Image, ImageTk

from gui.board_widget import BoardWidget

def main():
    root = tk.Tk()
    root.title("Azul")
    root.geometry("660x600+200+200")
    root.resizable(True, True)

    ico = Image.open("icons/ikonka.jpg")
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    board = BoardWidget(root)
    board.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()