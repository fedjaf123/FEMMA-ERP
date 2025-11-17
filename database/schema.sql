PRAGMA foreign_keys = ON;


-- Korisnici
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
full_name TEXT,
role TEXT DEFAULT 'admin',
active INTEGER DEFAULT 1
);


-- Granularna prava po korisniku
CREATE TABLE IF NOT EXISTS user_permissions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
can_open_pos INTEGER DEFAULT 1,
can_view_finance INTEGER DEFAULT 1,
can_edit_prices INTEGER DEFAULT 0,
can_change_stock INTEGER DEFAULT 1,
can_view_finance_graph INTEGER DEFAULT 1,
can_manage_users INTEGER DEFAULT 1,
can_backup_restore INTEGER DEFAULT 1,
FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- Key/Value postavke (Company, PDV, POS…)
CREATE TABLE IF NOT EXISTS settings (
key TEXT PRIMARY KEY,
value TEXT
);


-- Globalni audit log
CREATE TABLE IF NOT EXISTS audit_log (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ts TEXT NOT NULL,
user_id INTEGER,
action TEXT NOT NULL,
details TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);


-- Evidencija backup/restore
CREATE TABLE IF NOT EXISTS backup_history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ts TEXT NOT NULL,
action TEXT NOT NULL, -- BACKUP ili RESTORE
file_path TEXT NOT NULL,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id)
);