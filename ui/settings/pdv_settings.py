import tkinter as tk
from tkinter import messagebox
from core.settings_store import get_setting, set_setting


class PdvSettingsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        # Checkbox: firma u PDV-u
        self.var_enabled = tk.IntVar(value=int(get_setting('pdv_enabled') or 1))
        chk = tk.Checkbutton(self, text="Firma je u PDV sistemu", variable=self.var_enabled)
        chk.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        # Stopa PDV-a
        tk.Label(self, text="Stopa PDV-a (%):").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.ent_rate = tk.Entry(self, width=10)
        self.ent_rate.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        self.ent_rate.insert(0, get_setting('pdv_rate') or "17")

        # Dugme SPASI
        tk.Button(self, text="Spasi", command=self._save).grid(
            row=2, column=0, columnspan=2, pady=20
        )

    def _save(self):
        # Spremanje vrijednosti
        set_setting('pdv_enabled', str(self.var_enabled.get()))
        set_setting('pdv_rate', self.ent_rate.get().strip())

        messagebox.showinfo("Spašeno", "PDV postavke su uspješno spašene.")
