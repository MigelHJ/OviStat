import customtkinter as ctk
from gyerek import GyerekAdatlap
from mainpage import MainPage
from statisztika import StatisztikaNezet
import os
import sys
import customtkinter as ctk
import csv

# Meghatározza a program tényleges futási útvonalát (akár EXE, akár sima script)
if getattr(sys, 'frozen', False):
  # getattr-ral kérjük le, így a Pylance nem dob hibát
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  data_path = os.path.dirname(sys.executable)
else:
  base_path = os.path.dirname(os.path.abspath(__file__))
  data_path = base_path

theme_path = os.path.join(base_path, "custom_theme.json")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme_path)


class App(ctk.CTk):

  def __init__(self):
    super().__init__()


    # --- IKON BEÁLLÍTÁSA ---
    icon_path = os.path.join(base_path, "OviStat.ico")
    if os.path.exists(icon_path):
      try:
        self.iconbitmap(icon_path)
      except Exception as e:
        print(f"Ikon betöltési hiba: {e}")
    # -----------------------
    
    self.firststart = True # Jelzi, hogy a fájlbeolvasás még nem történt meg
    self.title("Gyerek Nyilvántartó")
    self.after(10, lambda: self.state("zoomed"))

    # Csak az nyers adatokat tároljuk (dict formátumban), nem a widgeteket!
    self.gyerek_adatok = []
    self.adatfajl = os.path.join(data_path, "gyerek_adatok.csv")

    # Konténer keret a nézeteknek
    self.container = ctk.CTkFrame(self)
    self.container.pack(fill="both", expand=True)

    self.show_mainpage()

  def clear_container(self):
    """Törli a konténer aktuális tartalmát."""
    for widget in self.container.winfo_children():
      widget.destroy()

  def show_mainpage(self):
    """Megjeleníti a fő adatbeviteli oldalt."""
    if self.firststart:
      self.adatok_betoltese_fajlbol(self.adatfajl)
      self.firststart = False  # Jelöljük, hogy a fájlbeolvasás megtörtént
    else:
      self.clear_container()

    self.main_page = MainPage(master=self.container, app_controller=self)
    self.main_page.pack(fill="both", expand=True)

  def show_statisztika(self):
    """Megjeleníti a statisztikai nézetet."""
    # Mielőtt átlépünk, biztonságosan elmentjük az aktuálisan kitöltött mezők állapotát
    if hasattr(self, "main_page"):
        mentes_fn = getattr(self.main_page, "adatok_mentese_memoriaba", None)
        if callable(mentes_fn):
            mentes_fn()

    self.clear_container()

    stat_frame = ctk.CTkFrame(self.container)
    stat_frame.pack(fill="both", expand=True)

    btn_vissza = ctk.CTkButton(
        stat_frame,
        text="← Vissza az Adatbevitelhez",
        font=("Arial", 24, "bold"),
        command=self.show_mainpage,
        height=40,
        width=200
    )
    btn_vissza.pack(anchor="nw", padx=20, pady=(15, 0))

    # Kiszűrjük az üresen hagyott kártyákat a statisztikából
    érvényes_adatok = [d for d in self.gyerek_adatok if d.get("gyerek_neve", "").strip()]

    stat_nezet = StatisztikaNezet(stat_frame, gyerek_lista=érvényes_adatok)
    stat_nezet.pack(fill="both", expand=True, padx=10, pady=10)

  def adatok_betoltese_fajlbol(self, fajlnev="gyerek_adatok.csv"):
    self.gyerek_adatok = []
    try:
      with open(fajlnev, "r", encoding="utf-8", newline="") as file:
        for row in csv.reader(file):
          if not row:
            continue
          row = [value.strip() for value in row]
          if len(row) >= 12:
            values = row[:12]
          elif len(row) >= 7:
            # A korábbi formátum nem tartalmazta a nem, tartósbeteg és
            # étkezés mezőket.
            values = row[:4] + ["", "", ""] + row[4:7] + ["", ""]
          else:
            continue

          self.gyerek_adatok.append({
              "id": values[0],
              "gyerek_neve": values[1],
              "szuletesi_datum": values[2],
              "bejaras": values[3],
              "nem": values[4],
              "tartosbeteg": values[5],
              "etkezes": values[6],
              "nagycsalados": values[7].lower() == "true",
              "sni": values[8].lower() == "true",
              "btm": values[9].lower() == "true",
              "hh": values[10].lower() == "true",
              "hhh": values[11].lower() == "true",
          })
      print(
          f"Adatok sikeresen betöltve a '{fajlnev}' fájlból. Beolvasva:"
          f" {len(self.gyerek_adatok)} gyerek."
      )
    except FileNotFoundError:
      print(f"A(z) '{fajlnev}' fájl még nem létezik.")
    except Exception as e:
      print(f"Hiba a fájl beolvasásakor: {e}")

if __name__ == "__main__":
  app = App()
  app.mainloop()