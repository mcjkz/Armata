import tkinter as tk
import sys, os
from PIL import Image, ImageTk
import pygame
from gra import gra
from tkinter import font
import random
from tkextrafont import Font

class PrzesuwaneObrazy:

    def __init__(self, root,
                 sciezka_do_obrazu1, sciezka_do_obrazu2, sciezka_do_obrazu3,
                 sciezka_do_obrazu4, sciezka_do_obrazu5, sciezka_do_obrazu6, sciezka_do_obrazu7,
                 sciezka_do_dzwieku1, sciezka_do_dzwieku2, sciezka_do_dzwieku3, sciezka_do_dzwieku4, sciezka_do_dzwieku5):

        # Ustalanie base_path w zależności od tego, czy uruchamiamy .exe (PyInstaller), czy normalnie:
        if getattr(sys, 'frozen', False):
            # Uruchomione ze spakowanego .exe (PyInstaller)
            base_path = sys._MEIPASS
        else:
            # Uruchomiono normalnie (np. python menu.py)
            base_path = os.path.dirname(__file__)

        # Ścieżki do plików czcionek (wcześniej: Font(file="resources\fonts\Stem-Bold.ttf"), itd.)
        bold_font_path    = os.path.join(base_path, "resources", "fonts", "Stem-Bold.ttf")
        medium_font_path  = os.path.join(base_path, "resources", "fonts", "Stem-Medium.otf")
        regular_font_path = os.path.join(base_path, "resources", "fonts", "Stem-Regular.ttf")
        cards_path = os.path.join(base_path, "resources", "cards")

        # Rejestracja czcionek:
        Font(file=bold_font_path)
        Font(file=medium_font_path)
        Font(file=regular_font_path)

        self.root = root
        self.root.attributes("-fullscreen", True)

        # Dla przejrzystości: budujemy również ścieżki do obrazów i dźwięków na bazie base_path
        sciezka_obrazu1 = os.path.join(base_path, sciezka_do_obrazu1)
        sciezka_obrazu2 = os.path.join(base_path, sciezka_do_obrazu2)
        sciezka_obrazu3 = os.path.join(base_path, sciezka_do_obrazu3)
        sciezka_obrazu4 = os.path.join(base_path, sciezka_do_obrazu4)
        sciezka_obrazu5 = os.path.join(base_path, sciezka_do_obrazu5)
        sciezka_obrazu6 = os.path.join(base_path, sciezka_do_obrazu6)
        sciezka_obrazu7 = os.path.join(base_path, sciezka_do_obrazu7)

        sciezka_dzwieku1 = os.path.join(base_path, sciezka_do_dzwieku1)
        sciezka_dzwieku2 = os.path.join(base_path, sciezka_do_dzwieku2)
        sciezka_dzwieku3 = os.path.join(base_path, sciezka_do_dzwieku3)
        sciezka_dzwieku4 = os.path.join(base_path, sciezka_do_dzwieku4)
        sciezka_dzwieku5 = os.path.join(base_path, sciezka_do_dzwieku5)

        # Przygotuj ścieżki do plików kart (karta1.png, karta2.png, itp.)
        sciezka_karta   = os.path.join(cards_path, "karta1.png")
        sciezka_karta2  = os.path.join(cards_path, "karta2.png")
        sciezka_karta3  = os.path.join(cards_path, "karta3.png")
        sciezka_karta4  = os.path.join(cards_path, "karta4.png")
        sciezka_karta5  = os.path.join(cards_path, "karta5.png")
        sciezka_karta6  = os.path.join(cards_path, "karta6.png")
        sciezka_karta7  = os.path.join(cards_path, "karta7.png")
        sciezka_karta8  = os.path.join(cards_path, "karta8.png")
        sciezka_karta9  = os.path.join(cards_path, "karta9.png")
        sciezka_karta10 = os.path.join(cards_path, "karta10.png")
        sciezka_karta11 = os.path.join(cards_path, "karta11.png")

        self.ilosc_kart = 0
        self.lst = []
        self.lst2 = []
        self.ani_running = False
        self.animacja_w_trakcie = False

        self.czcionka_ramki  = ("Stem-Bold", 24  * root.winfo_screenwidth() // 1920)
        self.czcionka_ramki2 = ("Microsoft Sans Serif", 34 * root.winfo_screenwidth() // 1920, "bold")

        # Zmienna piętro (pietro)
        self.pietro = 0

        # Utwórz Canvas na cały ekran
        self.canvas = tk.Canvas(root,
                                width=root.winfo_screenwidth(),
                                height=root.winfo_screenheight(),
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.place(relwidth=1, relheight=1)

        # Dostosowywanie do rozmiaru ekranu:
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        sk = screen_width / 1920

        # --- Wczytanie i przeskalowanie obrazów ---
        self.obraz1 = Image.open(sciezka_obrazu1).resize((screen_width, screen_height))
        self.obraz2 = Image.open(sciezka_obrazu2).resize((screen_width, screen_height))
        self.obraz3 = Image.open(sciezka_obrazu3).resize((screen_width, screen_height))
        self.obraz4 = Image.open(sciezka_obrazu4).resize((screen_width, screen_height))
        self.obraz5 = Image.open(sciezka_obrazu5).resize((screen_width, screen_height))
        self.obraz6 = Image.open(sciezka_obrazu6).resize((screen_width, screen_height))
        self.obraz7 = Image.open(sciezka_obrazu7).resize((screen_width, screen_height))

        # Przerabiamy na PhotoImage
        self.obraz1 = ImageTk.PhotoImage(self.obraz1)
        self.obraz2 = ImageTk.PhotoImage(self.obraz2)
        self.obraz3 = ImageTk.PhotoImage(self.obraz3)
        self.obraz4 = ImageTk.PhotoImage(self.obraz4)
        self.obraz5 = ImageTk.PhotoImage(self.obraz5)
        self.obraz6 = ImageTk.PhotoImage(self.obraz6)
        self.obraz7 = ImageTk.PhotoImage(self.obraz7)

        # Karty
        karta1  = ImageTk.PhotoImage(Image.open(sciezka_karta))
        karta2  = ImageTk.PhotoImage(Image.open(sciezka_karta2))
        karta3  = ImageTk.PhotoImage(Image.open(sciezka_karta3))
        karta4  = ImageTk.PhotoImage(Image.open(sciezka_karta4))
        karta5  = ImageTk.PhotoImage(Image.open(sciezka_karta5))
        karta6  = ImageTk.PhotoImage(Image.open(sciezka_karta6))
        karta7  = ImageTk.PhotoImage(Image.open(sciezka_karta7))
        karta8  = ImageTk.PhotoImage(Image.open(sciezka_karta8))
        karta9  = ImageTk.PhotoImage(Image.open(sciezka_karta9))
        karta10 = ImageTk.PhotoImage(Image.open(sciezka_karta10))
        karta11 = ImageTk.PhotoImage(Image.open(sciezka_karta11))

        self.obrazy_kart = [
            karta1, karta2, karta3, karta4, karta5,
            karta6, karta7, karta8, karta9, karta10, karta11
        ]

        # Ustawienie obrazów na ekranie
        self.obraz1_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.obraz1)
        self.obraz2_id = self.canvas.create_image(0, -screen_height, anchor=tk.NW, image=self.obraz2)
        self.obraz3_id = self.canvas.create_image(0, -2*screen_height, anchor=tk.NW, image=self.obraz3)
        self.obraz4_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.obraz4)
        self.obraz5_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.obraz5)
        self.obraz6_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.obraz6)
        self.obraz7_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.obraz7)

        # Schowaj obrazy 4..7 na starcie
        self.canvas.itemconfig(self.obraz4_id, state=tk.HIDDEN)
        self.canvas.itemconfig(self.obraz5_id, state=tk.HIDDEN)
        self.canvas.itemconfig(self.obraz6_id, state=tk.HIDDEN)
        self.canvas.itemconfig(self.obraz7_id, state=tk.HIDDEN)

        # Wczytaj dźwięki (pygame)
        pygame.init()
        self.dzwiek1 = pygame.mixer.Sound(sciezka_dzwieku1)
        self.dzwiek2 = pygame.mixer.Sound(sciezka_dzwieku2)
        self.dzwiek3 = pygame.mixer.Sound(sciezka_dzwieku3)
        self.dzwiek4 = pygame.mixer.Sound(sciezka_dzwieku4)
        self.dzwiek5 = pygame.mixer.Sound(sciezka_dzwieku5)

        # Jeśli pietro == 0, to gra dźwięk1
        if self.pietro == 0:
            self.dzwiek1.play()

        # ------------------------------
        #  Tworzenie panelu przycisków
        # ------------------------------
        a = int(0.6 * screen_width)
        b = int(0.2 * screen_height)

        self.panel_przyciskow = tk.Frame(root, width=200, height=200,
                                         bg="#B2B2B2",
                                         highlightbackground="#606060",
                                         highlightthickness=4)
        self.panel_przyciskow.place(x=a, y=b)

        self.przycisk0 = tk.Frame(self.panel_przyciskow,
                                  bg="#8E8E8E",
                                  highlightbackground="#606060",
                                  highlightthickness=3)
        self.przycisk0.grid(row=2, column=0,
                            pady=(60 * sk, 70 * sk),
                            padx=(60 * sk, 20 * sk))

        self.etykieta0 = tk.Label(self.przycisk0,
                                  text=" 0 ",
                                  font=self.czcionka_ramki2,
                                  bg="#8E8E8E",
                                  fg="#333333")
        self.etykieta0.pack()
        self.etykieta0.bind("<Button-1>", lambda event: self.rozpocznij_animacje("pt0"))

        self.przycisk1 = tk.Frame(self.panel_przyciskow,
                                  bg="#8E8E8E",
                                  highlightbackground="#606060",
                                  highlightthickness=3)
        self.przycisk1.grid(row=1, column=0,
                            pady=60 * sk,
                            padx=(60 * sk, 20 * sk))

        self.etykieta1 = tk.Label(self.przycisk1,
                                  text=" 1 ",
                                  font=self.czcionka_ramki2,
                                  bg="#8E8E8E",
                                  fg="#333333")
        self.etykieta1.pack()
        self.etykieta1.bind("<Button-1>", lambda event: self.rozpocznij_animacje("pt1"))

        self.przycisk2 = tk.Frame(self.panel_przyciskow,
                                  bg="#8E8E8E",
                                  highlightbackground="#606060",
                                  highlightthickness=3)
        self.przycisk2.grid(row=0, column=0,
                            pady=(65 * sk, 60 * sk),
                            padx=(60 * sk, 20 * sk))

        self.etykieta2 = tk.Label(self.przycisk2,
                                  text=" 2 ",
                                  font=self.czcionka_ramki2,
                                  bg="#8E8E8E",
                                  fg="#333333")
        self.etykieta2.pack()
        self.etykieta2.bind("<Button-1>", lambda event: self.rozpocznij_animacje("pt2"))

        # Druga kolumna z napisami
        label_gora = tk.Label(self.panel_przyciskow,
                              text="Graj",
                              bg="#B2B2B2",
                              font=self.czcionka_ramki)
        label_gora.grid(row=0, column=1,
                        pady=60 * sk,
                        padx=(20 * sk, 60 * sk))

        label_dol = tk.Label(self.panel_przyciskow,
                             text="O grze",
                             bg="#B2B2B2",
                             font=self.czcionka_ramki)
        label_dol.grid(row=1, column=1,
                       pady=60 * sk,
                       padx=(20 * sk, 60 * sk))

        label_pt3 = tk.Label(self.panel_przyciskow,
                             text="Menu główne",
                             bg="#B2B2B2",
                             font=self.czcionka_ramki)
        label_pt3.grid(row=2, column=1,
                       pady=(60 * sk, 70 * sk),
                       padx=(20 * sk, 60 * sk))

        # Przycisk "O grze"
        self.przycisk_ogr = tk.Button(root,
                                      text="    O grze    ",
                                      command=self.o_grze,
                                      font=self.czcionka_ramki,
                                      fg="#002B04",
                                      bg="green",
                                      activebackground="green",
                                      bd=3)
        # Ukryj przycisk na początku (bo pietro != 1)
        self.przycisk_ogr.place_forget()

        # Przycisk "Graj"
        self.przycisk_graj = tk.Button(root,
                                       text="      Graj      ",
                                       command=self.graj,
                                       font=self.czcionka_ramki,
                                       bg="red",
                                       fg="#490000",
                                       activebackground="red",
                                       bd=3)
        self.przycisk_graj.place_forget()

        # Przycisk "Powrót"
        self.przycisk_powrot = tk.Button(root,
                                         text="Powrót",
                                         command=self.powrot,
                                         font=self.czcionka_ramki)
        self.przycisk_powrot.place_forget()

        # Flaga do śledzenia, czy obrazy są widoczne
        self.obrazy_widoczne = True

    # -----------------------------------------------------------------
    def karty(self):
        """
        Funkcja odpowiedzialna za manipulowanie obrazami kart na Canvasie,
        współpracuje z obiektem gra (self.test), w którym trzymane są
        informacje o kartach (self.test.liczymy_karty).
        """
        # Usuwa poprzednie karty z canvas
        for i in self.lst2:
            self.canvas.delete(i)
        self.lst2 = []
        self.lst = []

        if not (self.test.ktore_menu == 2 and
                self.test.aktualny_panel == 2 and
                self.test.ilosc_kart == 1):
            for i in range(self.test.ilosc_kart):
                idx_karty = self.test.liczymy_karty[i]
                self.obraz_karta = self.obrazy_kart[idx_karty]
                self.lst.append(self.obraz_karta)
            self.ilosc_kart = self.test.ilosc_kart
        else:
            self.ilosc_kart = 0

        if self.ilosc_kart != 0:
            self.min_odstep = 5
            self.ilosc_kart3 = self.ilosc_kart
            ekran_szerokosc = self.root.winfo_screenwidth()
            ekran_wysokosc = self.root.winfo_screenheight()

            if self.ilosc_kart > 17:
                if self.ilosc_kart % 2 == 0:
                    self.ilosc_kart2 = self.ilosc_kart // 2
                    self.ilosc_kart3 = self.ilosc_kart // 2
                else:
                    self.ilosc_kart2 = self.ilosc_kart // 2 + 1
                    self.ilosc_kart3 = self.ilosc_kart // 2

            if self.ilosc_kart3 < 10:
                odstep = 90
                szerokosc_kart = self.ilosc_kart3 * 100 + (self.ilosc_kart3 - 1) * odstep
                margines = (ekran_szerokosc - 80 - szerokosc_kart) // 2
            else:
                odstep = max(((ekran_szerokosc - 135) - self.ilosc_kart3 * 100) // (self.ilosc_kart3 - 1),
                             self.min_odstep)
                margines = 30

            if self.ilosc_kart <= 17:
                for i in range(self.ilosc_kart3):
                    self.obraz_karta = self.lst[i]
                    x = margines + i * (100 + odstep)
                    if (self.test.ktore_menu == 2 and
                        self.test.aktualny_panel == 2 and
                        self.ilosc_kart == 1):
                        y = int(0.6 * self.root.winfo_screenheight())
                    else:
                        y = (ekran_wysokosc - 170) // 2
                    obraz_id = self.canvas.create_image(x, y,
                                                        anchor=tk.NW,
                                                        image=self.obraz_karta)
                    self.lst2.append(obraz_id)
            else:
                odstep2 = max(((ekran_szerokosc - 135) - self.ilosc_kart2 * 100) // (self.ilosc_kart2 - 1),
                              self.min_odstep)
                margines = 30
                margines2 = 30
                if self.ilosc_kart3 < 10:
                    odstep = 90
                    szerokosc_kart = self.ilosc_kart3 * 100 + (self.ilosc_kart3 - 1) * odstep
                    margines = (ekran_szerokosc - 80 - szerokosc_kart) // 2
                if self.ilosc_kart2 < 10:
                    odstep2 = 90
                    szerokosc_kart2 = self.ilosc_kart2 * 100 + (self.ilosc_kart2 - 1) * odstep2
                    margines2 = (ekran_szerokosc - 80 - szerokosc_kart2) // 2

                self.ktory_obraz = 0
                for i in range(self.ilosc_kart3):
                    self.obraz_karta = self.lst[i]
                    x = margines + i * (100 + odstep)
                    y = (ekran_wysokosc - 500) // 2
                    obraz_id = self.canvas.create_image(x, y,
                                                        anchor=tk.NW,
                                                        image=self.obraz_karta)
                    self.lst2.append(obraz_id)
                    self.ktory_obraz = i
                for i in range(self.ilosc_kart2):
                    self.obraz_karta = self.lst[self.ktory_obraz + i]
                    x = margines2 + i * (100 + odstep2)
                    y = (ekran_wysokosc + 50) // 2
                    obraz_id = self.canvas.create_image(x, y,
                                                        anchor=tk.NW,
                                                        image=self.obraz_karta)
                    self.lst2.append(obraz_id)

    def ukryj_obrazy(self):
        if self.obrazy_widoczne:
            self.canvas.itemconfig(self.obraz1_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz2_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz3_id, state=tk.HIDDEN)
            self.obrazy_widoczne = False

    def pokaz_obrazy(self):
        if not self.obrazy_widoczne:
            self.canvas.itemconfig(self.obraz1_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.obraz2_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.obraz3_id, state=tk.NORMAL)
            self.obrazy_widoczne = True

    def pokaz_panel_przyciskow(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        a = int(0.6 * screen_width)
        b = int(0.2 * screen_height)
        self.panel_przyciskow.place(x=a, y=b)

    def ukryj_panel_przyciskow(self):
        self.panel_przyciskow.place_forget()

    def o_grze(self):
        self.dzwiek5.play()
        self.ukryj_obrazy()
        self.zatrzymaj_dzwiek()
        self.zatrzymaj_dzwiek2()
        self.ukryj_panel_przyciskow()
        self.ukryj_przycisk_ogr()
        self.pokaz_przycisk_powrot()
        self.canvas.itemconfig(self.obraz4_id, state=tk.NORMAL)

    def powrot_z_gry(self, argument):
        if argument == 1:
            self.dzwiek3.play()
            self.pokaz_obrazy()
            self.pokaz_panel_przyciskow()
            self.pokaz_przycisk_graj()
            self.canvas.itemconfig(self.obraz5_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz6_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz7_id, state=tk.HIDDEN)
        elif argument == 2:
            self.canvas.itemconfig(self.obraz6_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.obraz5_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz7_id, state=tk.HIDDEN)
        elif argument == 3:
            self.canvas.itemconfig(self.obraz7_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.obraz5_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz6_id, state=tk.HIDDEN)
        elif argument == 4:
            self.canvas.itemconfig(self.obraz7_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.obraz5_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.obraz6_id, state=tk.HIDDEN)

    def powrot(self):
        self.dzwiek2.play()
        self.pokaz_obrazy()
        self.pokaz_panel_przyciskow()
        self.pokaz_przycisk_ogr()
        self.canvas.itemconfig(self.obraz4_id, state=tk.HIDDEN)
        self.ukryj_przycisk_powrot()

    def graj(self):
        self.dzwiek5.play()
        self.ukryj_obrazy()
        self.zatrzymaj_dzwiek()
        self.zatrzymaj_dzwiek2()
        self.ukryj_panel_przyciskow()
        self.ukryj_przycisk_graj()
        self.canvas.itemconfig(self.obraz4_id, state=tk.HIDDEN)
        self.canvas.itemconfig(self.obraz5_id, state=tk.NORMAL)
        # Odpalamy logikę gry
        self.test = gra(self.root, callback=self.karty, powrot_do_menu=self.powrot_z_gry)

    def zatrzymaj_dzwiek(self):
        self.dzwiek1.stop()
        self.dzwiek2.stop()
        self.dzwiek3.stop()

    def zatrzymaj_dzwiek2(self):
        self.dzwiek4.stop()

    def rozpocznij_animacje(self, kierunek):
        """
        Obsługa animacji przesuwania obrazów w górę/dół, w zależności od
        wybranego "piętra" (pt0, pt1, pt2).
        """
        if not (kierunek == "pt0" and self.pietro == 0):
            if not (kierunek == "pt1" and self.pietro == 1):
                if not (kierunek == "pt2" and self.pietro == 2):
                    if not self.animacja_w_trakcie:
                        self.ani_running = True
                        self.animacja_w_trakcie = True
                        self.przesun_obrazy(kierunek)
                        self.dzwiek4.play()

    def przesun_obrazy(self, kierunek):
        if not self.ani_running:
            self.animacja_w_trakcie = False
            return

        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        piksele = 10 * (screen_height / 1080)

        # Podświetlanie przycisków w zależności od kierunku
        if (kierunek == "pt0" and self.pietro != 0):
            self.przycisk0.config(highlightbackground="#00FFFF")
            self.etykieta0.config(fg="#00FFFF", bg="#8E8E8E")
        if (kierunek == "pt1" and self.pietro != 1):
            self.przycisk1.config(highlightbackground="#00FFFF")
            self.etykieta1.config(fg="#00FFFF", bg="#8E8E8E")
        if (kierunek == "pt2" and self.pietro != 2):
            self.przycisk2.config(highlightbackground="#00FFFF")
            self.etykieta2.config(fg="#00FFFF", bg="#8E8E8E")

        # Logika przesuwania w dół lub w górę
        if (kierunek in ["pt1", "pt2"]) and self.pietro != 2:
            self.zatrzymaj_dzwiek()
            self.ukryj_przycisk_ogr()
            self.ukryj_przycisk_graj()
            self.canvas.move(self.obraz1_id, 0, piksele)
            self.canvas.move(self.obraz2_id, 0, piksele)
            self.canvas.move(self.obraz3_id, 0, piksele)
        elif kierunek == "pt0" or self.pietro == 2:
            self.zatrzymaj_dzwiek()
            self.ukryj_przycisk_ogr()
            self.ukryj_przycisk_graj()
            self.canvas.move(self.obraz3_id, 0, -piksele)
            self.canvas.move(self.obraz2_id, 0, -piksele)
            self.canvas.move(self.obraz1_id, 0, -piksele)

        # Sprawdź, czy górna krawędź obrazu2 spadła poza ekran
        obraz2_bbox = self.canvas.bbox(self.obraz2_id)
        if obraz2_bbox[1] >= screen_height and kierunek == "pt2":
            # Dotarliśmy do piętra 2
            self.pietro = 2
            self.ani_running = False
            self.dzwiek3.play()
            self.pokaz_przycisk_graj()
            self.przycisk2.config(highlightbackground="#606060")
            self.etykieta2.config(fg="#333333")
        elif self.pietro == 0:
            # Sprawdź, czy obraz1 spadł poza ekran
            obraz1_bbox = self.canvas.bbox(self.obraz1_id)
            if obraz1_bbox[1] >= screen_height and kierunek == "pt1":
                self.pietro = 1
                self.ani_running = False
                self.dzwiek2.play()
                self.pokaz_przycisk_ogr()
                self.przycisk1.config(highlightbackground="#606060")
                self.etykieta1.config(fg="#333333")
        elif self.pietro == 2 and kierunek == "pt1":
            # Jeżeli jesteśmy na piętrze 2 i cofamy się do pt1
            obraz3_bbox = self.canvas.bbox(self.obraz3_id)
            if obraz3_bbox[3] <= 0:
                self.pietro = 1
                self.ani_running = False
                self.dzwiek2.play()
                self.pokaz_przycisk_ogr()
                self.przycisk1.config(highlightbackground="#606060")
                self.etykieta1.config(fg="#333333")

        # Sprawdź, czy obraz2 zniknął w górę
        obraz2_bbox = self.canvas.bbox(self.obraz2_id)
        if obraz2_bbox[3] <= 0:
            self.pietro = 0
            self.ani_running = False
            self.dzwiek1.play()
            self.przycisk0.config(highlightbackground="#606060")
            self.etykieta0.config(fg="#333333")

        # Kontynuuj animację
        self.root.after(10, self.przesun_obrazy, kierunek)

    def pokaz_przycisk_ogr(self):
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        c = int(0.66 * screen_width)
        d = int(0.76 * screen_height)
        self.przycisk_ogr.place(x=c, y=d)

    def pokaz_przycisk_graj(self):
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        c = int(0.66 * screen_width)
        d = int(0.76 * screen_height)
        self.przycisk_graj.place(x=c, y=d)

    def pokaz_przycisk_powrot(self):
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        c = int(0.1 * screen_width)
        d = int(0.05 * screen_height)
        self.przycisk_powrot.place(x=c, y=d)

    def ukryj_przycisk_powrot(self):
        self.przycisk_powrot.place_forget()

    def ukryj_przycisk_ogr(self):
        self.przycisk_ogr.place_forget()

    def ukryj_przycisk_graj(self):
        self.przycisk_graj.place_forget()


# Jeżeli odpalamy ten plik bezpośrednio, możemy go przetestować
if __name__ == "__main__":
    root = tk.Tk()

    # Ścieżki do obrazów
    sciezka_do_obrazu1 = "pt0.png"
    sciezka_do_obrazu2 = "pt1.png"
    sciezka_do_obrazu3 = "pt2.png"
    sciezka_do_obrazu4 = "o_grze.png"
    sciezka_do_obrazu5 = "tlo_gry.png"
    sciezka_do_obrazu6 = "red.png"
    sciezka_do_obrazu7 = "blue.png"

    # Ścieżki do dźwięków
    sciezka_do_dzwieku1 = "pt0.wav"
    sciezka_do_dzwieku2 = "pt1.wav"
    sciezka_do_dzwieku3 = "pt2.wav"
    sciezka_do_dzwieku4 = "zamk.wav"
    sciezka_do_dzwieku5 = "wjazd.wav"

    # Tworzymy instancję klasy PrzesuwaneObrazy
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

    root.mainloop()
