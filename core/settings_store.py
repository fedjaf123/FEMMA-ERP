from typing import Optional
from .db import get_conn

DEFAULTS = {
    'company_name': '',
    'company_jib': '',
    'company_pdv': '',
    'company_address': '',
    'company_trr': '',
    'company_email': '',   # ⬅️ NOVO POLJE
    'pdv_enabled': '1',    # 1 = firma u PDV sistemu, 0 = nije
    'pdv_rate': '17',
}


def get_setting(key: str) -> Optional[str]:
    with get_conn() as conn:
        cur = conn.execute('SELECT value FROM settings WHERE key=?', (key,))
        row = cur.fetchone()
        if row is None:
            return DEFAULTS.get(key)
        return row[0]


def set_setting(key: str, value: str) -> None:
    with get_conn() as conn:
        conn.execute(
            'INSERT INTO settings (key, value) VALUES (?, ?) '
            'ON CONFLICT(key) DO UPDATE SET value=excluded.value',
            (key, value)
        )
        conn.commit()


def ensure_defaults():
    for k, v in DEFAULTS.items():
        if get_setting(k) is None:
            set_setting(k, v)
