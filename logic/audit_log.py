from datetime import datetime
from core.db import get_conn


def log_event(user_id: int | None, action: str, details: str = ''):
    ts = datetime.now().isoformat(timespec='seconds')
    with get_conn() as conn:
        conn.execute(
            'INSERT INTO audit_log(ts, user_id, action, details) VALUES (?, ?, ?, ?)',
            (ts, user_id, action, details)
        )
        conn.commit()
