import tkinter as tk
import sys, os
from tkinter import font
from menu import PrzesuwaneObrazy
from gra import gra


class FullscreenApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Armata")
        self.master.attributes('-fullscreen', True)


class CustomButton(tk.Button):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        self.configure(
            font=("Microsoft Yi Baiti", 15, "bold"),
            relief="flat",
            activebackground="#404040",
            borderwidth=0,
            bg="#404040",
            fg="white",
            width=4
        )


class CustomTitleBarApp:
    def __init__(self, master):
        self.master = master

        # Ścieżka do arma.png z _MEIPASS:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        arma_png_path = os.path.join(base_path, "resources", "icons", "arma.png")
        self.icon_image = tk.PhotoImage(file=arma_png_path)
        self.master.iconphoto(True, self.icon_image)

        segoe_ui_font = font.Font(family="Segoe UI", size=12)
        self.master.option_add("*Font", segoe_ui_font)

        # Dodanie tła do paska tytułowego
        self.title_bar = tk.Frame(self.master, bg="#404040", relief="raised", bd=0)
        self.title_bar.pack(fill="x", side="top", anchor="w")

        close_button = CustomButton(self.title_bar, text="X", command=self.on_close)
        close_button.pack(side="right", padx=0, pady=0)
        close_button.bind("<Enter>", self.on_enter_close)
        close_button.bind("<Leave>", self.on_leave_close)

        minimize_button = CustomButton(self.title_bar, text="_", command=self.minimize_window)
        minimize_button.pack(side="right", padx=0, pady=0)
        minimize_button.bind("<Enter>", self.on_enter_minimize)
        minimize_button.bind("<Leave>", self.on_leave_minimize)

        icon_label = tk.Label(self.title_bar, image=self.icon_image, bg="#404040")
        icon_label.pack(side="left", padx=0, pady=0)

        title_label = tk.Label(self.title_bar, text="Armata", bg="#404040", fg="#5E9494",
                               font=(segoe_ui_font.actual("family"), segoe_ui_font.actual("size"), "bold"))
        title_label.pack(side="left", padx=0, pady=0)

    def on_enter_close(self, event):
        event.widget.configure(bg="#C40000")

    def on_leave_close(self, event):
        event.widget.configure(bg="#404040")

    def on_enter_minimize(self, event):
        event.widget.configure(bg="#6B6B6B")

    def on_leave_minimize(self, event):
        event.widget.configure(bg="#404040")

    def minimize_window(self):
        self.master.iconify()

    def on_close(self):
        self.master.destroy()


root = tk.Tk()
root.configure(bg="black")

# Ponownie sprawdzamy _MEIPASS:
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)


backgrounds_path = os.path.join(base_path, "resources", "backgrounds")

sciezka_do_obrazu1 = os.path.join(backgrounds_path, "pt0.png")
sciezka_do_obrazu2 = os.path.join(backgrounds_path, "pt1.png")
sciezka_do_obrazu3 = os.path.join(backgrounds_path, "pt2.png")
sciezka_do_obrazu4 = os.path.join(backgrounds_path, "o_grze.png")
sciezka_do_obrazu5 = os.path.join(backgrounds_path, "tlo_gry.png")
sciezka_do_obrazu6 = os.path.join(backgrounds_path, "red.png")
sciezka_do_obrazu7 = os.path.join(backgrounds_path, "blue.png")

sciezka_do_dzwieku1 = os.path.join(backgrounds_path, "pt0.wav")
sciezka_do_dzwieku2 = os.path.join(backgrounds_path, "pt1.wav")
sciezka_do_dzwieku3 = os.path.join(backgrounds_path, "pt2.wav")
sciezka_do_dzwieku4 = os.path.join(backgrounds_path, "zamk.wav")
sciezka_do_dzwieku5 = os.path.join(backgrounds_path, "wjazd.wav")

obrazy = PrzesuwaneObrazy(
    root,
    sciezka_do_obrazu1,
    sciezka_do_obrazu2,
    sciezka_do_obrazu3,
    sciezka_do_obrazu4,
    sciezka_do_obrazu5,
    sciezka_do_obrazu6,
    sciezka_do_obrazu7,
    sciezka_do_dzwieku1,
    sciezka_do_dzwieku2,
    sciezka_do_dzwieku3,
    sciezka_do_dzwieku4,
    sciezka_do_dzwieku5
)

app = CustomTitleBarApp(root)
app_fullscreen = FullscreenApp(root)
root.mainloop()
