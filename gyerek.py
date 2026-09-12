import datetime as dt
from typing import TYPE_CHECKING, cast
import uuid
import csv
from alert import AlertPopup
from ctkdateentry import CTkDateEntry
import customtkinter as ctk

if TYPE_CHECKING:
  from main import App


class GyerekAdatlap(ctk.CTkFrame):

  def __init__(self, master, gyerek_id=None, **kwargs):
    super().__init__(master, **kwargs)

    # Rejtett azonosító (GUI-n nem jelenik meg)
    self.id = gyerek_id if gyerek_id else str(uuid.uuid4())

    # Jelzi, hogy történt-e már mentési kísérlet
    self.mentes_megtortent = False

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(1, weight=0)
    self.grid_columnconfigure(2, weight=0)
    self.grid_columnconfigure(3, weight=0)
    self.grid_columnconfigure(4, weight=0)
    self.grid_columnconfigure(5, weight=0)
    self.grid_columnconfigure(6, weight=0)
    self.grid_columnconfigure(7, weight=1)
    self.grid_columnconfigure(8, weight=0)
    

    FONT_ENTRY = ("Arial", 15, "bold")
    FONT_CHECK = ("Arial", 14, "bold")
    FONT_ERROR = ("Arial", 12, "bold")

    # --- 1. Gyerek neve ---
    self.entry_nev = ctk.CTkEntry(
        self,
        placeholder_text="Gyerek neve...",
        width=250,
        height=42,
        font=FONT_ENTRY,
    )
    self.entry_nev.grid(row=1, column=1, padx=8, pady=12, sticky="ew")

    # --- 2. Születési dátum ---
    self.entry_szul_datum = CTkDateEntry(
        self, width=150, height=42, font=FONT_ENTRY
    )
    self.entry_szul_datum.grid(row=1, column=2, padx=8, pady=12)

    # --- 3. Dropdownok ---
    bejaras_opciok = [
        "Velence",
        "Kápolnásnyék",
        "Gárdony",
        "Agárd",
        "Sukoró",
        "Pázmánd",
        "Pákozd",
        "Bejárós (egyéb)",
    ]
    
    nem_opciok = [
        "Fiú",
        "Lány",
    ]
    
    tartosbeteg_opciok = [
      "Tartós beteg",
      "Nem tartós beteg",
      "Családban tartós beteg",
    ]
    
    etkezesi_opciok = [
      "Egésznapos",
      "Félnapos",
      "Ételallergiás",
      "Térítés mentes"
    ]
    
    self.dropdown_bejaras = ctk.CTkOptionMenu(
        self,
        values=bejaras_opciok,
        width=160,
        height=42,
        font=FONT_ENTRY,
        dropdown_font=FONT_ENTRY
    )
    self.dropdown_bejaras.grid(row=1, column=3, padx=8, pady=12)

    self.dropdown_nem = ctk.CTkOptionMenu(
        self,
        values=nem_opciok,
        width=160,
        height=42,
        font=FONT_ENTRY,
        dropdown_font=FONT_ENTRY
    )
    self.dropdown_nem.grid(row=1, column=4, padx=8, pady=12)

    self.dropdown_tartosbeteg = ctk.CTkOptionMenu(
        self,
        values=tartosbeteg_opciok,
        width=160,
        height=42,
        font=FONT_ENTRY,
        dropdown_font=FONT_ENTRY
    )
    self.dropdown_tartosbeteg.grid(row=1, column=5, padx=8, pady=12)
    
    self.dropdown_etkezes = ctk.CTkOptionMenu(
        self,
        values=etkezesi_opciok,
        width=160,
        height=42,
        font=FONT_ENTRY,
        dropdown_font=FONT_ENTRY
    )
    self.dropdown_etkezes.grid(row=1, column=6, padx=8, pady=12)
    

    # --- 4. Jelölőnégyzetek ---
    self.var_nagycsalados = ctk.BooleanVar(value=False)
    self.chk_nagycsalados = ctk.CTkCheckBox(
        self,
        text="Nagycsaládos",
        variable=self.var_nagycsalados,
        checkbox_width=28,
        checkbox_height=28,
        font=FONT_CHECK,
    )
    
    self.chk_nagycsalados.grid(row=2, column=1, padx=12, pady=12)

    self.var_sni = ctk.BooleanVar(value=False)
    self.chk_sni = ctk.CTkCheckBox(
        self,
        text="SNI",
        variable=self.var_sni,
        checkbox_width=28,
        checkbox_height=28,
        font=FONT_CHECK,
    )
    self.chk_sni.grid(row=2, column=2, padx=12, pady=12)

    self.var_btm = ctk.BooleanVar(value=False)
    self.chk_btm = ctk.CTkCheckBox(
        self,
        text="BTM",
        variable=self.var_btm,
        checkbox_width=28,
        checkbox_height=28,
        font=FONT_CHECK,
    )
    self.chk_btm.grid(row=2, column=3, padx=(12, 16), pady=12)
    
    self.var_HH = ctk.BooleanVar(value=False)
    self.chk_HH = ctk.CTkCheckBox(
            self,
            text="HH",
            variable=self.var_HH,
            checkbox_width=28,
            checkbox_height=28,
            font=FONT_CHECK,
        )
    self.chk_HH.grid(row=2, column=4, padx=(12, 16), pady=12)
        
    self.var_HHH = ctk.BooleanVar(value=False)
    self.chk_HHH = ctk.CTkCheckBox(
            self,
            text="HHH",
            variable=self.var_HHH,
            checkbox_width=28,
            checkbox_height=28,
            font=FONT_CHECK,
        )
    self.chk_HHH.grid(row=2, column=5, padx=(12, 16), pady=12)

   
    # --- Mentés gomb ---
    self.btn_mentes = ctk.CTkButton(
        self,
        text="💾 Mentés",
        fg_color="#4CAF50",
        hover_color="#388E3C",
        height=42,
        width=110,
        font=FONT_ENTRY,
        command=lambda: self.fajlba_mentes("gyerek_adatok.csv"),
    )
    self.btn_mentes.grid(row=1, rowspan=2, column=7, padx=8, pady=12, sticky="e")

    # --- 6. Törlés Gomb ---
    self.btn_torles = ctk.CTkButton(
        self,
        text="Törlés",
        fg_color="#D32F2F",
        hover_color="#9A0007",
        height=42,
        width=110,
        font=FONT_ENTRY,
        command=self.torles,
    )
    self.btn_torles.grid(row=1, rowspan=2, column=8, padx=8, pady=12, sticky="e")

  def adat_lekeres(self):
    return {
        "id": self.id,
        "gyerek_neve": self.entry_nev.get(),
        "szuletesi_datum": self.entry_szul_datum.variable.get(),
        "bejaras": self.dropdown_bejaras.get(),
        "nem": self.dropdown_nem.get(),
        "tartosbeteg": self.dropdown_tartosbeteg.get(),
        "etkezes": self.dropdown_etkezes.get(),
        "nagycsalados": self.var_nagycsalados.get(),
        "sni": self.var_sni.get(),
        "btm": self.var_btm.get(),
        "hh": self.var_HH.get(),
        "hhh": self.var_HHH.get(),
    }

  def datum_ellenorzes(self) -> bool:
      """Ellenőrzi a kártya saját dátumát. Ha hibás, kiírja a piros szöveget."""
      self.mentes_megtortent = True
      datum_str = str(self.entry_szul_datum.variable.get()).strip()

      szul_datum = None
      for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
          szul_datum = dt.datetime.strptime(datum_str, fmt).date()
          break
        except ValueError:
          continue
 
      return True
  
  def fajlba_mentes(self, fajlnev):
    """Elmenti az ÖSSZES gyerek kártyájának adatát a fájlba, miután felülvizsgálta a dátumokat."""
    top_level = self.winfo_toplevel()
    main_page = getattr(top_level, "main_page", None)

    # Megkeressük az összes gyerek kártyát a felületen
    gyerek_lista = []
    if main_page is not None and hasattr(main_page, "app_controller"):
      controller = getattr(main_page, "app_controller")
      if hasattr(main_page, "gyerek_lista"):
        gyerek_lista = main_page.gyerek_lista

    if not gyerek_lista:
      gyerek_lista = [self]

    # Minden kártyán bekapcsoljuk a hibaellenőrzést és megvizsgáljuk a dátumot
    van_hibas_datum = False
    for kartya in gyerek_lista:
      kartya.mentes_megtortent = True
      if not kartya.datum_ellenorzes():
        van_hibas_datum = True

    # Ha akár egyetlen kártyán is hibás vagy üres a dátum, megszakítjuk a mentést
    if van_hibas_datum:
      return

    # Megerősítő ablak
    popup = AlertPopup(
        master=self.winfo_toplevel(),
        message=(
            "Biztosan menteni szeretnéd az összes gyerek adatlapját a fájlba?"
        ),
        szelesseg=520,
        magassag=220,
    )
    self.wait_window(popup)

    if popup.eredmeny:
      try:
        adatfajl = getattr(
            getattr(main_page, "app_controller", None),
            "adatfajl",
            fajlnev,
        )
        with open(adatfajl, "w", encoding="utf-8", newline="") as file:
          writer = csv.writer(file, lineterminator="\n")
          for kartya in gyerek_lista:
            data = kartya.adat_lekeres()
            if data["gyerek_neve"].strip():
              writer.writerow([
                  data["id"], data["gyerek_neve"], data["szuletesi_datum"],
                  data["bejaras"], data["nem"], data["tartosbeteg"],
                  data["etkezes"], data["nagycsalados"], data["sni"],
                  data["btm"], data["hh"], data["hhh"],
              ])

        if main_page and hasattr(main_page, "adatok_mentese_memoriaba"):
          main_page.adatok_mentese_memoriaba()

        print(f"Az összes adat sikeresen mentve a '{fajlnev}' fájlba.")
      except Exception as e:
        print(f"Hiba történt a fájl mentése közben: {e}")


  def torles(self):
    """Törli az adott kártyát a felületről és a MainPage gyerek_lista tömbjéből."""
    popup = AlertPopup(
        master=self.winfo_toplevel(),
        message="Biztosan törölni szeretnéd ezt a gyerek adatlapját?",
        szelesseg=520,
        magassag=220,
    )
    self.wait_window(popup)

    if popup.eredmeny:
      top_level = self.winfo_toplevel()
      main_page = getattr(top_level, "main_page", None)

      # 1. Töröljük a kártyát a MainPage saját gyerek_lista tömbjéből!
      if main_page is not None and hasattr(main_page, "gyerek_lista"):
        if self in main_page.gyerek_lista:
          main_page.gyerek_lista.remove(self)

      # 2. Megsemmisítjük a felületi elemet
      self.destroy()

      # 3. Frissítjük a megmaradt kártyák pozícióját a felületen
      if main_page is not None and hasattr(main_page, "lista_frissitese"):
        main_page.lista_frissitese()