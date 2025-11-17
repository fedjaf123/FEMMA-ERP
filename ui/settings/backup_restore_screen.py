import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

from core.db import DB_PATH


BACKUP_DIR = "backups"


class BackupRestoreFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        tk.Label(self, text="Backup i Restore baze", font=("Arial", 14, "bold")).pack(
            pady=20
        )

        tk.Button(
            self,
            text="📦 Napravi backup baze",
            font=("Arial", 12),
            width=30,
            command=self._make_backup,
        ).pack(pady=15)

        tk.Button(
            self,
            text="♻ Vrati backup baze",
            font=("Arial", 12),
            width=30,
            command=self._restore_backup,
        ).pack(pady=15)

    def _make_backup(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        backup_name = f"femma_backup_{timestamp}.zip"
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        try:
            shutil.make_archive(
                base_name=backup_path.replace(".zip", ""),
                format="zip",
                root_dir=os.path.dirname(DB_PATH),
                base_dir=os.path.basename(DB_PATH),
            )
            messagebox.showinfo("Backup", f"Backup uspješno kreiran:\n{backup_path}")

        except Exception as e:
            messagebox.showerror("Greška", f"Backup nije uspio:\n{e}")

    def _restore_backup(self):
        file_path = filedialog.askopenfilename(
            title="Odaberite backup ZIP datoteku",
            filetypes=[("ZIP fajlovi", "*.zip")],
        )

        if not file_path:
            return

        if not messagebox.askyesno(
            "Potvrda",
            "Da li ste sigurni da želite vratiti ovaj backup?\nOvo će zamijeniti trenutnu bazu!",
        ):
            return

        try:
            shutil.unpack_archive(file_path, extract_dir=os.path.dirname(DB_PATH))

            messagebox.showinfo(
                "Restore", "Backup uspješno vraćen.\nRestartujte aplikaciju."
            )
        except Exception as e:
            messagebox.showerror("Greška", f"Restore nije uspio:\n{e}")
