import tkinter as tk
from tkinter import ttk

class PrzesuwaneObrazy:
    def __init__(self, root):
        self.root = root

        # Utwórz nowe okno z przezroczystym tłem
        self.top = tk.Toplevel(root)
        self.top.wm_attributes("-transparentcolor", "white")

        # Ustaw przezroczystość dla całego okna na 50%
        self.top.attributes("-alpha", 0.5)

        # Utwórz ramkę na przyciski w nowym oknie
        self.panel_przyciskow = ttk.Frame(self.top)
        self.panel_przyciskow.pack()

        # Ustaw kolor tła ramki na niebieski
        self.panel_przyciskow.configure(background='blue')

        # Dodaj przycisk do ramki
        self.przycisk = ttk.Button(self.panel_przyciskow, text="Przycisk")
        self.przycisk.pack()

if __name__ == "__main__":
    root = tk.Tk()
    obrazy = PrzesuwaneObrazy(root)
    root.mainloop()
