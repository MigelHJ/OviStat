import customtkinter as ctk
from alert import AlertPopup

class GyerekAdatlap(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
    # A oszlopok méretezése
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=0)
        self.grid_columnconfigure(7, weight=1)

    # --- 1. Gyerek neve ---
        self.entry_nev = ctk.CTkEntry(self, placeholder_text="Gyerek neve...", width=350)
        self.entry_nev.grid(row=0, column=1, padx=5, pady=8)

    # --- 2. Születési dátum ---
        self.entry_szul_datum = ctk.CTkEntry(self, placeholder_text="ÉÉÉÉ.MM.DD", width=150)
        self.entry_szul_datum.bind("<FocusOut>", lambda event: self.datum_ellenorzes())
        self.entry_szul_datum.grid(row=0, column=2, padx=5, pady=8)

    # --- 3. Bejárás ---
        bejaras_opciok = [
            "Velencei", "Kápolnásnyék", "Gárdony", 
            "Agárd", "Sukoró", "Pázmánd", "Pákozd", "Bejárós (egyéb)"
        ]
        self.dropdown_bejaras = ctk.CTkOptionMenu(self, values=bejaras_opciok, width=130)
        self.dropdown_bejaras.grid(row=0, column=3, padx=5, pady=8)

    # --- 4. Jelölőnégyzetek ---
        self.var_nagycsalados = ctk.BooleanVar(value=False)
        self.chk_nagycsalados = ctk.CTkCheckBox(self, text="Nagycsaládos", variable=self.var_nagycsalados, checkbox_width=20, checkbox_height=20)
        self.chk_nagycsalados.grid(row=0, column=4, padx=8, pady=8)

        self.var_sni = ctk.BooleanVar(value=False)
        self.chk_sni = ctk.CTkCheckBox(self, text="SNI", variable=self.var_sni, checkbox_width=20, checkbox_height=20)
        self.chk_sni.grid(row=0, column=5, padx=8, pady=8)

        self.var_btm = ctk.BooleanVar(value=False)
        self.chk_btm = ctk.CTkCheckBox(self, text="BTM", variable=self.var_btm, checkbox_width=20, checkbox_height=20)
        self.chk_btm.grid(row=0, column=6, padx=(8, 10), pady=8)

    # --- 5. Törlés Gomb ---
        self.btn_torles = ctk.CTkButton(self, text="Törlés", fg_color="red", command=self.torles)
        self.btn_torles.grid(row=0, column=7, padx=5, pady=8, sticky="e")
        
        

    def adat_lekeres(self):
        """Visszaadja a sorban megadott adatokat szótár (dictionary) formájában."""
        return {
            "gyerek_neve": self.entry_nev.get(),
            "szuletesi_datum": self.entry_szul_datum.get(),
            "bejaras": self.dropdown_bejaras.get(),
            "nagycsalados": self.var_nagycsalados.get(),
            "sni": self.var_sni.get(),
            "btm": self.var_btm.get()
        }
    
    def datum_ellenorzes(self):
        """Ellenőrzi, hogy a születési dátum helyes formátumban van-e (ÉÉÉÉ.MM.NN)."""
        datum = self.entry_szul_datum.get()
        if len(datum) != 10 or datum[4] != '.' or datum[7] != '.':
            return False
        ev, honap, nap = datum.split('.')
        if not (ev.isdigit() and honap.isdigit() and nap.isdigit()):
            return False
        ev, honap, nap = int(ev), int(honap), int(nap)
        if not (1 <= honap <= 12 and 1 <= nap <= 31):
            return False
        return True
    
    def torles(self, szelesseg=400, magassag=150):
        """Törli az adatlapot a GUI-ból."""
        popup = AlertPopup(master=self, message="Biztosan törölni szeretnéd ezt a gyerek adatlapját?", szelesseg=450, magassag=150)
        self.wait_window(popup)
        if popup.eredmeny:  # Ha az OK gombot nyomták meg 
            self.destroy()  