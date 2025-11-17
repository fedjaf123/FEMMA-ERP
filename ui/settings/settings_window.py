import tkinter as tk
from ui.settings.company_info import CompanyInfoFrame
from ui.settings.pdv_settings import PdvSettingsFrame
from ui.settings.users_screen import UsersFrame
from ui.settings.audit_log_screen import AuditLogFrame
from ui.settings.backup_restore_screen import BackupRestoreFrame


class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Postavke")
        self.geometry("800x500")

        self._build_ui()

    def _build_ui(self):
        # Glavni kontejner
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Sidebar lijevo
        self.sidebar = tk.Frame(container, width=200, bg="#f0f0f0")
        self.sidebar.pack(side="left", fill="y")

        # Content panel desno
        self.content = tk.Frame(container, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar dugmad (čisto, bez duplikata)
        tk.Button(
            self.sidebar,
            text="Podaci o firmi",
            anchor="w",
            command=lambda: self._open_screen("company"),
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.sidebar,
            text="PDV Postavke",
            anchor="w",
            command=lambda: self._open_screen("pdv"),
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.sidebar,
            text="Korisnici",
            anchor="w",
            command=lambda: self._open_screen("users"),
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.sidebar,
            text="Backup / Restore",
            anchor="w",
            command=lambda: self._open_screen("backup"),
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.sidebar,
            text="Audit Log",
            anchor="w",
            command=lambda: self._open_screen("audit"),
        ).pack(fill="x", padx=10, pady=5)

        # Default ekran
        self._open_screen("company")

    def _open_screen(self, screen: str):
        # Očistimo content panel
        for widget in self.content.winfo_children():
            widget.destroy()

        if screen == "company":
            frame = CompanyInfoFrame(self.content)
            frame.pack(fill="both", expand=True)

        elif screen == "pdv":
            frame = PdvSettingsFrame(self.content)
            frame.pack(fill="both", expand=True)

        elif screen == "users":
            frame = UsersFrame(self.content)
            frame.pack(fill="both", expand=True)

        elif screen == "backup":
            frame = BackupRestoreFrame(self.content)
            frame.pack(fill="both", expand=True)

        elif screen == "audit":
            frame = AuditLogFrame(self.content)
            frame.pack(fill="both", expand=True)

        # Placeholder
        else:
            tk.Label(
                self.content,
                text=f"[Ekran '{screen}' još nije implementiran]",
                font=("Arial", 14),
            ).pack(pady=40)
