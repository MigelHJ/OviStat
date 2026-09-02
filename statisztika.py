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
        self.nem_szerinti_eletkorok = {
            "Fiú": {
                "3 évesnél fiatalabb": 0,
                "3 éves": 0,
                "4 éves": 0,
                "5 éves": 0,
                "6 éves": 0,
                "7 éves": 0,
                "7 évesnél idősebb": 0
                },
            "Lány": {
                "3 évesnél fiatalabb": 0,
                "3 éves": 0,
                "4 éves": 0,
                "5 éves": 0,
                "6 éves": 0,
                "7 éves": 0,
                "7 évesnél idősebb": 0
                }            
        }
        self.specialitas = {          
          "Nagycsaládos": 0,
          "SNI (Sajátos Nevelés Igénylésű)": 0,
          "BTM (Beileszkedési, Tanulás, Magatartás)": 0,
          "HH": 0,
          "HHH": 0          
        }

        self.etkezes={
            "Egésznapos": 0,
            "Félnapos": 0,
            "Ételallergiás": 0,
            "Térítés mentes": 0
        }
        
        self.betegseg = {
            "Tartós beteg": 0,
            "Nem tartós beteg": 0,
            "Családban tartós beteg": 0
        }
       
        self.helyi = 0
        self.bejaros = 0

        for gyerek in self.gyerek_lista:
            if gyerek.get("nagycsalados"):
                self.specialitas["Nagycsaládos"] += 1
            if gyerek.get("sni"):
                self.specialitas["SNI (Sajátos Nevelés Igénylésű)"]  += 1
            if gyerek.get("btm"):
                self.specialitas["BTM (Beileszkedési, Tanulás, Magatartás)"] += 1
            if gyerek.get("hh"):
                self.specialitas["HH"] += 1
            if gyerek.get("hhh"):
                self.specialitas["HHH"] += 1

            # --- Étkezési típusok ---
            if gyerek.get("etkezes") == "Egésznapos":
                self.etkezes["Egésznapos"] += 1
            if gyerek.get("etkezes") == "Félnapos":
                self.etkezes["Félnapos"] += 1
            if gyerek.get("etkezes") == "Ételallergiás":
                self.etkezes["Ételallergiás"] += 1
            if gyerek.get("etkezes") == "Térítés mentes":
                self.etkezes["Térítés mentes"] += 1
                
            # --- Betegségek ---
            if gyerek.get("tartosbeteg") == "Tartós beteg":
                self.betegseg["Tartós beteg"] += 1
            if gyerek.get("tartosbeteg") == "Nem tartós beteg":
                self.betegseg["Nem tartós beteg"] += 1
            if gyerek.get("tartosbeteg") == "Családban tartós beteg":
                self.betegseg["Családban tartós beteg"] += 1

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
                        if gyerek.get("nem") == "Fiú":
                            if eletkor >= 0:
                                if eletkor < 3:
                                    self.nem_szerinti_eletkorok["Fiú"]["3 évesnél fiatalabb"] += 1
                                elif eletkor == 3:
                                    self.nem_szerinti_eletkorok["Fiú"]["3 éves"] += 1
                                elif eletkor == 4:
                                    self.nem_szerinti_eletkorok["Fiú"]["4 éves"] += 1
                                elif eletkor == 5:
                                    self.nem_szerinti_eletkorok["Fiú"]["5 éves"] += 1
                                elif eletkor == 6:
                                    self.nem_szerinti_eletkorok["Fiú"]["6 éves"] += 1
                                elif eletkor == 7:
                                    self.nem_szerinti_eletkorok["Fiú"]["7 éves"] += 1
                                else:
                                    self.nem_szerinti_eletkorok["Fiú"]["7 évesnél idősebb"] += 1
                        elif gyerek.get("nem") == "Lány":
                            if eletkor >= 0:
                                if eletkor < 3:
                                    self.nem_szerinti_eletkorok["Lány"]["3 évesnél fiatalabb"] += 1
                                elif eletkor == 3:
                                    self.nem_szerinti_eletkorok["Lány"]["3 éves"] += 1
                                elif eletkor == 4:
                                    self.nem_szerinti_eletkorok["Lány"]["4 éves"] += 1
                                elif eletkor == 5:
                                    self.nem_szerinti_eletkorok["Lány"]["5 éves"] += 1
                                elif eletkor == 6:
                                    self.nem_szerinti_eletkorok["Lány"]["6 éves"] += 1
                                elif eletkor == 7:
                                    self.nem_szerinti_eletkorok["Lány"]["7 éves"] += 1
                                else:
                                    self.nem_szerinti_eletkorok["Lány"]["7 évesnél idősebb"] += 1                        
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

        # 2. Életkori megoszlás Fejléc
        eletkor_fejlec_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=50)
        eletkor_fejlec_frame.pack(fill="x", pady=(20, 10))

        lbl_eletkor = ctk.CTkLabel(
            eletkor_fejlec_frame,
            text="Életkori megoszlás - Vizsgált dátum:",
            font=("Segoe UI", 18, "bold"),
        )
        lbl_eletkor.pack(side="left", padx=(0, 10))

        self.entry_szul_datum = CTkDateEntry(
            eletkor_fejlec_frame,
            width=140,
            height=42,
            border_width=0,
            fg_color="transparent",
            bg_color="transparent"
        )
        self.entry_szul_datum.pack(side="left")

        mai_str = self.kivalasztott_datum.strftime("%Y.%m.%d")
        self.entry_szul_datum.variable.set(mai_str)
        self.entry_szul_datum.variable.trace_add("write", self.datum_valtozott)

        # 3. Nemek szerinti bontás egymás mellett (2 Oszlopos konténer)
        nemek_kontener = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        nemek_kontener.pack(fill="x", pady=10)
        
        # Grid súlyozás, hogy a két oszlop egyenlő széles legyen
        nemek_kontener.grid_columnconfigure(0, weight=1)
        nemek_kontener.grid_columnconfigure(1, weight=1)

        for nem_idx, (nem, korok) in enumerate(self.nem_szerinti_eletkorok.items()):
            nem_osszesen = sum(korok.values())
            nem_szazalek = (nem_osszesen / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0

            # Külön blokk a nemnek (Fiú / Lány)
            nem_blokk = ctk.CTkFrame(nemek_kontener)
            nem_blokk.grid(row=0, column=nem_idx, padx=8, pady=5, sticky="nsew")

            lbl_nem_fejlec = ctk.CTkLabel(
                nem_blokk,
                text=f"{nem}: {nem_osszesen} fő ({int(nem_szazalek)}%)",
                font=("Segoe UI", 16, "bold")
            )
            lbl_nem_fejlec.pack(anchor="center", padx=15, pady=(15, 15))

            # Rács keret a 12 oszlopos felosztásnak
            korok_frame = ctk.CTkFrame(nem_blokk, fg_color="transparent")
            korok_frame.pack(fill="x", padx=5, pady=(0, 10))

            # 12 oszlop beállítása egyenlő súlyozással
            for col in range(12):
                korok_frame.grid_columnconfigure(col, weight=1)

            for index, (ev, db) in enumerate(korok.items()):
                szazalek = (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
                ertek = f"{db} fő ({int(szazalek)}%)"

                if index < 4:
                    # Első 4 kártya: mindegyik 3 oszlop széles (0-3, 3-6, 6-9, 9-12)
                    row = 0
                    col = index * 3
                    span = 3
                else:
                    # Második 3 kártya: mindegyik 4 oszlop széles (0-4, 4-8, 8-12)
                    row = 1
                    col = (index - 4) * 4
                    span = 4

                # Egyedi kártya létrehozása a megadott fesztávval (span)
                card = ctk.CTkFrame(korok_frame)
                card.grid(row=row, column=col, columnspan=span, padx=4, pady=4, sticky="nsew")
                
                ctk.CTkLabel(
                    card, text=ev, font=("Segoe UI", 13), text_color="gray70"
                ).pack(pady=(10, 2))
                ctk.CTkLabel(card, text=ertek, font=("Segoe UI", 18, "bold")).pack(
                    pady=(0, 10)
                )

        # 4. Különleges jogállások
        lbl_jogallas = ctk.CTkLabel(
            self.scroll_frame,
            text="Specialitások & Kategóriák",
            font=("Segoe UI", 18, "bold")
        )
        lbl_jogallas.pack(anchor="w", pady=(20, 10))

        jog_frame = ctk.CTkFrame(self.scroll_frame)
        jog_frame.pack(fill="x", pady=5)

        MAX_OSZLOP_JOG = 5
        for index, (jog, db) in enumerate(self.specialitas.items()):
            szazalek = (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
            ertek = f"{db} fő ({int(szazalek)}%)"

            sor = index // MAX_OSZLOP_JOG
            oszlop = index % MAX_OSZLOP_JOG

            self._kartya_kreálás(
                jog_frame, jog, ertek, sor, oszlop
            )
       
       # 5. Étkezési típusok
        lbl_etkezes = ctk.CTkLabel(
            self.scroll_frame,
            text="Étkezési típusok",
            font=("Segoe UI", 18, "bold")
        )
        lbl_etkezes.pack(anchor="w", pady=(20, 10))
        
        etkezes_frame = ctk.CTkFrame(self.scroll_frame)
        etkezes_frame.pack(fill="x", pady=5)
        
        MAX_OSZLOP_ETKEZES = 4
        for index, (tipus, db) in enumerate(self.etkezes.items()):
            szazalek = (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
            ertek = f"{db} fő ({int(szazalek)}%)"

            sor = index // MAX_OSZLOP_ETKEZES
            oszlop = index % MAX_OSZLOP_ETKEZES

            self._kartya_kreálás(
                etkezes_frame, tipus, ertek, sor, oszlop
            )
            
        # 6. Betegségek
        lbl_betegseg = ctk.CTkLabel(
            self.scroll_frame,
            text="Tartósbetegségek",
            font=("Segoe UI", 18, "bold")
        )
        lbl_betegseg.pack(anchor="w", pady=(20, 10))
        
        betegseg_frame = ctk.CTkFrame(self.scroll_frame)
        betegseg_frame.pack(fill="x", pady=5)
        
        MAX_OSZLOP_BETEGSEG = 3
        for index, (betegseg, db) in enumerate(self.betegseg.items()):
            szazalek = (db / self.osszes_gyerek * 100) if self.osszes_gyerek > 0 else 0
            ertek = f"{db} fő ({int(szazalek)}%)"

            sor = index // MAX_OSZLOP_BETEGSEG
            oszlop = index % MAX_OSZLOP_BETEGSEG

            self._kartya_kreálás(
                betegseg_frame, betegseg, ertek, sor, oszlop
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