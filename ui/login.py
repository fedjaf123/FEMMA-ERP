import tkinter as tk
from tkinter import messagebox
from core.security import verify_password
from models.users import get_user_by_username
from logic.audit_log import log_event


class LoginFrame(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success

        tk.Label(self, text='Korisničko ime').grid(row=0, column=0, padx=6, pady=6, sticky='e')
        tk.Label(self, text='Lozinka').grid(row=1, column=0, padx=6, pady=6, sticky='e')

        self.ent_user = tk.Entry(self)
        self.ent_pass = tk.Entry(self, show='*')

        self.ent_user.grid(row=0, column=1, padx=6, pady=6)
        self.ent_pass.grid(row=1, column=1, padx=6, pady=6)

        tk.Button(self, text='Prijava', command=self._login).grid(row=2, column=0, columnspan=2, pady=8)

        self.ent_user.focus_set()

    def _login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()

        rec = get_user_by_username(u)
        if not rec:
            messagebox.showerror('Greška', 'Nepostojeći korisnik')
            return

        user_id, username, pwd_hash, full_name, role, active = rec

        if not active:
            messagebox.showerror('Greška', 'Korisnik je deaktiviran')
            return

        if verify_password(p, pwd_hash):
            log_event(user_id, 'LOGIN', f'User {username} prijavljen')
            self.on_success(user_id, username)
        else:
            log_event(None, 'LOGIN_FAIL', f'Pogrešna lozinka za {u}')
            messagebox.showerror('Greška', 'Pogrešna lozinka')
