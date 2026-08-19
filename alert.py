import customtkinter as ctk

class AlertPopup(ctk.CTkToplevel):
    def __init__(self, master, message, szelesseg=400, magassag=180, **kwargs):
        super().__init__(master, **kwargs)

        # Alapértelmezetten False (pl. ha az X-re kattintva zárja be)
        self.eredmeny = False

        self.title("Megerősítés")
        self.resizable(False, False)

        # Üzenet
        label = ctk.CTkLabel(self, text=message, font=("Arial", 12))
        label.pack(padx=20, pady=20)

        # Gombok kerete
        gomb_frame = ctk.CTkFrame(self, fg_color="transparent")
        gomb_frame.pack(pady=10)

        # OK és Mégse gombok
        btn_ok = ctk.CTkButton(gomb_frame, text="OK", fg_color="green", command=self.Ok_gomb_nyomaskor)
        btn_ok.pack(side="left", padx=10)

        btn_megse = ctk.CTkButton(gomb_frame, text="Mégse", fg_color="red", command=self.Megse_gomb_nyomaskor)
        btn_megse.pack(side="left", padx=10)

        # Ablak középre helyezése
        self.after(10, self.kozepre)

    def kozepre(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        self.geometry(f"300x150+{x}+{y}")
        self.grab_set()

    def Ok_gomb_nyomaskor(self):
        self.eredmeny = True   # Elmentjük az értéket
        self.destroy()          # Bezárjuk az ablakot

    def Megse_gomb_nyomaskor(self):
        self.eredmeny = False  # Elmentjük az értéket
        self.destroy()          # Bezárjuk az ablakot