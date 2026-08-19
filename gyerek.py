from typing import TYPE_CHECKING, cast
import customtkinter as ctk
from alert import AlertPopup
from ctkdateentry import CTkDateEntry
import datetime as dt

if TYPE_CHECKING:
    from main import App


class GyerekAdatlap(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=0)
        self.grid_columnconfigure(7, weight=0)

        FONT_ENTRY = ("Arial", 15, "bold")
        FONT_CHECK = ("Arial", 14, "bold")

    # --- 1. Gyerek neve ---
        self.entry_nev = ctk.CTkEntry(
            self, 
            placeholder_text="Gyerek neve...", 
            width=380, 
            height=42, 
            font=FONT_ENTRY
        )
        self.entry_nev.grid(row=0, column=1, padx=8, pady=12, sticky="ew")

    # --- 2. Születési dátum ---
        self.entry_szul_datum = CTkDateEntry(
            self,
            width=150,
            height=42,
            font=FONT_ENTRY
        )
        self.entry_szul_datum.grid(row=0, column=2, padx=8, pady=12)

    # --- 3. Bejárás ---
        bejaras_opciok = [
            "Velence", "Kápolnásnyék", "Gárdony", 
            "Agárd", "Sukoró", "Pázmánd", "Pákozd", "Bejárós (egyéb)"
        ]
        self.dropdown_bejaras = ctk.CTkOptionMenu(
            self, 
            values=bejaras_opciok, 
            width=160, 
            height=42, 
            font=FONT_ENTRY,
            dropdown_font=FONT_ENTRY
        )
        self.dropdown_bejaras.grid(row=0, column=3, padx=8, pady=12)

    # --- 4. Jelölőnégyzetek ---
        self.var_nagycsalados = ctk.BooleanVar(value=False)
        self.chk_nagycsalados = ctk.CTkCheckBox(
            self, 
            text="Nagycsaládos", 
            variable=self.var_nagycsalados, 
            checkbox_width=28, 
            checkbox_height=28, 
            font=FONT_CHECK
        )
        self.chk_nagycsalados.grid(row=0, column=4, padx=12, pady=12)

        self.var_sni = ctk.BooleanVar(value=False)
        self.chk_sni = ctk.CTkCheckBox(
            self, 
            text="SNI", 
            variable=self.var_sni, 
            checkbox_width=28, 
            checkbox_height=28, 
            font=FONT_CHECK
        )
        self.chk_sni.grid(row=0, column=5, padx=12, pady=12)

        self.var_btm = ctk.BooleanVar(value=False)
        self.chk_btm = ctk.CTkCheckBox(
            self, 
            text="BTM", 
            variable=self.var_btm, 
            checkbox_width=28, 
            checkbox_height=28, 
            font=FONT_CHECK
        )
        self.chk_btm.grid(row=0, column=6, padx=(12, 16), pady=12)

        # --- 5. Törlés Gomb ---
        self.btn_torles = ctk.CTkButton(
            self, 
            text="Törlés", 
            fg_color="#D32F2F", 
            hover_color="#9A0007", 
            height=42, 
            width=110, 
            font=FONT_ENTRY, 
            command=self.torles
        )
        self.btn_torles.grid(row=0, column=7, padx=8, pady=12, sticky="e")

    def adat_lekeres(self):
        return {
            "gyerek_neve": self.entry_nev.get(),
            "szuletesi_datum": self.entry_szul_datum.variable.get(),  # A variable-t olvassuk ki
            "bejaras": self.dropdown_bejaras.get(),
            "nagycsalados": self.var_nagycsalados.get(),
            "sni": self.var_sni.get(),
            "btm": self.var_btm.get()
        }

    
    def datum_ellenorzes(self):
        datum = self.entry_szul_datum.variable.get()  # A variable-t olvassuk ki
        return len(datum) > 0
    
    def torles(self):
        popup = AlertPopup(
            master=self.winfo_toplevel(), 
            message="Biztosan törölni szeretnéd ezt a gyerek adatlapját?", 
            szelesseg=520, 
            magassag=220
        )
        self.wait_window(popup)
        if popup.eredmeny:
            # Type casting használata a Pylance hibák elkerülésére
            app = cast("App", self.winfo_toplevel())
            if hasattr(app, "elemek_listaja") and self in app.elemek_listaja:
                app.elemek_listaja.remove(self)
                self.destroy()
                app.lista_frissitese()
            else:
                self.destroy()