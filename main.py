import customtkinter as ctk
from gyerek import GyerekAdatlap
from alert import AlertPopup

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("custom_theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gyerek Nyilvántartó")
        self.after(10, lambda: self.state("zoomed"))
        
        self.elemek_listaja = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # Font-rendszer a felülethez
        FONT_MAIN_BTN = ("Arial", 16, "bold")

    # --- 1. Gördíthető Lista Terület ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    # --- Hozzáadás gomb a lista alján ---
        self.btn_hozzaadas_inline = ctk.CTkButton(
            self.scrollable_frame,           
            text="+ Új gyerek hozzáadása",
            fg_color="green",
            hover_color="darkgreen",
            height=50,
            width=300,
            anchor="center",
            font=("Arial", 17, "bold"),
            command=self.gyerek_hozzaadasa
        )

    # --- 2. Alsó Vezérlőgombok ---
        self.bottom_button_frame = ctk.CTkFrame(self, corner_radius=8, height=70)
        self.bottom_button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 20))

        # --- 2.1 Adatok Nyomtatása (Console) ---
        self.btn_kiiras = ctk.CTkButton(
            self.bottom_button_frame, 
            text="Adatok Nyomtatása (Console)", 
            fg_color="#555555", 
            hover_color="#333333",
            height=48,
            font=FONT_MAIN_BTN,
            command=self.adatok_kiirasa
        )
        self.btn_kiiras.pack(side="left", padx=10, pady=10)
        
        # --- 2.2 Mentés ---
        self.btn_mentes = ctk.CTkButton(
            self.bottom_button_frame, 
            text="Mentés Fájlba", 
            fg_color="#1E88E5", 
            hover_color="#1565C0",
            height=48,
            font=FONT_MAIN_BTN,
            command=lambda: self.fajlba_mentes("gyerek_adatok.csv")
        )
        self.btn_mentes.pack(side="right", padx=10, pady=10)

        # --- 2.3 Összes Törlése ---
        self.btn_torles = ctk.CTkButton(
            self.bottom_button_frame, 
            text="Összes Törlése", 
            fg_color="#D32F2F", 
            hover_color="#9A0007",
            height=48,
            font=FONT_MAIN_BTN,
            command=self.osszes_torlese
        )
        self.btn_torles.pack(side="right", padx=10, pady=10)
        
    # Adatok betöltése
        self.fajlbol_betoltes("gyerek_adatok.csv")

        if not self.elemek_listaja:
            self.gyerek_hozzaadasa()
        else:
            self.gomb_pozicionalasa()


# ---- 3. Funkciók ----
    def gomb_pozicionalasa(self):
        self.btn_hozzaadas_inline.grid(
            row=len(self.elemek_listaja),
            column=0,
            padx=10,
            pady=20,
            sticky="n"
        )

    def gyerek_hozzaadasa(self):
        elem = GyerekAdatlap(master=self.scrollable_frame)        
        self.elemek_listaja.append(elem)
        self.gomb_pozicionalasa()

    def lista_frissitese(self):
        for i, elem in enumerate(self.elemek_listaja):
            elem.grid(row=i, column=0, padx=5, pady=6, sticky="ew")
        self.gomb_pozicionalasa()

    def adatok_kiirasa(self):
        print("\n================ RENDSZERBEN LÉVŐ ADATOK ================")
        for elem in self.elemek_listaja:
            if elem.winfo_exists():
                print(elem.adat_lekeres())

    def osszes_torlese(self):
        popup = AlertPopup(
            master=self, 
            message="Biztosan törölni szeretnéd az összes gyerek adatlapját?", 
            szelesseg=520, 
            magassag=220
        )
        self.wait_window(popup)
        if popup.eredmeny:
            for elem in self.elemek_listaja:
                elem.destroy()
            self.elemek_listaja.clear()
            self.gomb_pozicionalasa()
        
    def fajlbol_betoltes(self, fajlnev):
        try:
            with open(fajlnev, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 6:
                        elem = GyerekAdatlap(master=self.scrollable_frame)
                        elem.entry_nev.insert(0, data[0])
                        
                        # --- DÁTUM BIZTONSÁGOS BEÁLLÍTÁSA ---
                        # main.py - fajlbol_betoltes() belseje:
                        datum_szoveg = data[1].strip()
                        if datum_szoveg:
                            try:
                                elem.entry_szul_datum.variable.set(datum_szoveg)  # A variable értékét állítjuk be
                            except Exception:
                                pass  # Ha érvénytelen a formátum, meghagyja az alapértelmezett mai dátumot
                        
                        elem.dropdown_bejaras.set(data[2])
                        elem.var_nagycsalados.set(data[3] == "True")
                        elem.var_sni.set(data[4] == "True")
                        elem.var_btm.set(data[5] == "True")
                        
                        elem.grid(row=len(self.elemek_listaja), column=0, padx=5, pady=6, sticky="ew")
                        self.elemek_listaja.append(elem)
            print(f"Adatok sikeresen betöltve a '{fajlnev}' fájlból.")
        except FileNotFoundError:
            print(f"A '{fajlnev}' fájl nem található.")
        except Exception as e:
            print(f"Hiba történt a fájl betöltése közben: {e}")
    
    def fajlba_mentes(self, fajlnev):
        popup = AlertPopup(
            master=self, 
            message="Biztosan menteni szeretnéd az összes gyerek adatlapját a fájlba?", 
            szelesseg=520, 
            magassag=220
        )
        self.wait_window(popup)
        if popup.eredmeny:
            try:                
                with open(fajlnev, "w", encoding="utf-8") as file:
                    for elem in self.elemek_listaja:  
                        if  elem.datum_ellenorzes():
                            raise ValueError(f"Hibás dátum formátum a gyerek adatlapján: {elem.entry_szul_datum.get()}")
                        data = elem.adat_lekeres()
                        line = f"{data['gyerek_neve']},{data['szuletesi_datum']},{data['bejaras']},{data['nagycsalados']},{data['sni']},{data['btm']}\n"
                        file.write(line)
                print(f"Adatok sikeresen mentve a '{fajlnev}' fájlba.")
            except ValueError as ve:
                print(f"Hiba: {ve}")
            except Exception as e:
                print(f"Hiba történt a fájl mentése közben: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()