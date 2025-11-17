from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / 'database'
DB_PATH = DB_DIR / 'femma.db'
SCHEMA_PATH = DB_DIR / 'schema.sql'


def get_conn():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        if SCHEMA_PATH.exists():
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        conn.commit()
