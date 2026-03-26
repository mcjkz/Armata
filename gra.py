import tkinter as tk
import sys, os
from PIL import Image, ImageTk
import pygame
import random
# import unittest

class gra:

    def __init__(self, root, callback, powrot_do_menu):
        self.root = root

        # Ustawiamy base_path w zależności od tego, czy skrypt jest spakowany:
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS  # folder tymczasowy, gdzie PyInstaller trzyma pliki
        else:
            self.base_path = os.path.dirname(__file__)

        icons_path = os.path.join(self.base_path, "resources", "icons")

        screen_width = self.root.winfo_screenwidth()
        sk = screen_width // 1920
        self.pk = 0
        self.poziom = 0
        self.ktore_menu = 0
        self.czyszczenie = 0
        self.czcionka_ramki = ("Stem-Medium", 24 * sk)
        self.root.attributes("-fullscreen", True)
        self.callback = callback
        self.powrot_do_menu = powrot_do_menu
        self.ilosc_kart = 0
        self.powrot_klik = 0
        self.liczymy_karty = []

        # Ścieżki do plików graficznych
        self.komp_png_path = os.path.join(icons_path, "komp.png")
        self.dwie_os_png_path = os.path.join(icons_path, "dwie_os.png")
        self.komp_red_png_path = os.path.join(icons_path, "komp-red.png")

        # Rozpocznij od menu_komp
        self.menu_komp()

    def menu_komp(self):
        screen_width = self.root.winfo_screenwidth()
        sk = screen_width / 1920
        self.pozycja_gracz1 = 0
        self.pozycja_gracz2 = 0
        self.rozgrywka = 0
        self.dane_graczy = {
            "gracz1": {"nazwa": "", "ilosc_punktow": 0},
            "gracz2": {"nazwa": "", "ilosc_punktow": 0}
        }
        screen_height = self.root.winfo_screenheight()
        a = int(0.32 * screen_width)
        b = int(0.25 * screen_height)

        self.panel_rozgr = tk.Frame(self.root, width=0, height=0, bg="#6B0000", bd=0, relief=tk.SOLID)
        self.panel_rozgr.place(x=a, y=b)

        label_gracz1 = tk.Label(
            self.panel_rozgr,
            text="Wybierz rozgrywkę:",
            bg="#6B0000",
            fg="white",
            font=self.czcionka_ramki
        )
        label_gracz1.grid(row=0, column=0, columnspan=3, padx=200 * sk, pady=(50 * sk, 30 * sk), sticky="ew", ipady=5)

        # Wczytujemy obrazki przy pomocy Pillow i os.path.join
        icon_komp_img = Image.open(self.komp_png_path)
        x1, y1 = icon_komp_img.size
        icon_komp_img = icon_komp_img.resize((int(x1 * sk), int(y1 * sk)))
        icon_komp = ImageTk.PhotoImage(icon_komp_img)

        icon_dwuosob_img = Image.open(self.dwie_os_png_path)
        x2, y2 = icon_dwuosob_img.size
        icon_dwuosob_img = icon_dwuosob_img.resize((int(x2 * sk), int(y2 * sk)))
        icon_dwuosob = ImageTk.PhotoImage(icon_dwuosob_img)

        przycisk_rozp = tk.Button(
            self.panel_rozgr,
            text="  Komputer  ",
            image=icon_komp,
            compound=tk.LEFT,
            command=self.menu_gl2,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0,
            padx=20 * sk
        )
        przycisk_rozp.image = icon_komp
        przycisk_rozp.grid(row=1, column=1, pady=(20 * sk, 30 * sk), padx=200 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_rozp = tk.Button(
            self.panel_rozgr,
            text="Dwuosobowa",
            image=icon_dwuosob,
            compound=tk.LEFT,
            command=self.menu_gl,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0,
            padx=15 * sk
        )
        przycisk_rozp.image = icon_dwuosob
        przycisk_rozp.grid(row=2, column=1, pady=(30 * sk, 40 * sk), padx=200 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_dol = tk.Button(
            self.panel_rozgr,
            text="  Powrót  ",
            command=self.powrot2,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_dol.grid(row=3, column=1, pady=(40 * sk, 80 * sk))
        przycisk_dol.bind("<Enter>", lambda event, button=przycisk_dol: button.config(bg="#B70000"))
        przycisk_dol.bind("<Leave>", lambda event, button=przycisk_dol: button.config(bg="#330000"))

        self.ukryj_ile_kart()
        self.tablica_wynikow()

    def menu_gl(self):
        self.ktore_menu = 1
        self.ukryj_panel_rozgr()
        screen_width = self.root.winfo_screenwidth()
        sk = screen_width / 1920
        screen_height = self.root.winfo_screenheight()
        a = int(0.33 * screen_width)
        b = int(0.2 * screen_height)

        test_png = os.path.join(self.base_path, "resources", "icons", "test.png")
        self.transparent_image = tk.PhotoImage(file=test_png)

        self.panel_przyciskow = tk.Frame(self.root, width=0, height=0, bg="#6B0000", relief=tk.SOLID)
        self.panel_przyciskow.place(x=a, y=b)

        def remove_entry_focus(event):
            self.root.focus_set()
            self.label_sprobuj_ponownie.grid_remove()
            self.label_sprobuj_ponownie2.grid_remove()
            self.g_line1.grid_remove()

        self.panel_przyciskow.bind("<Button-1>", remove_entry_focus)

        self.label_sprobuj_ponownie2 = tk.Label(
            self.panel_przyciskow,
            text="WPROWADZONA NAZWA PRZEKRACZA 20 ZNAKÓW",
            bg="#330000",
            fg="#FF2600",
            font=("Stem-Bold", int(16 * sk))
        )
        self.label_sprobuj_ponownie2.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=12)
        self.label_sprobuj_ponownie2.grid_remove()

        self.label_sprobuj_ponownie = tk.Label(
            self.panel_przyciskow,
            text="WPROWADZONO NIEPOPRAWNĄ NAZWĘ UŻYTKOWNIKA",
            bg="#330000",
            fg="#FF2600",
            font=("Stem-Bold", int(16 * sk))
        )
        self.label_sprobuj_ponownie.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=12)

        self.g_line1 = tk.Frame(self.panel_przyciskow, bg="#FF2600", height=4)
        self.g_line1.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.label_sprobuj_ponownie.grid_remove()
        self.g_line1.grid_remove()

        label_gracz1 = tk.Label(
            self.panel_przyciskow,
            text="Podaj nazwę użytkownika Gracza 1:",
            bg="#6B0000",
            fg="white",
            font=self.czcionka_ramki
        )
        label_gracz1.grid(row=2, column=0, pady=(30 * sk, 15 * sk), padx=60 * sk)

        self.entry_gracz1 = tk.Entry(
            self.panel_przyciskow,
            font=self.czcionka_ramki,
            bg="#330000",
            fg="red",
            highlightbackground="#330000",
            highlightcolor="red",
            highlightthickness=3,
            borderwidth=0,
            insertbackground="white"
        )
        self.entry_gracz1.grid(row=3, column=0, pady=(15 * sk, 35 * sk), padx=60 * sk, ipady=2)

        label_gracz2 = tk.Label(
            self.panel_przyciskow,
            text="Podaj nazwę użytkownika Gracza 2:",
            bg="#6B0000",
            fg="white",
            font=self.czcionka_ramki
        )
        label_gracz2.grid(row=4, column=0, pady=(35 * sk, 15 * sk), padx=60 * sk)

        self.entry_gracz2 = tk.Entry(
            self.panel_przyciskow,
            font=self.czcionka_ramki,
            bg="#330000",
            fg="#0059FF",
            highlightbackground="#330000",
            highlightcolor="#0059FF",
            highlightthickness=3,
            borderwidth=0,
            insertbackground="white"
        )
        self.entry_gracz2.grid(row=5, column=0, pady=(15 * sk, 30 * sk), padx=60 * sk, ipady=2)

        przycisk_dol = tk.Button(
            self.panel_przyciskow,
            text="  Powrót  ",
            command=self.powrot4,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_dol.grid(row=6, column=0, pady=(30 * sk, 20 * sk))
        przycisk_dol.bind("<Enter>", lambda event, button=przycisk_dol: button.config(bg="#B70000"))
        przycisk_dol.bind("<Leave>", lambda event, button=przycisk_dol: button.config(bg="#330000"))

        przycisk_dol = tk.Button(
            self.panel_przyciskow,
            text="    Dalej    ",
            command=self.dalej,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_dol.grid(row=7, column=0, pady=(30 * sk, 60 * sk))
        przycisk_dol.bind("<Enter>", lambda event, button=przycisk_dol: button.config(bg="#B70000"))
        przycisk_dol.bind("<Leave>", lambda event, button=przycisk_dol: button.config(bg="#330000"))

        self.ukryj_ile_kart()

    # ---------------- MENU GLOWNE 2 ----------------
    def menu_gl2(self):
        self.ktore_menu = 2
        self.ukryj_panel_rozgr()
        screen_width = self.root.winfo_screenwidth()
        sk = screen_width / 1920
        screen_height = self.root.winfo_screenheight()
        a = int(0.34 * screen_width)
        b = int(0.22 * screen_height)

        test_png = os.path.join(self.base_path, "resources", "icons", "test.png")
        self.transparent_image = tk.PhotoImage(file=test_png)

        self.panel_przyciskow = tk.Frame(self.root, width=0, height=0, bg="#6B0000", relief=tk.SOLID)
        self.panel_przyciskow.place(x=a, y=b)

        def remove_entry_focus(event):
            self.root.focus_set()
            self.label_sprobuj_ponownie.grid_remove()
            self.label_sprobuj_ponownie2.grid_remove()
            self.g_line1.grid_remove()

        self.panel_przyciskow.bind("<Button-1>", remove_entry_focus)

        self.label_sprobuj_ponownie2 = tk.Label(
            self.panel_przyciskow,
            text="WPROWADZONA NAZWA PRZEKRACZA 20 ZNAKÓW",
            bg="#330000",
            fg="#FF2600",
            font=("Stem-Bold", int(16 * sk))
        )
        self.label_sprobuj_ponownie2.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=12)
        self.label_sprobuj_ponownie2.grid_remove()

        self.label_sprobuj_ponownie = tk.Label(
            self.panel_przyciskow,
            text="WPROWADZONO NIEPOPRAWNĄ NAZWĘ UŻYTKOWNIKA",
            bg="#330000",
            fg="#FF2600",
            font=("Stem-Bold", int(16 * sk))
        )
        self.label_sprobuj_ponownie.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=12)

        self.g_line1 = tk.Frame(self.panel_przyciskow, bg="#FF2600", height=4)
        self.g_line1.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.label_sprobuj_ponownie.grid_remove()
        self.g_line1.grid_remove()

        label_gracz1 = tk.Label(
            self.panel_przyciskow,
            text="Poziom trudności Komputera:",
            bg="#6B0000",
            fg="white",
            font=self.czcionka_ramki
        )
        label_gracz1.grid(row=2, column=0, columnspan=3, pady=(40 * sk, 0), padx=120 * sk)

        self.latwy = tk.Button(
            self.panel_przyciskow,
            text="ŁATWY",
            font=("Stem-Bold", int(18 * sk)),
            relief=tk.FLAT,
            bg="#330000",
            fg="#D3D3D3",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        self.latwy.grid(row=3, column=0, pady=(30 * sk, 0), padx=(120 * sk, 0), sticky="we")
        self.linia1 = tk.Frame(self.panel_przyciskow, bg="#330000", height=3)
        self.linia1.grid(row=4, column=0, sticky="ew", padx=(120 * sk, 0))

        self.latwy.bind("<Enter>", lambda event, button=self.latwy, line=self.linia1:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#B70000", line))
        self.latwy.bind("<Leave>", lambda event, button=self.latwy, line=self.linia1:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))
        self.latwy.bind("<Button-1>", lambda event: self.przycisk("Łatwy"))

        self.sredni = tk.Button(
            self.panel_przyciskow,
            text="ŚREDNI",
            font=("Stem-Bold", int(18 * sk)),
            relief=tk.FLAT,
            bg="#330000",
            fg="#D3D3D3",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        self.sredni.grid(row=3, column=1, pady=(30 * sk, 0), sticky="ew")
        self.linia2 = tk.Frame(self.panel_przyciskow, bg="#330000", height=3)
        self.linia2.grid(row=4, column=1, sticky="ew")

        self.sredni.bind("<Enter>", lambda event, button=self.sredni, line=self.linia2:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#B70000", line))
        self.sredni.bind("<Leave>", lambda event, button=self.sredni, line=self.linia2:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))
        self.sredni.bind("<Button-1>", lambda event: self.przycisk("Średni"))

        self.trudny = tk.Button(
            self.panel_przyciskow,
            text="TRUDNY",
            font=("Stem-Bold", int(18 * sk)),
            relief=tk.FLAT,
            bg="#330000",
            fg="#D3D3D3",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        self.trudny.grid(row=3, column=2, pady=(30 * sk, 0), padx=(0, 120 * sk), sticky="we")
        self.linia3 = tk.Frame(self.panel_przyciskow, bg="#330000", height=3)
        self.linia3.grid(row=4, column=2, sticky="ew", padx=(0, 120 * sk))
        self.trudny.bind("<Enter>", lambda event, button=self.trudny, line=self.linia3:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#B70000", line))
        self.trudny.bind("<Leave>", lambda event, button=self.trudny, line=self.linia3:
                                      self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))
        self.trudny.bind("<Button-1>", lambda event: self.przycisk("Trudny"))

        label_gracz2 = tk.Label(
            self.panel_przyciskow,
            text="Podaj nazwę użytkownika:",
            bg="#6B0000",
            fg="white",
            font=self.czcionka_ramki
        )
        label_gracz2.grid(row=5, column=0, columnspan=3, pady=(80 * sk, 0), sticky="ew")

        self.entry_gracz2 = tk.Entry(
            self.panel_przyciskow,
            font=self.czcionka_ramki,
            bg="#330000",
            fg="#0059FF",
            highlightbackground="#330000",
            highlightcolor="#0059FF",
            highlightthickness=3,
            borderwidth=0,
            insertbackground="white"
        )
        self.entry_gracz2.grid(row=6, column=0, columnspan=3, pady=(30 * sk, 60 * sk), padx=50 * sk)

        przycisk_dol = tk.Button(
            self.panel_przyciskow,
            text="  Powrót  ",
            command=self.powrot4,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_dol.grid(row=7, column=0, columnspan=2, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_dol.bind("<Enter>", lambda event, button=przycisk_dol: button.config(bg="#B70000"))
        przycisk_dol.bind("<Leave>", lambda event, button=przycisk_dol: button.config(bg="#330000"))

        przycisk_dol = tk.Button(
            self.panel_przyciskow,
            text="    Dalej    ",
            command=self.dalej,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_dol.grid(row=7, column=1, columnspan=3, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_dol.bind("<Enter>", lambda event, button=przycisk_dol: button.config(bg="#B70000"))
        przycisk_dol.bind("<Leave>", lambda event, button=przycisk_dol: button.config(bg="#330000"))

        self.ukryj_ile_kart()
        self.przycisk("Średni")

    def zmien_kolor_przycisku_i_linii(self, event, button, color, line):
        line.config(bg=color)
        if color != "white":
            color = "#939393"
        button.config(fg=color)

    def przycisk(self, poziom):
        self.poziom = poziom
        if self.poziom == "Łatwy":
            self.latwy.config(bg="#330000", disabledforeground="#4AF700", state="disabled")
            self.linia1.config(bg="#4AF700")
            self.latwy.bind("<Enter>", lambda event, button=self.latwy: button.config(bg="#330000"))
            self.latwy.bind("<Leave>", lambda event, button=self.latwy: button.config(bg="#330000"))

            self.sredni.config(fg="#939393", state="normal")
            self.linia2.config(bg="#330000")
            self.sredni.bind("<Enter>", lambda event, button=self.sredni, line=self.linia2:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.sredni.bind("<Leave>", lambda event, button=self.sredni, line=self.linia2:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

            self.trudny.config(fg="#939393", state="normal")
            self.linia3.config(bg="#330000")
            self.trudny.bind("<Enter>", lambda event, button=self.trudny, line=self.linia3:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.trudny.bind("<Leave>", lambda event, button=self.trudny, line=self.linia3:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

        elif self.poziom == "Średni":
            self.latwy.config(fg="#939393", state="normal")
            self.linia1.config(bg="#330000")
            self.latwy.bind("<Enter>", lambda event, button=self.latwy, line=self.linia1:
                                          self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.latwy.bind("<Leave>", lambda event, button=self.latwy, line=self.linia1:
                                          self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

            self.sredni.config(bg="#330000", disabledforeground="#FFBB00", state="disabled")
            self.linia2.config(bg="#FFBB00")
            self.sredni.bind("<Enter>", lambda event, button=self.sredni: button.config(bg="#330000"))
            self.sredni.bind("<Leave>", lambda event, button=self.sredni: button.config(bg="#330000"))

            self.trudny.config(fg="#939393", state="normal")
            self.linia3.config(bg="#330000")
            self.trudny.bind("<Enter>", lambda event, button=self.trudny, line=self.linia3:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.trudny.bind("<Leave>", lambda event, button=self.trudny, line=self.linia3:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

        else:  # self.poziom == "Trudny"
            self.latwy.config(fg="#939393", state="normal")
            self.linia1.config(bg="#330000")
            self.latwy.bind("<Enter>", lambda event, button=self.latwy, line=self.linia1:
                                          self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.latwy.bind("<Leave>", lambda event, button=self.latwy, line=self.linia1:
                                          self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

            self.sredni.config(fg="#939393", state="normal")
            self.linia2.config(bg="#330000")
            self.sredni.bind("<Enter>", lambda event, button=self.sredni, line=self.linia2:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "white", line))
            self.sredni.bind("<Leave>", lambda event, button=self.sredni, line=self.linia2:
                                           self.zmien_kolor_przycisku_i_linii(event, button, "#330000", line))

            self.trudny.config(bg="#330000", disabledforeground="#FF2600", state="disabled")
            self.linia3.config(bg="#FF2600")
            self.trudny.bind("<Enter>", lambda event, button=self.trudny: button.config(bg="#330000"))
            self.trudny.bind("<Leave>", lambda event, button=self.trudny: button.config(bg="#330000"))

    def tablica_wynikow(self):
        ilosc_stron = 0
        screen_width = self.root.winfo_screenwidth()
        sk = screen_width / 1920
        if sk == 1:
            mn = 1
        elif sk > 1:
            mn = 2
        else:
            mn = 0.5

        screen_height = self.root.winfo_screenheight()

        tabela_x = int(0.01 * screen_width)
        tabela_y = int(0.05 * screen_height)

        self.panel_tabela = tk.Frame(
            self.root,
            width=0 * sk,
            height=0 * sk,
            bg="#6B0000",
            bd=0,
            relief=tk.SOLID
        )
        self.panel_tabela.place(x=tabela_x, y=tabela_y)

        naglowki = ["Pozycja", "Gracz", "Pkt"]
        button = tk.Button(
            self.panel_tabela,
            text="▶",
            relief=tk.FLAT,
            bg="#330000",
            fg="#FFBB00",
            activebackground="#FFBB00",
            activeforeground="#330000",
            borderwidth=0,
            font=("Stem-Bold", int(16 * sk), "bold"),
            state=tk.DISABLED,
            disabledforeground="#330000"
        )
        button.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="ew", ipady=0)

        label_naglowek = tk.Button(
            self.panel_tabela,
            text="Ściana chwały",
            relief=tk.FLAT,
            bg="#330000",
            fg="#FFBB00",
            activebackground="#B70000",
            activeforeground="#FFBB00",
            pady=0,
            borderwidth=0,
            font=("Stem-Bold", int(16 * sk), "bold"),
            state=tk.DISABLED,
            disabledforeground="#FFBB00"
        )
        label_naglowek.grid(row=0, column=1, padx=0, pady=(0, 0), sticky="ew", ipady=0)

        button = tk.Button(
            self.panel_tabela,
            text="▶",
            relief=tk.FLAT,
            bg="#330000",
            fg="#FFBB00",
            activebackground="#FFBB00",
            activeforeground="#330000",
            borderwidth=0,
            font=("Stem-Bold", int(16 * sk), "bold")
        )
        button.bind("<Enter>", lambda event, button=button: button.config(bg="#FFBB00", fg="#330000"))
        button.bind("<Leave>", lambda event, button=button: button.config(bg="#330000", fg="#FFBB00"))
        button.grid(row=0, column=2, padx=0, pady=(0, 0), sticky="ew", ipady=0)

        red_line = tk.Frame(self.panel_tabela, bg="#FFBB00", height=3)
        red_line.grid(row=1, column=0, columnspan=len(naglowki), sticky="ew")

        for i, naglowek in enumerate(naglowki):
            label_naglowek = tk.Label(
                self.panel_tabela,
                text=naglowek,
                bg="#330000",
                fg="white",
                font=("Stem-Medium", int(15 * sk))
            )
            label_naglowek.grid(row=2, column=i, padx=0, pady=(0, 5 * sk), sticky="ew")

        self.panel_tabela.grid_columnconfigure(0, uniform="same_width")
        self.panel_tabela.grid_columnconfigure(2, uniform="same_width")
        self.panel_tabela.grid_columnconfigure(1, minsize=210 * sk)

        with open("dane_graczy.txt", "a") as plik:
            pass
        with open("dane_graczy.txt", "r") as plik:
            linie = plik.readlines()

        ilosc_linii = len(linie) // 2

        self.gracze = []
        for i in range(0, len(linie), 2):
            nazwa_gracza = linie[i].strip()
            ilosc_punktow = self.pobierz_ilosc_punktow(nazwa_gracza)
            krotka_gracza = (nazwa_gracza, ilosc_punktow)
            self.gracze.append(krotka_gracza)

        self.sortowanie_babelkowe()
        for i in range(len(self.gracze)):
            if self.gracze[i][0] == self.dane_graczy["gracz1"]["nazwa"]:
                self.pozycja_gracz1 = i + 1
            elif self.gracze[i][0] == self.dane_graczy["gracz2"]["nazwa"]:
                self.pozycja_gracz2 = i + 1

        for i in range(0 + self.pk, 25 + self.pk):
            if i < len(self.gracze):
                nazwa_gracza, ilosc_punktow = self.gracze[i]
            akt_poz = i

            if i < len(self.gracze):
                if nazwa_gracza == self.dane_graczy["gracz1"]["nazwa"]:
                    self.kolor = "#FF002C"
                    self.czcionka_arial = ("Roboto", int(13 * sk), "bold")
                    if self.pozycja_gracz1 == 0:
                        self.pozycja_gracz1 = i + 1
                elif nazwa_gracza == self.dane_graczy["gracz2"]["nazwa"]:
                    self.kolor = "#00D8FF"
                    self.czcionka_arial = ("Roboto", int(13 * sk), "bold")
                    if self.pozycja_gracz2 == 0:
                        self.pozycja_gracz2 = i + 1
                else:
                    self.kolor = "white"
                    self.czcionka_arial = ("Roboto", int(13 * sk))
            if i < len(self.gracze):
                label_pozycja = tk.Label(self.panel_tabela, text=f"#{i + 1}", bg="#6B0000", fg=self.kolor,
                                         font=self.czcionka_arial)
                label_gracz = tk.Label(self.panel_tabela, text=nazwa_gracza, bg="#6B0000", fg=self.kolor,
                                       font=self.czcionka_arial)
                label_punkty = tk.Label(self.panel_tabela, text=str(ilosc_punktow), bg="#6B0000",
                                        fg=self.kolor, font=self.czcionka_arial)
            else:
                label_pozycja = tk.Label(self.panel_tabela, font=self.czcionka_arial, bg="#6B0000")
                label_gracz = tk.Label(self.panel_tabela, font=self.czcionka_arial, bg="#6B0000")
                label_punkty = tk.Label(self.panel_tabela, font=self.czcionka_arial, bg="#6B0000")
            label_pozycja.grid(row=i + 3 - self.pk, column=0, padx=10 * sk, pady=3 * sk * mn)
            label_gracz.grid(row=i + 3 - self.pk, column=1, padx=(0, 0), pady=3 * sk * mn)
            label_punkty.grid(row=i + 3 - self.pk, column=2, padx=10 * sk, pady=3 * sk * mn)

        akt_poz += 1
        if ilosc_linii / 25 > ilosc_linii // 25:
            ilosc_stron = ilosc_linii // 25 + 1
        else:
            ilosc_stron = ilosc_linii // 25
        strony = ["◀", f"Strona({(self.pk // 25) + 1}/{(ilosc_stron)})", "▶"]

        def previous_page():
            if self.pk > 0:
                self.pk -= 25
                self.czyszczenie = 1
                self.ukryj_tablice_wynikow()
                self.tablica_wynikow()
            else:
                button.config(state=tk.DISABLED)

        def next_page():
            self.pk += 25
            self.czyszczenie = 1
            self.ukryj_tablice_wynikow()
            self.tablica_wynikow()

        for i, strona in enumerate(strony):
            if strona == "◀":
                button = tk.Button(
                    self.panel_tabela,
                    text=strona,
                    relief=tk.FLAT,
                    bg="#330000",
                    fg="white",
                    activebackground="#B70000",
                    activeforeground="white",
                    borderwidth=0,
                    font=("Stem-Medium", int(15 * sk)),
                    command=previous_page
                )
                if self.pk > 0:
                    button.bind("<Enter>", lambda event, button=button: button.config(bg="#B70000"))
                    button.bind("<Leave>", lambda event, button=button: button.config(bg="#330000"))
                    button.config(state=tk.NORMAL)
                else:
                    button.config(state=tk.DISABLED, text="")
            elif strona == "▶":
                button = tk.Button(
                    self.panel_tabela,
                    text=strona,
                    relief=tk.FLAT,
                    bg="#330000",
                    fg="white",
                    activebackground="#B70000",
                    activeforeground="white",
                    borderwidth=0,
                    font=("Stem-Medium", int(15 * sk)),
                    command=next_page
                )
                if ilosc_linii > akt_poz:
                    button.bind("<Enter>", lambda event, button=button: button.config(bg="#B70000"))
                    button.bind("<Leave>", lambda event, button=button: button.config(bg="#330000"))
                else:
                    button.config(state=tk.DISABLED, text="")
            else:
                button = tk.Button(
                    self.panel_tabela,
                    text=strona,
                    relief=tk.FLAT,
                    bg="#330000",
                    fg="white",
                    activebackground="#B70000",
                    activeforeground="white",
                    borderwidth=0,
                    font=("Stem-Medium", int(15 * sk)),
                    state=tk.DISABLED,
                    disabledforeground="white"
                )
            button.grid(row=28, column=i, padx=0, pady=(5 * sk, 0), sticky="ew")

    def sortowanie_babelkowe(self):
        n = len(self.gracze)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.gracze[j + 1][1] > self.gracze[j][1]:
                    self.gracze[j], self.gracze[j + 1] = self.gracze[j + 1], self.gracze[j]

    def ukryj_tablice_wynikow(self):
        self.panel_tabela.place_forget()

    def pokaz_panel_przyciskow(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.36 * screen_width)
        b = int(0.25 * screen_height)
        self.panel_przyciskow.place(x=a, y=b)

    def ukryj_panel_przyciskow(self):
        self.panel_przyciskow.place_forget()

    def ukryj_panel_rozgr(self):
        self.panel_rozgr.place_forget()

    def pokaz_panel_rozgr(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.32 * screen_width)
        b = int(0.25 * screen_height)
        self.panel_rozgr.place(x=a, y=b)

    def dalej(self):
        self.label_sprobuj_ponownie.grid_remove()
        if self.ktore_menu == 1:
            nazwa_gracza1 = self.entry_gracz1.get()
        else:
            nazwa_gracza1 = ""  # menu == 2
        nazwa_gracza2 = self.entry_gracz2.get()

        if ((self.ktore_menu == 1 and (not nazwa_gracza1 or not nazwa_gracza2))
            or (self.ktore_menu == 2 and not nazwa_gracza2)):
            self.sprobuj_ponownie = 1
            self.label_sprobuj_ponownie.grid()
            self.g_line1.grid()
            self.entry_gracz1.delete(0, tk.END)
            self.entry_gracz2.delete(0, tk.END)
            return

        if nazwa_gracza1 == nazwa_gracza2:
            self.sprobuj_ponownie = 1
            self.label_sprobuj_ponownie2.grid_remove()
            self.label_sprobuj_ponownie.grid()
            self.g_line1.grid()
            self.entry_gracz1.delete(0, tk.END)
            self.entry_gracz2.delete(0, tk.END)
            return

        if len(nazwa_gracza1) > 20 or len(nazwa_gracza2) > 20:
            self.sprobuj_ponownie = 1
            self.label_sprobuj_ponownie.grid_remove()
            self.label_sprobuj_ponownie2.grid()
            self.g_line1.grid()
            self.entry_gracz1.delete(0, tk.END)
            self.entry_gracz2.delete(0, tk.END)
            return

        # Dodajemy/aktualizujemy dane gracza1
        if self.ktore_menu != 2:
            self.dane_graczy["gracz1"]["nazwa"] = nazwa_gracza1
            if self.sprawdz_czy_gracz_istnieje(nazwa_gracza1):
                self.dane_graczy["gracz1"]["ilosc_punktow"] = self.pobierz_ilosc_punktow(nazwa_gracza1)
            else:
                self.dodaj_gracza_do_pliku(nazwa_gracza1)

        # Dodajemy/aktualizujemy dane gracza2
        self.dane_graczy["gracz2"]["nazwa"] = nazwa_gracza2
        if self.sprawdz_czy_gracz_istnieje(nazwa_gracza2):
            self.dane_graczy["gracz2"]["ilosc_punktow"] = self.pobierz_ilosc_punktow(nazwa_gracza2)
        else:
            self.dodaj_gracza_do_pliku(nazwa_gracza2)

        self.label_sprobuj_ponownie.grid_remove()
        self.g_line1.grid_remove()
        self.ukryj_panel_przyciskow()
        self.ilosc_kart_panel()

    def ilosc_kart_panel(self):
        self.liczymy_karty = []
        self.powt_ruch = 0
        self.aktualny_panel = random.randint(1, 2)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.25 * screen_width)
        b = int(0.35 * screen_height)
        sk = screen_width / 1920

        self.panel_karty = tk.Frame(self.root, width=0, height=0, bg="#6B0000", bd=0, relief=tk.SOLID)
        self.panel_karty.place(x=a, y=b)

        label_gracz1 = tk.Label(self.panel_karty, text="Ilość kart:", bg="#6B0000", fg="white", font=self.czcionka_ramki)
        label_gracz1.grid(row=0, column=3, pady=(30 * sk, 15 * sk), padx=0)

        przycisk_rozp = tk.Button(
            self.panel_karty,
            text="  10  ",
            command=lambda: self.ile_kart("10"),
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_rozp.grid(row=1, column=1, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_rozp = tk.Button(
            self.panel_karty,
            text="  20  ",
            command=lambda: self.ile_kart("20"),
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_rozp.grid(row=1, column=2, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_rozp = tk.Button(
            self.panel_karty,
            text="  25  ",
            command=lambda: self.ile_kart("25"),
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_rozp.grid(row=1, column=3, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_rozp = tk.Button(
            self.panel_karty,
            text="  30  ",
            command=lambda: self.ile_kart("30"),
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_rozp.grid(row=1, column=4, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

        przycisk_rozp = tk.Button(
            self.panel_karty,
            text="  34  ",
            command=lambda: self.ile_kart("34"),
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        przycisk_rozp.grid(row=1, column=5, pady=(30 * sk, 60 * sk), padx=50 * sk)
        przycisk_rozp.bind("<Enter>", lambda event, button=przycisk_rozp: button.config(bg="#B70000"))
        przycisk_rozp.bind("<Leave>", lambda event, button=przycisk_rozp: button.config(bg="#330000"))

    def panel_gry(self):
        self.rozgrywka = 1
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.02 * screen_width)
        b = int(0.07 * screen_height)
        sk = screen_width / 1920

        self.panel_g1 = tk.Frame(self.root, width=screen_width, height=200, bg="#191919", relief=tk.SOLID)
        self.panel_g1.place(x=a, y=b)

        komp_red_img = Image.open(self.komp_red_png_path)
        x1, y1 = komp_red_img.size
        komp_red_img = komp_red_img.resize((int(x1 * sk * 0.8), int(y1 * sk * 0.8)))
        self.icon_komp_red = ImageTk.PhotoImage(komp_red_img)

        if self.ktore_menu == 1:
            label_g1 = tk.Label(
                self.panel_g1,
                text=f"{self.dane_graczy['gracz1']['nazwa']} | Ilość punktów: {self.dane_graczy['gracz1']['ilosc_punktow']}",
                bg="#191919",
                fg="red",
                font=self.czcionka_ramki
            )
            label_g1.grid(row=0, column=0, pady=(12 * sk, 12 * sk), padx=(30 * sk, 30 * sk), sticky="we")
        else:  # self.ktore_menu == 2
            label_g1 = tk.Label(
                self.panel_g1,
                text=f"Komputer | Poziom: {self.poziom}",
                image=self.icon_komp_red,
                compound=tk.LEFT,
                bg="#191919",
                fg="red",
                font=self.czcionka_ramki
            )
            label_g1.grid(row=0, column=0, pady=(12 * sk, 12 * sk), padx=(30 * sk, 30 * sk), sticky="we")

        a = int(0.02 * screen_width)
        b = int(0.9 * screen_height)

        self.panel_g2 = tk.Frame(self.root, width=0, height=0, bg="#191919", relief=tk.SOLID)
        self.panel_g2.place(x=a, y=b)

        label_g2 = tk.Label(
            self.panel_g2,
            text=f"{self.dane_graczy['gracz2']['nazwa']} | Ilość punktów: {self.dane_graczy['gracz2']['ilosc_punktow']}",
            bg="#191919",
            fg="#0045FF",
            font=self.czcionka_ramki
        )
        label_g2.grid(row=1, column=0, pady=(12 * sk, 12 * sk), padx=(30 * sk, 30 * sk))

        self.pokaz_panel_przyciskow1()
        self.pokaz_panel_przyciskow2()
        self.ktory_panel()

    def zaktualizuj_punkty_po_wygranej(self):
        if self.aktualny_panel == 1:
            wygrany_gracz = self.dane_graczy['gracz1']
            przegrany_gracz = self.dane_graczy['gracz2']
        else:
            wygrany_gracz = self.dane_graczy['gracz2']
            przegrany_gracz = self.dane_graczy['gracz1']

        # Zaktualizuj punkty po wygranej
        wygrany_gracz['ilosc_punktow'] += 1
        if przegrany_gracz['ilosc_punktow'] > 0:
            przegrany_gracz['ilosc_punktow'] -= 1

        self.zapisz_do_pliku(wygrany_gracz['nazwa'], wygrany_gracz['ilosc_punktow'])
        self.zapisz_do_pliku(przegrany_gracz['nazwa'], przegrany_gracz['ilosc_punktow'])

    def pokaz_panel_przyciskow1(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.41 * screen_width)
        b = int(0.07 * screen_height)

        self.przycisk1 = tk.Button(
            self.root,
            text="Usuń 1 kartę",
            command=lambda: self.usun_karte("1"),
            font=self.czcionka_ramki,
            bg="#630000",
            fg="white",
            activebackground="#D10000",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk1.bind("<Enter>", lambda event, button=self.przycisk1: button.config(bg="#D10000"))
        self.przycisk1.bind("<Leave>", lambda event, button=self.przycisk1: button.config(bg="#630000"))

        self.przycisk2 = tk.Button(
            self.root,
            text="Usuń 2 karty",
            command=lambda: self.usun_karte("2"),
            font=self.czcionka_ramki,
            bg="#630000",
            fg="white",
            activebackground="#D10000",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk2.bind("<Enter>", lambda event, button=self.przycisk2: button.config(bg="#D10000"))
        self.przycisk2.bind("<Leave>", lambda event, button=self.przycisk2: button.config(bg="#630000"))

        self.przycisk3 = tk.Button(
            self.root,
            text="Usuń 3 karty",
            command=lambda: self.usun_karte("3"),
            font=self.czcionka_ramki,
            bg="#630000",
            fg="white",
            activebackground="#D10000",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk3.bind("<Enter>", lambda event, button=self.przycisk3: button.config(bg="#D10000"))
        self.przycisk3.bind("<Leave>", lambda event, button=self.przycisk3: button.config(bg="#630000"))

        if self.ktore_menu == 1:
            self.przycisk1.place(x=a, y=b)
            self.przycisk2.place(x=a + 300, y=b)
            self.przycisk3.place(x=a + 600, y=b)

    def usun_panel_przyciskow1(self):
        for button in [self.przycisk1, self.przycisk2, self.przycisk3]:
            button.destroy()

    def usun_panel_przyciskow2(self):
        for button in [self.przycisk_rozp1, self.przycisk_rozp2, self.przycisk_rozp3]:
            button.destroy()

    def pokaz_panel_przyciskow2(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        c = int(0.41 * screen_width)
        d = int(0.9 * screen_height)

        self.przycisk_rozp1 = tk.Button(
            self.root,
            text="Usuń 1 kartę",
            command=lambda: self.usun_karte("1"),
            font=self.czcionka_ramki,
            bg="#00093D",
            fg="white",
            activebackground="#00093D",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk_rozp1.bind("<Enter>", lambda event, button=self.przycisk_rozp1: button.config(bg="#106C96"))
        self.przycisk_rozp1.bind("<Leave>", lambda event, button=self.przycisk_rozp1: button.config(bg="#00093D"))
        self.przycisk_rozp1.place(x=c, y=d)

        self.przycisk_rozp2 = tk.Button(
            self.root,
            text="Usuń 2 karty",
            command=lambda: self.usun_karte("2"),
            font=self.czcionka_ramki,
            bg="#00093D",
            fg="white",
            activebackground="#00093D",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk_rozp2.bind("<Enter>", lambda event, button=self.przycisk_rozp2: button.config(bg="#106C96"))
        self.przycisk_rozp2.bind("<Leave>", lambda event, button=self.przycisk_rozp2: button.config(bg="#00093D"))
        self.przycisk_rozp2.place(x=c + 300, y=d)

        self.przycisk_rozp3 = tk.Button(
            self.root,
            text="Usuń 3 karty",
            command=lambda: self.usun_karte("3"),
            font=self.czcionka_ramki,
            bg="#00093D",
            fg="white",
            activebackground="#00093D",
            activeforeground="white",
            borderwidth=0
        )
        self.przycisk_rozp3.bind("<Enter>", lambda event, button=self.przycisk_rozp3: button.config(bg="#106C96"))
        self.przycisk_rozp3.bind("<Leave>", lambda event, button=self.przycisk_rozp3: button.config(bg="#00093D"))
        self.przycisk_rozp3.place(x=c + 600, y=d)

    def komputer(self):
        if self.aktualny_panel == 2:
            sprawdzanie_kart = self.ilosc_kart
            ustalanie_randomu = random.randint(0, 10)
            if self.poziom == "Łatwy":
                if self.ilosc_kart == 1:
                    jaki_przycisk = 1
                elif self.ilosc_kart == 2:
                    jaki_przycisk = random.randint(1, 2)
                else:
                    jaki_przycisk = random.randint(1, 3)
            elif self.poziom == "Średni":
                if self.ilosc_kart == 1:
                    jaki_przycisk = 1
                elif self.ilosc_kart == 2:
                    if ustalanie_randomu < 8:
                        jaki_przycisk = 2
                    else:
                        jaki_przycisk = 1
                elif self.ilosc_kart == 3:
                    if ustalanie_randomu < 8:
                        jaki_przycisk = 3
                    else:
                        jaki_przycisk = random.randint(1, 2)
                else:
                    if self.ilosc_kart % 4 != 0:
                        while sprawdzanie_kart % 4 != 0:
                            sprawdzanie_kart -= 1
                        if ustalanie_randomu < 6:
                            jaki_przycisk = self.ilosc_kart - sprawdzanie_kart
                        else:
                            jaki_przycisk = random.randint(1, 3)
                        self.powt_ruch = 0
                    else:
                        if self.ilosc_kart > 11:
                            if self.powt_ruch > random.randint(2, 4):
                                jaki_przycisk = random.randint(1, 2)
                            else:
                                jaki_przycisk = random.randint(1, 3)
                        else:
                            jaki_przycisk = random.randint(1, 2)
                        self.powt_ruch += 1
            else:  # self.poziom == "Trudny"
                if self.ilosc_kart == 1:
                    jaki_przycisk = 1
                elif self.ilosc_kart == 2:
                    jaki_przycisk = 2
                elif self.ilosc_kart == 3:
                    jaki_przycisk = 3
                else:
                    if self.ilosc_kart % 4 != 0:
                        while sprawdzanie_kart % 4 != 0:
                            sprawdzanie_kart -= 1
                        jaki_przycisk = self.ilosc_kart - sprawdzanie_kart
                        self.powt_ruch = 0
                    else:
                        if self.ilosc_kart > 11:
                            if self.powt_ruch > random.randint(2, 4):
                                jaki_przycisk = random.randint(1, 2)
                            else:
                                jaki_przycisk = random.randint(1, 3)
                        else:
                            jaki_przycisk = random.randint(1, 2)
                        self.powt_ruch += 1

            if jaki_przycisk == 1:
                self.root.after(1300, self.przycisk1.invoke)
            elif jaki_przycisk == 2:
                self.root.after(1300, self.przycisk2.invoke)
            else:
                self.root.after(1300, self.przycisk3.invoke)

    def liczba_kart_panel(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.45 * screen_width)
        b = int(0.21 * screen_height)
        sk = screen_width / 1920

        self.panel_lkart = tk.Frame(self.root, width=0, height=0, bg="#0094FF", bd=0, relief=tk.SOLID)
        self.panel_lkart.place(x=a, y=b)

        label_lkart = tk.Label(
            self.panel_lkart,
            text=f"Ilość kart:{self.ilosc_kart}",
            bg="#CCCCCC",
            fg="white",
            font=("Stem-Medium", int(22 * sk))
        )
        label_lkart.grid(row=0, column=3, pady=0, padx=0)

    def ktory_panel(self):
        if self.ktore_menu == 1:
            self.usun_panel_przyciskow1()
        self.usun_panel_przyciskow2()

        if self.ilosc_kart == 0:
            if self.ktore_menu == 1:
                self.usun_panel_przyciskow1()
            self.usun_panel_przyciskow2()
        else:
            if self.aktualny_panel == 1:
                if self.ktore_menu == 1:
                    self.usun_panel_przyciskow1()
                self.pokaz_panel_przyciskow2()
                self.aktualny_panel = 2
                if self.powrot_do_menu:
                    self.powrot_do_menu(3)
            else:
                self.komputer_aktywacja = 0
                self.usun_panel_przyciskow2()
                if self.ktore_menu == 1:
                    self.pokaz_panel_przyciskow1()
                if self.ktore_menu == 2:
                    self.komputer()
                self.aktualny_panel = 1
                if self.powrot_do_menu:
                    self.powrot_do_menu(2)

    def usun_karte(self, usun):
        self.panel_lkart.place_forget()
        if usun == "1" and self.ilosc_kart > 0:
            self.ilosc_kart -= 1
            self.ktory_panel()
        elif usun == "2" and self.ilosc_kart > 1:
            if self.ktore_menu == 2 and self.aktualny_panel == 2 and self.ilosc_kart == 2:
                self.ilosc_kart -= 1
            else:
                self.ilosc_kart -= 2
                self.ktory_panel()
        elif usun == "3" and self.ilosc_kart > 2:
            if self.ktore_menu == 2 and self.aktualny_panel == 2 and self.ilosc_kart == 3:
                self.ilosc_kart -= 2
            else:
                self.ilosc_kart -= 3
                self.ktory_panel()

        self.liczba_kart_panel()
        self.komputer_aktywacja = 1

        while len(self.liczymy_karty) > self.ilosc_kart:
            indeks_usuniecia = random.randint(0, len(self.liczymy_karty) - 1)
            self.liczymy_karty.pop(indeks_usuniecia)

        if (self.ilosc_kart == 0 and self.rozgrywka == 1) or \
           (self.ktore_menu == 2 and self.aktualny_panel == 2 and self.ilosc_kart == 1):
            if self.ktore_menu == 1:
                self.usun_panel_przyciskow1()
            self.usun_panel_przyciskow2()
            self.panel_lkart.place_forget()
            self.wygrana()

        if self.callback:
            self.callback()

    def wygrana(self):
        print(self.liczymy_karty)
        self.pk = 0
        self.ukryj_panel_gry()
        self.zaktualizuj_punkty_po_wygranej()
        self.tablica_wynikow()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        sk = screen_width / 1920

        self.dane_graczy["gracz1"]["kolor"] = "#FF002C"
        self.dane_graczy["gracz2"]["kolor"] = "#00D8FF"

        if self.aktualny_panel == 1:
            wygrany_gracz = self.dane_graczy['gracz1']
            przegrany_gracz = self.dane_graczy['gracz2']
            wygrana_pozycja = self.pozycja_gracz1
            przegrana_pozycja = self.pozycja_gracz2
        else:
            wygrany_gracz = self.dane_graczy['gracz2']
            przegrany_gracz = self.dane_graczy['gracz1']
            wygrana_pozycja = self.pozycja_gracz2
            przegrana_pozycja = self.pozycja_gracz1

        if self.ktore_menu == 2 and wygrany_gracz == self.dane_graczy['gracz2']:
            a = int(0.27 * screen_width)
            b = int(0.2 * screen_height)
        else:
            a = int(0.27 * screen_width)
            b = int(0.25 * screen_height)

        self.panel_g3 = tk.Frame(self.root, width=0, height=0, bg="#6B0000", bd=0, relief=tk.SOLID)
        self.panel_g3.place(x=a, y=b)

        if self.ktore_menu == 1 or (self.ktore_menu == 2 and wygrany_gracz == self.dane_graczy['gracz2']):
            label_g1 = tk.Label(
                self.panel_g3,
                text="WYGRANA",
                bg="#330000",
                fg="#4AF700",
                font=("Stem-Bold", int(24 * sk), "bold")
            )
            label_g1.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=8)
            g_line = tk.Frame(self.panel_g3, bg="#4AF700", height=4)
            g_line.grid(row=1, column=0, columnspan=3, sticky="ew")
        else:
            label_g1 = tk.Label(
                self.panel_g3,
                text="PRZEGRANA",
                bg="#330000",
                fg="#FF2600",
                font=("Stem-Bold", int(24 * sk), "bold")
            )
            label_g1.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="ew", ipady=8)
            g_line = tk.Frame(self.panel_g3, bg="#FF2600", height=4)
            g_line.grid(row=1, column=0, columnspan=3, sticky="ew")

        # ---------------
        # Tutaj delikatnie zmieniamy, by ładować pliki kart z base_path
        # ---------------
        if self.ktore_menu == 1:
            label_g1 = tk.Label(
                self.panel_g3,
                text=f"#{wygrana_pozycja} ● {wygrany_gracz['nazwa']} ● {wygrany_gracz['ilosc_punktow']} pkt ▲",
                bg="#6B0000",
                fg=wygrany_gracz['kolor'],
                font=("Stem-Bold", int(40 * sk), "bold")
            )
            label_g1.grid(row=2, column=0, columnspan=3, sticky="we", pady=10)

            label_g1 = tk.Label(
                self.panel_g3,
                text=f"#{przegrana_pozycja} ● {przegrany_gracz['nazwa']} ● {przegrany_gracz['ilosc_punktow']} pkt ▼",
                bg="#6B0000",
                fg=przegrany_gracz['kolor'],
                font=("Stem-Bold", int(30 * sk), "bold")
            )
            label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 30))

        elif self.ktore_menu == 2 and wygrany_gracz != self.dane_graczy['gracz2']:
            label_g1 = tk.Label(
                self.panel_g3,
                text="Nie udało ci się dostać na żaden\n z kierunków studiów UG",
                bg="#6B0000",
                fg="white",
                font=("Stem-Bold", int(35 * sk), "bold")
            )
            label_g1.grid(row=2, column=0, columnspan=3, sticky="we", pady=10)

        elif self.ktore_menu == 2 and wygrany_gracz == self.dane_graczy['gracz2']:
            label_g1 = tk.Label(
                self.panel_g3,
                text=f"#{wygrana_pozycja} ● {wygrany_gracz['nazwa']} ● {wygrany_gracz['ilosc_punktow']} pkt ▲",
                bg="#6B0000",
                fg=wygrany_gracz['kolor'],
                font=("Stem-Bold", int(30 * sk), "bold")
            )
            label_g1.grid(row=2, column=0, columnspan=3, sticky="we", pady=10)

            # W zależności od self.liczymy_karty[0], ładujemy inną "kartę" z base_path
            # Zamiast "karta1.png" bezwzględnie, używamy os.path.join(self.base_path, "karta1.png")
            # i tak dla wszystkich, minimalna zmiana w logice if-ów:

            if self.liczymy_karty[0] == 0:
                path_card = os.path.join(self.base_path, "karta1.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Informatyki",
                    bg="#6B0000",
                    fg="#00C1C1",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 1:
                path_card = os.path.join(self.base_path, "karta2.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Prawa i Administracji",
                    bg="#6B0000",
                    fg="#C18700",
                    font=("Stem-Bold", int(35 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 2:
                path_card = os.path.join(self.base_path, "karta3.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Geografii",
                    bg="#6B0000",
                    fg="#AEAB00",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 3:
                path_card = os.path.join(self.base_path, "karta4.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Chemii",
                    bg="#6B0000",
                    fg="#7D00C1",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 4:
                path_card = os.path.join(self.base_path, "karta5.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Biologii",
                    bg="#6B0000",
                    fg="#257110",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 5:
                path_card = os.path.join(self.base_path, "karta6.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się skierować do\nBiblioteki Głównej UG",
                    bg="#6B0000",
                    fg="#103271",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 6:
                path_card = os.path.join(self.base_path, "karta7.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Matematyki,\nFizyki, Informatyki",
                    bg="#6B0000",
                    fg="#878787",
                    font=("Stem-Bold", int(35 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 7:
                path_card = os.path.join(self.base_path, "karta8.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Historyczny",
                    bg="#6B0000",
                    fg="#C10100",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 8:
                path_card = os.path.join(self.base_path, "karta9.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Filologiczny",
                    bg="#6B0000",
                    fg="#C1008E",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 9:
                path_card = os.path.join(self.base_path, "karta10.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Oceanografii",
                    bg="#6B0000",
                    fg="#00A4D3",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

            elif self.liczymy_karty[0] == 10:
                path_card = os.path.join(self.base_path, "karta11.png")
                original_image = Image.open(path_card)
                resized_image = original_image.resize((int(original_image.width / 1.3 * sk),
                                                       int(original_image.height / 1.3 * sk)))
                tk_image = ImageTk.PhotoImage(resized_image)

                label_g1 = tk.Label(
                    self.panel_g3,
                    text="Udało ci się dostać na\nWydział Zarządzania",
                    bg="#6B0000",
                    fg="#F64200",
                    font=("Stem-Bold", int(40 * sk), "bold"),
                    image=tk_image,
                    compound="left",
                    padx=100
                )
                label_g1.image = tk_image
                label_g1.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)

        label_g1 = tk.Button(
            self.panel_g3,
            text="Nowa gra",
            command=self.nowa_gra,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        label_g1.grid(row=5, column=2, pady=(30, 60), padx=60)
        label_g1.bind("<Enter>", lambda event, button=label_g1: button.config(bg="#B70000"))
        label_g1.bind("<Leave>", lambda event, button=label_g1: button.config(bg="#330000"))

        label_g1 = tk.Button(
            self.panel_g3,
            text="Zagraj jeszcze raz",
            command=self.zagraj_ponownie,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        label_g1.grid(row=5, column=1, pady=(30, 60), padx=60)
        label_g1.bind("<Enter>", lambda event, button=label_g1: button.config(bg="#B70000"))
        label_g1.bind("<Leave>", lambda event, button=label_g1: button.config(bg="#330000"))

        label_g1 = tk.Button(
            self.panel_g3,
            text="Powrót",
            command=self.powrot3,
            font=self.czcionka_ramki,
            relief=tk.FLAT,
            bg="#330000",
            fg="white",
            activebackground="#B70000",
            activeforeground="white",
            borderwidth=0
        )
        label_g1.grid(row=5, column=0, pady=(30, 60), padx=60)
        label_g1.bind("<Enter>", lambda event, button=label_g1: button.config(bg="#B70000"))
        label_g1.bind("<Leave>", lambda event, button=label_g1: button.config(bg="#330000"))

    def ukryj_panel_gry(self):
        self.panel_g1.place_forget()
        self.panel_g2.place_forget()

    def nowa_gra(self):
        self.ukryj_panel_gry()
        self.panel_g3.place_forget()
        self.ukryj_tablice_wynikow()
        self.menu_komp()
        if self.powrot_do_menu:
            self.powrot_do_menu(4)

    def powrot3(self):
        self.panel_g3.place_forget()
        self.ukryj_panel_gry()
        self.powrot2()

    def powrot2(self):
        self.ukryj_panel_rozgr()
        self.ukryj_tablice_wynikow()
        if self.powrot_do_menu:
            self.powrot_do_menu(1)

    def powrot4(self):
        self.ukryj_panel_przyciskow()
        self.pokaz_panel_rozgr()

    def zagraj_ponownie(self):
        self.rozgrywka = 0
        self.panel_g3.place_forget()
        self.label_sprobuj_ponownie.grid_remove()
        self.g_line1.grid_remove()
        self.ukryj_panel_przyciskow()
        self.ilosc_kart_panel()
        if self.powrot_do_menu:
            self.powrot_do_menu(4)

    def ile_kart(self, liczba):
        if liczba == "10":
            self.ilosc_kart = 10
        elif liczba == "20":
            self.ilosc_kart = 20
        elif liczba == "25":
            self.ilosc_kart = 25
        elif liczba == "30":
            self.ilosc_kart = 30
        elif liczba == "34":
            self.ilosc_kart = 34

        for i in range(self.ilosc_kart):
            self.liczymy_karty.append(random.randint(0, 10))

        self.liczba_kart_panel()
        self.panel_gry()
        self.ukryj_tablice_wynikow()
        self.ukryj_ile_kart()

    def ukryj_ile_kart(self):
        if self.ilosc_kart != 0:
            self.panel_karty.place_forget()
            if self.callback:
                self.callback()

    def sprawdz_czy_gracz_istnieje(self, nazwa_gracza):
        with open("dane_graczy.txt", "r") as plik:
            for linia in plik:
                if nazwa_gracza.strip() in linia.strip():
                    return True
        return False

    def zapisz_do_pliku(self, nazwa_gracza, ilosc_punktow):
        with open("dane_graczy.txt", "r") as plik:
            linie = plik.readlines()

        with open("dane_graczy.txt", "w") as plik:
            for i in range(0, len(linie), 2):
                if nazwa_gracza.strip() == linie[i].strip():
                    plik.write(f"{nazwa_gracza}\n{ilosc_punktow}\n")
                else:
                    plik.write(linie[i])
                    if i + 1 < len(linie):
                        plik.write(linie[i + 1])

    def pobierz_ilosc_punktow(self, nazwa_gracza):
        with open("dane_graczy.txt", "r") as plik:
            linie = plik.readlines()

        for i in range(0, len(linie), 2):
            if nazwa_gracza.strip() == linie[i].strip():
                if i + 1 < len(linie):
                    punkty_str = linie[i + 1].strip()
                    if punkty_str.isdigit():
                        return int(punkty_str)
                return 0
        return 0

    def dodaj_gracza_do_pliku(self, nazwa_gracza):
        with open("dane_graczy.txt", "a") as plik:
            plik.write(f"{nazwa_gracza}\n0\n")


if __name__ == '__main__':
    root = tk.Tk()
    app = gra(root, None, None)  # None, None są dla callback i powrot_do_menu
    root.mainloop()
