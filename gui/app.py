import tkinter as tk

from gui.main_window import SpellDeckMainWindow


def main():
    root = tk.Tk()
    root.title("D&D Spelldeck - Magie")
    root.minsize(760, 520)
    SpellDeckMainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

