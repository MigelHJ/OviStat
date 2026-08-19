import customtkinter as ctk

class AlertPopup(ctk.CTkToplevel):
    def __init__(self, master, message, szelesseg=520, magassag=220, **kwargs):
        super().__init__(master, **kwargs)

        self.eredmeny = False
        self.title("Megerősítés")
        self.resizable(False, False)

    # Üzenet (Nagyobb, szembetűnő betűtípus)
        label = ctk.CTkLabel(
            self, 
            text=message, 
            font=("Arial", 16, "bold"),
            wraplength=szelesseg - 40
        )
        label.pack(padx=20, pady=(25, 15))

    # Gombok kerete
        gomb_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=0)
        gomb_frame.pack(pady=15)

    # OK és Mégse gombok (Magasabb gombok, nagyobb szöveggel)
        btn_ok = ctk.CTkButton(
            gomb_frame, 
            text="OK", 
            fg_color="green", 
            hover_color="darkgreen",
            font=("Arial", 16, "bold"),
            width=130,
            height=45,
            command=self.Ok_gomb_nyomaskor
        )
        btn_ok.pack(side="left", padx=15)

        btn_megse = ctk.CTkButton(
            gomb_frame, 
            text="Mégse", 
            fg_color="#D32F2F", 
            hover_color="#9A0007",
            font=("Arial", 16, "bold"),
            width=130,
            height=45,
            command=self.Megse_gomb_nyomaskor
        )
        btn_megse.pack(side="left", padx=15)

        self.szelesseg = szelesseg
        self.magassag = magassag
        self.after(10, self.kozepre)

    def kozepre(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.szelesseg // 2)
        y = (self.winfo_screenheight() // 2) - (self.magassag // 2)
        self.geometry(f"{self.szelesseg}x{self.magassag}+{x}+{y}")
        self.grab_set()

    def Ok_gomb_nyomaskor(self):
        self.eredmeny = True
        self.destroy()

    def Megse_gomb_nyomaskor(self):
        self.eredmeny = False
        self.destroy()