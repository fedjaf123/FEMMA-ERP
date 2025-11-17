import tkinter as tk
from tkinter import ttk, messagebox
from core.db import get_conn


PERMISSIONS = {
    "can_open_pos": "Dozvola pristupa POS modulu",
    "can_view_finance": "Dozvola pregleda finansija",
    "can_edit_prices": "Dozvola izmjene prodajnih cijena",
    "can_change_stock": "Dozvola izmjene skladišnog stanja",
    "can_view_finance_graph": "Dozvola pregleda finansijskih prikaza",
    "can_manage_users": "Dozvola upravljanja korisnicima",
    "can_backup_restore": "Dozvola kreiranja i vraćanja backup-a",
}


class PermissionsEditor(tk.Toplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id

        self.title("Uredi dozvole")
        self.geometry("420x460")

        # --- UČITAJ TRENUTNE DOZVOLE ---
        with get_conn() as conn:
            cur = conn.execute(
                "SELECT * FROM user_permissions WHERE user_id = ?", (user_id,)
            )
            row = cur.fetchone()

            if row is None:
                # Ako user nema entry u tabeli user_permissions → kreiraj ga
                conn.execute(
                    """
                    INSERT INTO user_permissions (user_id, can_open_pos, can_view_finance,
                        can_edit_prices, can_change_stock, can_view_finance_graph,
                        can_manage_users, can_backup_restore)
                    VALUES (?,0,0,0,0,0,0,0)
                    """,
                    (user_id,),
                )
                conn.commit()

                # ponovo učitaj
                cur = conn.execute(
                    "SELECT * FROM user_permissions WHERE user_id = ?", (user_id,)
                )
                row = cur.fetchone()

            # tuple → dict konverzija
            columns = [desc[0] for desc in cur.description]
            row = dict(zip(columns, row))

        # --- PRIKAZ CHECKBOXA ---
        self.vars = {}
        y = 20

        for key, label in PERMISSIONS.items():
            starting_value = row.get(key, 0)
            self.vars[key] = tk.IntVar(value=starting_value)

            chk = tk.Checkbutton(
                self, text=label, variable=self.vars[key], anchor="w", padx=10
            )
            chk.place(x=10, y=y)

            y += 35

        tk.Button(self, text="Spasi", command=self._save).place(x=170, y=y + 10)

    def _save(self):
        # spremi sve dozvole u bazu
        with get_conn() as conn:
            fields = ", ".join([f"{k}=?" for k in self.vars])
            values = [self.vars[k].get() for k in self.vars]
            values.append(self.user_id)

            conn.execute(
                f"UPDATE user_permissions SET {fields} WHERE user_id = ?", values
            )
            conn.commit()

        messagebox.showinfo("Spašeno", "Dozvole su uspješno spremljene.")
        self.destroy()
