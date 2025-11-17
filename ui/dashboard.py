import tkinter as tk
from ui.settings.settings_window import SettingsWindow


class Dashboard(tk.Frame):
    def __init__(self, master, current_user: dict):
        super().__init__(master)
        self.current_user = current_user
        self._build()

    def _build(self):
        # Dugme za otvaranje Settings prozora
        btn_settings = tk.Button(self, text="⚙ Postavke", command=self._open_settings)
        btn_settings.pack(anchor='ne', padx=12, pady=12)

        # Gornji red – dugmad za glavne module
        row = tk.Frame(self)
        row.pack(padx=12, pady=12, fill='x')

        for label in ('POS', 'NARUDŽBE', 'SKLADIŠTE', 'FINANSIJE'):
            b = tk.Button(row, text=label, width=16)
            b.pack(side='left', padx=6)

        # Placeholder za grafikon (biće graf kasnije)
        graph_holder = tk.Label(
            self,
            text='[Graf: Promet / Troškovi / Profit — placeholder]',
            font=('Arial', 12)
        )
        graph_holder.pack(padx=12, pady=24, fill='x')

    # Metoda koja otvara Settings prozor
    def _open_settings(self):
        SettingsWindow(self)
