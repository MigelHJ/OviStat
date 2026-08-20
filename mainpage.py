import customtkinter as ctk
from alert import AlertPopup
from gyerek import GyerekAdatlap


class MainPage(ctk.CTkFrame):

  def __init__(self, master, app_controller, **kwargs):
    super().__init__(master, **kwargs)
    self.app_controller = app_controller
    self.gyerek_lista = []  # Ebben a MainPage-ben lévő Adatlap widgetek

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    FONT_MAIN_BTN = ("Arial", 16, "bold")

  # --- 1. Gördíthető Lista Terület ---
    self.scrollable_frame = ctk.CTkScrollableFrame(self)
    self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    self.scrollable_frame.grid_columnconfigure(0, weight=1)

    # --- Hozzáadás gomb a lista alján ---
    self.btn_hozzaadas_inline = ctk.CTkButton(
        self.scrollable_frame,  # Javítva: eltávolítva a felesleges self,
        text="+ Új gyerek hozzáadása",
        fg_color="green",
        hover_color="darkgreen",
        height=50,
        width=300,
        font=("Arial", 17, "bold"),
        command=self.gyerek_hozzaadasa,
    )

  # --- 2. Alsó Vezérlőgombok ---
    self.bottom_button_frame = ctk.CTkFrame(self, corner_radius=8, height=70)
    self.bottom_button_frame.grid(
        row=1, column=0, sticky="ew", padx=20, pady=(5, 20)
    )

    self.btn_kiiras = ctk.CTkButton(
        self.bottom_button_frame,
        text="Statisztikák és Kimutatások",
        fg_color="#555555",
        hover_color="#333333",
        height=48,
        font=FONT_MAIN_BTN,
        command=self.app_controller.show_statisztika,
    )
    self.btn_kiiras.pack(side="left", padx=10, pady=10)

  # --- Mentés gomb ---
    self.btn_mentes = ctk.CTkButton(
        self.bottom_button_frame,
        text="💾 Mentés",
        fg_color="#4CAF50",
        hover_color="#388E3C",
        height=48,
        font=FONT_MAIN_BTN,
        command=self.osszes_mentese,
    )
    self.btn_mentes.pack(side="right", padx=10, pady=10)

    self.btn_torles = ctk.CTkButton(
        self.bottom_button_frame,
        text="Összes Törlése",
        fg_color="#D32F2F",
        hover_color="#9A0007",
        height=48,
        font=FONT_MAIN_BTN,
        command=self.osszes_torlese,
    )
    self.btn_torles.pack(side="right", padx=10, pady=10)

  # --- 3. Kártyák felépítése a memóriában lévő adatokból ---
    self.kartyat_felepit_adatokbol()


  def kartyat_felepit_adatokbol(self):
      """Létrehozza a kártyákat a memóriában lévő adatokból."""
      if not self.app_controller.gyerek_adatok:
        self.gyerek_hozzaadasa()
      else:
        for adat in self.app_controller.gyerek_adatok:
          gyerek_id = adat.get("id")
          elem = GyerekAdatlap(master=self.scrollable_frame, gyerek_id=gyerek_id)

        # 1. Név feltöltése (töröljük az esetleges alapértelmezést, majd beírjuk)
          elem.entry_nev.delete(0, "end")
          elem.entry_nev.insert(0, adat.get("gyerek_neve", ""))

        # 2. Születési dátum feltöltése
          datum = adat.get("szuletesi_datum", "")
          if datum:
            elem.entry_szul_datum.variable.set(str(datum))
            
            # Biztosítjuk, hogy az Entry mezőben is megjelenjen a szöveg
            elem.entry_szul_datum.entry.delete(0, "end")
            elem.entry_szul_datum.entry.insert(0, str(datum))

        # 3. Bejárás dropdown
          if "bejaras" in adat and adat["bejaras"]:
            elem.dropdown_bejaras.set(str(adat["bejaras"]))

        # 4. Checkboxok (biztosítjuk a Bool típust)
          elem.var_nagycsalados.set(
              str(adat.get("nagycsalados", "")).lower() == "true"
          )
          elem.var_sni.set(str(adat.get("sni", "")).lower() == "true")
          elem.var_btm.set(str(adat.get("btm", "")).lower() == "true")

          elem.grid(
              row=len(self.gyerek_lista),
              column=0,
              padx=5,
              pady=3,
              sticky="ew",
          )
          self.gyerek_lista.append(elem)

      self.gomb_pozicionalasa()


  def adatok_mentese_memoriaba(self):
    """Menti a felületen lévő kártyák aktuális tartalmát a memóriába."""
    self.app_controller.gyerek_adatok = [
        elem.adat_lekeres() for elem in self.gyerek_lista
    ]

  def osszes_mentese(self):
    """Végigmegy az összes kártyán, leellenőrzi őket, és ha nincs hiba, menti a CSV-be."""

  # 1. Minden kártyán külön lefut a dátumellenőrzés (ha van egyáltalán kártya)
    van_hiba = False
    for kartya in self.gyerek_lista:
      if not kartya.datum_ellenorzes():
        van_hiba = True

    # Ha bármelyik kártya dátuma hibás volt, leállunk
    if van_hiba:
      return

  # 2. Megerősítés kérése (akkor is rákérdez, ha 0 kártya van!)
    popup = AlertPopup(
        master=self.winfo_toplevel(),
        message=(
            "Biztosan menteni szeretnéd a jelenlegi állapotot a fájlba?"
        ),
        szelesseg=520,
        magassag=220,
    )
    self.wait_window(popup)

  # 3. CSV fájl felülírása (ha üres a lista, üres fájlt ment el)
    if popup.eredmeny:
      try:
        with open("gyerek_adatok.csv", "w", encoding="utf-8") as file:
          for kartya in self.gyerek_lista:
            data = kartya.adat_lekeres()
            line = f"{data['id']},{data['gyerek_neve']},{data['szuletesi_datum']},{data['bejaras']},{data['nagycsalados']},{data['sni']},{data['btm']}\n"
            file.write(line)

        self.adatok_mentese_memoriaba()
        print("Minden változtatás (akár a teljes törlés is) sikeresen mentve.")
      except Exception as e:
        print(f"Hiba történt a mentés során: {e}")
          
          
  def gomb_pozicionalasa(self):
    self.btn_hozzaadas_inline.grid(
        row=len(self.gyerek_lista), column=0, padx=10, pady=20, sticky="n"
    )


  def gyerek_hozzaadasa(self):
    elem = GyerekAdatlap(master=self.scrollable_frame)
    elem.grid(
        row=len(self.gyerek_lista), column=0, padx=5, pady=3, sticky="ew"
    )
    self.gyerek_lista.append(elem)
    self.gomb_pozicionalasa()


  def lista_frissitese(self):
    for i, elem in enumerate(self.gyerek_lista):
      elem.grid(row=i, column=0, padx=5, pady=6, sticky="ew")
    self.gomb_pozicionalasa()


  def osszes_torlese(self):
    popup = AlertPopup(
        master=self.winfo_toplevel(),
        message="Biztosan törölni szeretnéd az összes gyerek adatlapját?",
        szelesseg=520,
        magassag=220,
    )
    self.wait_window(popup)
    if popup.eredmeny:
      for elem in self.gyerek_lista:
        elem.destroy()
      self.gyerek_lista.clear()
      self.app_controller.gyerek_adatok.clear()
      self.gomb_pozicionalasa()