import customtkinter as ctk
from gyerek import GyerekAdatlap
from alert import AlertPopup

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gyerek Nyilvántartó")
        self.after(10, lambda: self.state("zoomed"))
        
        self.elemek_listaja = []

    # Főablak elrendezés
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # --- 1. Gördíthető Lista Terület (FELÜL) ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    # --- A Hozzáadás gomb a Gördíthető kereten BELÜL ---
        self.btn_hozzaadas_inline = ctk.CTkButton(
        self.scrollable_frame,           
            text="+ Új gyerek hozzáadása",
            fg_color="green",
            hover_color="darkgreen",
            height=40,
            width=250,
            anchor="center",
            font=("Arial", 14, "bold"),
            command=self.gyerek_hozzaadasa
        )

    # --- 2. Alsó Gombok (ALUL) ---
        self.bottom_button_frame = ctk.CTkFrame(self, corner_radius=5)
        self.bottom_button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 20))

    # --- Adatok Kiírása ---
        self.btn_kiiras = ctk.CTkButton(
            self.bottom_button_frame, text="Adatok Nyomtatása (Console)", fg_color="grey", command=self.adatok_kiirasa
        )
        self.btn_kiiras.pack(side="left", padx=5, pady=8)
        
    
        
    # --- Mentés Fájlba ---
        self.btn_mentes = ctk.CTkButton(
            self.bottom_button_frame, text="Mentés Fájlba", fg_color="blue", command=lambda: self.fajlba_mentes("gyerek_adatok.csv")
        )
        self.btn_mentes.pack(side="right", padx=5, pady=8)

    # --- Összes Törlése ---
        self.btn_torles = ctk.CTkButton(
            self.bottom_button_frame, text="Összes Törlése", fg_color="red", command=self.osszes_torlese
        )
        self.btn_torles.pack(side="right", padx=5, pady=8)
        
    # Fájl betöltése
        self.fajlbol_betoltes("gyerek_adatok.csv")

    # Ha nincs elem a fájlban, hozzáadunk egy üres sort
        if not self.elemek_listaja:
            self.gyerek_hozzaadasa()
        else:
            self.gomb_pozicionalasa()

    def gomb_pozicionalasa(self):
        """A hozzáadás gombot mindig a legutolsó gyerek sora alá helyezi."""
        self.btn_hozzaadas_inline.grid(
            row=len(self.elemek_listaja),
            column=0,
            padx=10,
            pady=15,
            sticky="n"
        )


    def gyerek_hozzaadasa(self):
        """Új gyerek adatlap hozzáadása és a gomb lejjebb tolása."""
        elem = GyerekAdatlap(master=self.scrollable_frame)
        elem.grid(row=len(self.elemek_listaja), column=0, padx=5, pady=3, sticky="ew")
        self.elemek_listaja.append(elem)

        # Gomb áthelyezése a lista aljára
        self.gomb_pozicionalasa()


    def lista_frissitese(self):
        """Újra rendezi a sorokat törlés után, hogy ne maradjanak lyukak."""
        for i, elem in enumerate(self.elemek_listaja):
            elem.grid(row=i, column=0, padx=5, pady=3, sticky="ew")
        self.gomb_pozicionalasa()


    def adatok_kiirasa(self):
        print("\n================ RENDSZERBEN LÉVŐ ADATOK ================")
        for elem in self.elemek_listaja:
            if elem.winfo_exists():
                print(elem.adat_lekeres())


    def osszes_torlese(self):
        popup = AlertPopup(master=self, message="Biztosan törölni szeretnéd az összes gyerek adatlapját?", szelesseg=450, magassag=150)
        self.wait_window(popup)
        if popup.eredmeny:  # Ha az OK gombot nyomták meg
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
                        elem.entry_szul_datum.insert(0, data[1])
                        elem.dropdown_bejaras.set(data[2])
                        elem.var_nagycsalados.set(data[3] == "True")
                        elem.var_sni.set(data[4] == "True")
                        elem.var_btm.set(data[5] == "True")
                        elem.grid(row=len(self.elemek_listaja), column=0, padx=5, pady=3, sticky="ew")
                        self.elemek_listaja.append(elem)
            print(f"Adatok sikeresen betöltve a '{fajlnev}' fájlból.")
        except FileNotFoundError:
            print(f"A '{fajlnev}' fájl nem található.")
        except Exception as e:
            print(f"Hiba történt a fájl betöltése közben: {e}")
    
    
    def fajlba_mentes(self, fajlnev):
        popup = AlertPopup(master=self, message="Biztosan menteni szeretnéd az összes gyerek adatlapját a fájlba?", szelesseg=450, magassag=150)
        self.wait_window(popup)
        if popup.eredmeny:  # Ha az OK gombot nyomták meg
            try:
                with open(fajlnev, "w", encoding="utf-8") as file:
                    for elem in self.elemek_listaja:
                        data = elem.adat_lekeres()
                        line = f"{data['gyerek_neve']},{data['szuletesi_datum']},{data['bejaras']},{data['nagycsalados']},{data['sni']},{data['btm']}\n"
                        file.write(line)
                print(f"Adatok sikeresen mentve a '{fajlnev}' fájlba.")
            except Exception as e:
                print(f"Hiba történt a fájl mentése közben: {e}")

    

if __name__ == "__main__":
    app = App()
    app.mainloop()