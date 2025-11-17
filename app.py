import tkinter as tk
from core.db import init_db
from core.settings_store import ensure_defaults
from models.users import bootstrap_admin
from ui.login import LoginFrame
from ui.dashboard import Dashboard


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FEMMA-ERP")
        self.geometry("900x600")
        self._current_user = None

        self._init_system()
        self._show_login()

    def _init_system(self):
        init_db()
        ensure_defaults()
        bootstrap_admin()

    def _show_login(self):
        self._clear()
        login_view = LoginFrame(self, on_success=self._on_login)
        login_view.pack(expand=True)

    def _on_login(self, user_id: int, username: str):
        self._current_user = {"id": user_id, "username": username}
        self._show_dashboard()

    def _show_dashboard(self):
        self._clear()
        dash = Dashboard(self, current_user=self._current_user)
        dash.pack(expand=True, fill="both")

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
