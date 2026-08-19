import customtkinter as ctk
from gyerek import GyerekAdatlap
from mainpage import MainPage
from statisztika import StatisztikaNezet

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("custom_theme.json")


class App(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.firststart = True # Jelzi, hogy a fájlbeolvasás még nem történt meg
    self.title("Gyerek Nyilvántartó")
    self.after(10, lambda: self.state("zoomed"))

    # Csak az nyers adatokat tároljuk (dict formátumban), nem a widgeteket!
    self.gyerek_adatok = []

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
      self.adatok_betoltese_fajlbol("gyerek_adatok.csv")
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
        font=("Arial", 14, "bold"),
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
      with open(fajlnev, "r", encoding="utf-8") as file:
        for line in file:
          sor = line.strip()
          if sor:
            adatok = sor.split(",")
            # Ha megvan a 7 mező (id, név, dátum, bejárás, nagycsaládos, sni, btm)
            if len(adatok) >= 7:
              self.gyerek_adatok.append({
                  "id": adatok[0].strip(),
                  "gyerek_neve": adatok[1].strip(),
                  "szuletesi_datum": adatok[2].strip(),
                  "bejaras": adatok[3].strip(),
                  "nagycsalados": adatok[4].strip().lower() == "true",
                  "sni": adatok[5].strip().lower() == "true",
                  "btm": adatok[6].strip().lower() == "true",
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