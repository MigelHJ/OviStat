import datetime as dt
import customtkinter as ctk
from dateutil.relativedelta import relativedelta
from ctkdateentry import CTkDateEntry


class StatisztikaNezet(ctk.CTkFrame):
    FONT_ENTRY = ("Arial", 15, "bold")

    def __init__(self, master, gyerek_lista=None, **kwargs):
        super().__init__(master, **kwargs)

        self.gyerek_lista = gyerek_lista if gyerek_lista is not None else []
        self.kivalasztott_datum = dt.date.today()

        self.adatok_feldolgozasa()
        self.ui_epites()

    def eletkor_szamitas(self, szul_datum, kiválasztott_datum):
        """Kiszámítja a betöltött életkort két dátum alapján."""
        kulonbseg = relativedelta(kiválasztott_datum, szul_datum)
        return kulonbseg.years

    def adatok_feldolgozasa(self):
        self.osszes_gyerek = len(self.gyerek_lista)
        self.eletkorok = {
            "3 évesnél fiatalabb": 0,
            "3 éves": 0,
            "4 éves": 0,
            "5 éves": 0,
            "6 éves": 0,
            "7 éves": 0,
            "7 évesnél idősebb": 0,
        }
        self.jogok = {
          "Nagycsaládos": 0,
          "SNI (Sajátos Nevelés Igénylésű)": 0,
          "BTM (Beileszkedési, Tanulás, Magatartás)": 0,
          "HH": 0,
          "HHH": 0
        }
       
        self.helyi = 0
        self.bejaros = 0

        for gyerek in self.gyerek_lista:
            if gyerek.get("nagycsalados"):
                self.jogok["Nagycsaládos"] += 1
            if gyerek.get("sni"):
                self.jogok["SNI (Sajátos Nevelés Igénylésű)"]  += 1
            if gyerek.get("btm"):
                self.jogok["BTM (Beileszkedési, Tanulás, Magatartás)"] += 1
            if gyerek.get("hh"):
                self.jogok["HH"] += 1
            if gyerek.get("hhh"):
                self.jogok["HHH"] += 1

            bejaras = str(gyerek.get("bejaras", "")).lower()
            if "velence" in bejaras or "helyi" in bejaras:
                self.helyi += 1
            else:
                self.bejaros += 1

            # --- DÁTUM FELDOLGOZÁS ---
            datum_str = str(gyerek.get("szuletesi_datum", "")).strip()

            if datum_str:
                szul_datum = None
                for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y.%m.%d.", "%Y/%m/%d"):
                    try:
                        szul_datum = dt.datetime.strptime(datum_str, fmt).date()
                        break
                    except ValueError:
                        continue

                if szul_datum:
                    try:
                        eletkor = self.eletkor_szamitas(
                            szul_datum, self.kivalasztott_datum
                        )
                        if eletkor >= 0:
                            if eletkor < 3:
                                self.eletkorok["3 évesnél fiatalabb"] += 1
                            elif eletkor == 3:
                                self.eletkorok["3 éves"] += 1
                            elif eletkor == 4:
                                self.eletkorok["4 éves"] += 1
                            elif eletkor == 5:
                                self.eletkorok["5 éves"] += 1
                            elif eletkor == 6:
                                self.eletkorok["6 éves"] += 1
                            elif eletkor == 7:
                                self.eletkorok["7 éves"] += 1
                            else:
                                self.eletkorok["7 évesnél idősebb"] += 1
                    except Exception:
                        pass

    def ui_epites(self):
        # 1. Cím
        label_cim = ctk.CTkLabel(
            self,
            text="📊 Óvodai Mutatók és Statisztika",
            font=("Segoe UI", 26, "bold"),
        )
        label_cim.pack(pady=(15, 10))

        # 2. Görgethető nézet inicializálása (egyszeri alkalommal)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=600)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tartalom kirajzolása
        self.tartalom_frissitese()

    def datum_valtozott(self, *args):
        """Akkor fut le, amikor a felhasználó kiválaszt egy dátumot a naptárból."""
        datum_str = self.entry_szul_datum.get().strip()

        if datum_str:
            for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y.%m.%d.", "%Y/%m/%d"):
                try:
                    self.kivalasztott_datum = dt.datetime.strptime(
                        datum_str, fmt
                    ).date()
                    # Újraszámlálás és frissítés
                    self.adatok_feldolgozasa()
                    self.tartalom_frissitese()
                    break
                except ValueError:
                    continue

    def tartalom_frissitese(self):
        """Eltávolítja a régi kártyákat és kirajzolja az újakat."""
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        # 1. Összesítő kártyák
        top_frame = ctk.CTkFrame(self.scroll_frame)
        top_frame.pack(fill="x", pady=10)
        self._kartya_kreálás(
            top_frame, "Összes gyerek", str(self.osszes_gyerek), 0, 0
        )
        self._kartya_kreálás(
            top_frame, "Velencei (Helyi)", str(self.helyi), 0, 1
        )
        self._kartya_kreálás(top_frame, "Bejárós", str(self.bejaros), 0, 2)

        # 2. Életkori megoszlás Sorköz (Cím + Dátumválasztó egy vonalban)
        eletkor_fejlec_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=50)
        eletkor_fejlec_frame.pack(fill="x", pady=(20, 10))

        lbl_eletkor = ctk.CTkLabel(
            eletkor_fejlec_frame,
            text="Életkori megoszlás - Vizsgált dátum:",
            font=("Segoe UI", 18, "bold"),
        )
        lbl_eletkor.pack(side="left", padx=(0, 10))

        # Dátumválasztó beágyazása közvetlenül az Életkori megoszlás mellé
        self.entry_szul_datum = CTkDateEntry(
            eletkor_fejlec_frame,
            width=140,
            height=42,
            border_width=0,
            fg_color="transparent",  # Átlátszóvá teszi a külső keret hátterét
            bg_color="transparent"
        )
        self.entry_szul_datum.pack(side="left")

        # Aktuálisan vizsgált dátum értékének beállítása
        mai_str = self.kivalasztott_datum.strftime("%Y.%m.%d")
        self.entry_szul_datum.variable.set(mai_str)

        # Figyelő esemény hozzáadása
        self.entry_szul_datum.variable.trace_add("write", self.datum_valtozott)

        # Életkor kártyák elrendezése
        eletkor_frame = ctk.CTkFrame(self.scroll_frame)
        eletkor_frame.pack(fill="x", pady=5)

        MAX_OSZLOP = 8
        for index, (ev, db) in enumerate(self.eletkorok.items()):
            szazalek = (
                (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
            )
            cimke = ev
            ertek = f"{db} fő ({int(szazalek)}%)"

            rész_sor = index // MAX_OSZLOP
            rész_oszlop = index % MAX_OSZLOP

            self._kartya_kreálás(
                eletkor_frame, cimke, ertek, rész_sor, rész_oszlop
            )

        # 3. Különleges jogállások
        lbl_jogallas = ctk.CTkLabel(
            self.scroll_frame,
            text="Specialitások & Kategóriák",
            font=("Segoe UI", 18, "bold"),
        )
        lbl_jogallas.pack(anchor="w", pady=(20, 10))

        jog_frame = ctk.CTkFrame(self.scroll_frame)
        jog_frame.pack(fill="x", pady=5)


             

        MAX_OSZLOP = 5
        for index, (jog, db) in enumerate(self.jogok.items()):
            szazalek = (
                (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
            )
            cimke = jog
            ertek = f"{db} fő ({int(szazalek)}%)"

            rész_sor = index // MAX_OSZLOP
            rész_oszlop = index % MAX_OSZLOP

            self._kartya_kreálás(
                jog_frame, cimke, ertek, rész_sor, rész_oszlop
            )
       

    def _kartya_kreálás(self, master, cim, ertek, row, col):
        card = ctk.CTkFrame(master)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        master.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(
            card, text=cim, font=("Segoe UI", 13), text_color="gray70"
        ).pack(pady=(10, 2))
        ctk.CTkLabel(card, text=ertek, font=("Segoe UI", 22, "bold")).pack(
            pady=(0, 10)
        )

    def _sor_kirazas(self, master, cim, ertek):
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=8)
        ctk.CTkLabel(row, text=cim, font=("Segoe UI", 15)).pack(side="left")
        szazalek = (
            (ertek / self.osszes_gyerek) * 100 if self.osszes_gyerek > 0 else 0
        )
        ctk.CTkLabel(
            row, text=f"{ertek} fő ({szazalek:.1f}%)", font=("Segoe UI", 15, "bold")
        ).pack(side="right")