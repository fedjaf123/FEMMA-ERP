import tkinter as tk
from tkinter import messagebox, ttk
from core.db import get_conn
from models.users import get_user_by_username, create_user
from ui.settings.permissions_screen import PermissionsEditor


class UsersFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self._load_users()

    def _build(self):
        # Gornji horizontalni panel (dio s dugmadima)
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", padx=10, pady=10)

        btn_add = tk.Button(
            top_bar, text="Dodaj korisnika", command=self._open_add_user
        )
        btn_add.pack(side="left", padx=5)

        btn_perm = tk.Button(
            top_bar, text="Uredi dozvole", command=self._open_permissions
        )
        btn_perm.pack(side="left", padx=5)

        # TABELA korisnika
        columns = ("id", "username", "full_name", "role", "active")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=15)

        self.table.heading("id", text="ID")
        self.table.heading("username", text="Korisničko ime")
        self.table.heading("full_name", text="Ime i prezime")
        self.table.heading("role", text="Uloga")
        self.table.heading("active", text="Aktivan")

        self.table.column("id", width=40)
        self.table.column("username", width=150)
        self.table.column("full_name", width=200)
        self.table.column("role", width=100)
        self.table.column("active", width=80)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def _load_users(self):
        for row in self.table.get_children():
            self.table.delete(row)

        with get_conn() as conn:
            cur = conn.execute(
                "SELECT id, username, full_name, role, active FROM users ORDER BY id"
            )
            for user in cur.fetchall():
                user_id, username, full_name, role, active = user
                status = "Da" if active == 1 else "Ne"
                self.table.insert(
                    "", "end", values=(user_id, username, full_name, role, status)
                )

    def _open_add_user(self):
        AddUserWindow(self, self._load_users)

    def _open_permissions(self):
        selected = self.table.focus()

        if not selected:
            messagebox.showerror("Greška", "Molimo odaberite korisnika!")
            return

        user = self.table.item(selected)["values"]
        user_id = user[0]

        PermissionsEditor(self, user_id)


class AddUserWindow(tk.Toplevel):
    def __init__(self, master, on_save_callback):
        super().__init__(master)
        self.on_save_callback = on_save_callback

        self.title("Novi korisnik")
        self.geometry("350x300")

        tk.Label(self, text="Korisničko ime:").pack(pady=5)
        self.ent_username = tk.Entry(self)
        self.ent_username.pack(pady=5)

        tk.Label(self, text="Lozinka:").pack(pady=5)
        self.ent_password = tk.Entry(self, show="*")
        self.ent_password.pack(pady=5)

        tk.Label(self, text="Ime i prezime:").pack(pady=5)
        self.ent_fullname = tk.Entry(self)
        self.ent_fullname.pack(pady=5)

        tk.Label(self, text="Uloga:").pack(pady=5)
        self.ent_role = tk.Entry(self)
        self.ent_role.insert(0, "user")  # default
        self.ent_role.pack(pady=5)

        tk.Button(self, text="Spasi", command=self._save).pack(pady=15)

    def _save(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        fullname = self.ent_fullname.get().strip()
        role = self.ent_role.get().strip()

        if not username or not password:
            messagebox.showerror("Greška", "Korisničko ime i lozinka su obavezni.")
            return

        if get_user_by_username(username):
            messagebox.showerror("Greška", "Korisničko ime već postoji!")
            return

        create_user(username, password, fullname, role, active=1)

        messagebox.showinfo("Spašeno", "Korisnik uspješno kreiran.")
        self.on_save_callback()
        self.destroy()
