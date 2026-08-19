import datetime as dt
import customtkinter as ctk


class StatisztikaNezet(ctk.CTkFrame):

  def __init__(self, master, gyerek_lista=None, **kwargs):
    super().__init__(master, **kwargs)

    self.gyerek_lista = gyerek_lista if gyerek_lista is not None else []

    self.adatok_feldolgozasa()
    self.ui_epites()

  def adatok_feldolgozasa(self):
    self.osszes_gyerek = len(self.gyerek_lista)
    self.eletkorok = {}
    self.nagycsalados = 0
    self.sni = 0
    self.btm = 0
    self.helyi = 0
    self.bejaros = 0

    mai_nap = dt.date.today()

    for gyerek in self.gyerek_lista:
      if gyerek.get("nagycsalados"):
        self.nagycsalados += 1
      if gyerek.get("sni"):
        self.sni += 1
      if gyerek.get("btm"):
        self.btm += 1

      bejaras = str(gyerek.get("bejaras", "")).lower()
      if "velence" in bejaras or "helyi" in bejaras:
        self.helyi += 1
      else:
        self.bejaros += 1

      # --- JAVÍTOTT DÁTUM FELDOLGOZÁS ---
      datum_str = str(gyerek.get("szuletesi_datum", "")).strip()

      if datum_str:
        szul_datum = None
        # Kipróbáljuk a leggyakoribb formátumokat
        for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y.%m.%d.", "%Y/%m/%d"):
          try:
            szul_datum = dt.datetime.strptime(datum_str, fmt).date()
            break
          except ValueError:
            continue

        if szul_datum:
          try:
            # Betöltött évek kiszámítása
            eletkor = (
                mai_nap.year
                - szul_datum.year
                - (
                    (mai_nap.month, mai_nap.day)
                    < (szul_datum.month, szul_datum.day)
                )
            )
            if eletkor >= 0:
              self.eletkorok[eletkor] = self.eletkorok.get(eletkor, 0) + 1
          except Exception:
            pass

  def ui_epites(self):
    label_cim = ctk.CTkLabel(
        self,
        text="📊 Óvodai Mutatók és Statisztika",
        font=("Segoe UI", 26, "bold"),
    )
    label_cim.pack(pady=(20, 15))

    scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=600)
    scroll_frame.pack(padx=20, pady=15, fill="both", expand=True)

    # 1. Összesítő kártyák
    top_frame = ctk.CTkFrame(scroll_frame)
    top_frame.pack(fill="x", pady=10)
    self._kartya_kreálás(
        top_frame, "Összes gyerek", str(self.osszes_gyerek), 0, 0
    )
    self._kartya_kreálás(top_frame, "Velencei (Helyi)", str(self.helyi), 0, 1)
    self._kartya_kreálás(top_frame, "Bejárós", str(self.bejaros), 0, 2)

    # 2. Életkori megoszlás
    lbl_eletkor = ctk.CTkLabel(
        scroll_frame,
        text="Életkori megoszlás (betöltött év)",
        font=("Segoe UI", 18, "bold"),
    )
    lbl_eletkor.pack(anchor="w", pady=(25, 10))

    eletkor_frame = ctk.CTkFrame(scroll_frame)
    eletkor_frame.pack(fill="x", pady=5)

    for ev in sorted(self.eletkorok.keys()):
      db = self.eletkorok[ev]
      szazalek = db / self.osszes_gyerek if self.osszes_gyerek > 0 else 0

      row = ctk.CTkFrame(eletkor_frame, fg_color="transparent")
      row.pack(fill="x", padx=15, pady=8)

      lbl_ev = ctk.CTkLabel(
          row, text=f"{ev} éves:", font=("Segoe UI", 15, "bold"), width=90, anchor="w"
      )
      lbl_ev.pack(side="left")

      progress = ctk.CTkProgressBar(row, height=16)
      progress.set(szazalek)
      progress.pack(side="left", fill="x", expand=True, padx=15)

      lbl_db = ctk.CTkLabel(
          row,
          text=f"{db} fő ({int(szazalek*100)}%)",
          font=("Segoe UI", 15),
          width=110,
          anchor="e",
      )
      lbl_db.pack(side="right")

    # 3. Különleges jogállások
    lbl_jogallas = ctk.CTkLabel(
        scroll_frame,
        text="Specialitások & Kategóriák",
        font=("Segoe UI", 18, "bold"),
    )
    lbl_jogallas.pack(anchor="w", pady=(25, 10))

    jog_frame = ctk.CTkFrame(scroll_frame)
    jog_frame.pack(fill="x", pady=5)

    self._sor_kirazas(jog_frame, "👨‍👩‍👧‍👦 Nagycsaládosok:", self.nagycsalados)
    self._sor_kirazas(
        jog_frame, "🧩 SNI (Sajátos nevelési igényű):", self.sni
    )
    self._sor_kirazas(
        jog_frame,
        "📘 BTMN (Beilleszkedési, tanulási, magatartási nehézségek):",
        self.btm,
    )

  def _kartya_kreálás(self, master, cim, ertek, row, col):
    card = ctk.CTkFrame(master)
    card.grid(row=row, column=col, padx=12, pady=12, sticky="ew")
    master.grid_columnconfigure(col, weight=1)
    ctk.CTkLabel(
        card, text=cim, font=("Segoe UI", 14), text_color="gray70"
    ).pack(pady=(12, 2))
    ctk.CTkLabel(card, text=ertek, font=("Segoe UI", 26, "bold")).pack(
        pady=(0, 12)
    )

  def _sor_kirazas(self, master, cim, ertek):
    row = ctk.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", padx=15, pady=10)
    ctk.CTkLabel(row, text=cim, font=("Segoe UI", 15)).pack(side="left")
    szazalek = (
        (ertek / self.osszes_gyerek) * 100 if self.osszes_gyerek > 0 else 0
    )
    ctk.CTkLabel(
        row, text=f"{ertek} fő ({szazalek:.1f}%)", font=("Segoe UI", 15, "bold")
    ).pack(side="right")