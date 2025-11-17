import tkinter as tk
from tkinter import messagebox
from core.settings_store import get_setting, set_setting


class CompanyInfoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        tk.Label(self, text='Naziv firme:').grid(row=0, column=0, sticky='e', padx=8, pady=6)
        tk.Label(self, text='JIB:').grid(row=1, column=0, sticky='e', padx=8, pady=6)
        tk.Label(self, text='PDV broj:').grid(row=2, column=0, sticky='e', padx=8, pady=6)
        tk.Label(self, text='Adresa:').grid(row=3, column=0, sticky='e', padx=8, pady=6)
        tk.Label(self, text='Broj TRR:').grid(row=4, column=0, sticky='e', padx=8, pady=6)
        tk.Label(self, text='Email adresa:').grid(row=5, column=0, sticky='e', padx=8, pady=6)

        self.ent_name = tk.Entry(self, width=40)
        self.ent_jib = tk.Entry(self, width=40)
        self.ent_pdv = tk.Entry(self, width=40)
        self.ent_address = tk.Entry(self, width=40)
        self.ent_trr = tk.Entry(self, width=40)
        self.ent_email = tk.Entry(self, width=40)

        self.ent_name.grid(row=0, column=1, padx=8, pady=6)
        self.ent_jib.grid(row=1, column=1, padx=8, pady=6)
        self.ent_pdv.grid(row=2, column=1, padx=8, pady=6)
        self.ent_address.grid(row=3, column=1, padx=8, pady=6)
        self.ent_trr.grid(row=4, column=1, padx=8, pady=6)
        self.ent_email.grid(row=5, column=1, padx=8, pady=6)

        # Dugme SPASI
        tk.Button(self, text='Spasi', command=self._save).grid(
            row=6, column=0, columnspan=2, pady=20
        )

        self._load()

    def _load(self):
        # Učitavamo sva polja iz baze
        self.ent_name.insert(0, get_setting('company_name') or '')
        self.ent_jib.insert(0, get_setting('company_jib') or '')
        self.ent_pdv.insert(0, get_setting('company_pdv') or '')
        self.ent_address.insert(0, get_setting('company_address') or '')
        self.ent_trr.insert(0, get_setting('company_trr') or '')
        self.ent_email.insert(0, get_setting('company_email') or '')

    def _save(self):
        set_setting('company_name', self.ent_name.get().strip())
        set_setting('company_jib', self.ent_jib.get().strip())
        set_setting('company_pdv', self.ent_pdv.get().strip())
        set_setting('company_address', self.ent_address.get().strip())
        set_setting('company_trr', self.ent_trr.get().strip())
        set_setting('company_email', self.ent_email.get().strip())

        messagebox.showinfo('Spaseno', 'Podaci o firmi su uspješno spašeni.')
