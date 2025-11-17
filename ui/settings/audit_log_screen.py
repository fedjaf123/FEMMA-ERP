import tkinter as tk
from tkinter import ttk
from core.db import get_conn


class AuditLogFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self._load_logs()

    def _build(self):
        tk.Label(
            self, text="Audit log – pregled aktivnosti", font=("Arial", 14, "bold")
        ).pack(pady=10)

        # SEARCH BAR
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10)

        tk.Label(search_frame, text="Pretraga:", font=("Arial", 11)).pack(
            side="left", padx=5
        )
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(search_frame, text="Filtriraj", command=self._filter_logs).pack(
            side="left", padx=5
        )
        tk.Button(search_frame, text="Osvježi", command=self._load_logs).pack(
            side="left", padx=5
        )

        # TABLE
        columns = ("ts", "user_id", "action", "details")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=18)

        self.table.heading("ts", text="Vrijeme")
        self.table.heading("user_id", text="User ID")
        self.table.heading("action", text="Akcija")
        self.table.heading("details", text="Detalji")

        self.table.column("ts", width=180)
        self.table.column("user_id", width=80)
        self.table.column("action", width=150)
        self.table.column("details", width=500)

        # SCROLLBAR
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="left", fill="y", pady=10)

    def _load_logs(self):
        # Clear old rows
        for row in self.table.get_children():
            self.table.delete(row)

        with get_conn() as conn:
            cur = conn.execute(
                """
                SELECT ts, user_id, action, details
                FROM audit_log
                ORDER BY ts DESC
                """
            )
            for log in cur.fetchall():
                self.table.insert("", "end", values=log)

    def _filter_logs(self):
        text = self.search_entry.get().strip().lower()

        # Clear table
        for row in self.table.get_children():
            self.table.delete(row)

        with get_conn() as conn:
            cur = conn.execute(
                """
                SELECT ts, user_id, action, details
                FROM audit_log
                WHERE LOWER(action) LIKE ? OR LOWER(details) LIKE ?
                ORDER BY ts DESC
                """,
                (f"%{text}%", f"%{text}%"),
            )
            for log in cur.fetchall():
                self.table.insert("", "end", values=log)
