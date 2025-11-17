from typing import Dict
from core.db import get_conn


def get_permissions(user_id: int) -> Dict[str, int]:
with get_conn() as conn:
cur = conn.execute('SELECT * FROM user_permissions WHERE user_id=?', (user_id,))
row = cur.fetchone()
if not row:
return {}
cols = [c[0] for c in cur.description]
return dict(zip(cols, row))


def set_permission(user_id: int, field: str, value: int):
with get_conn() as conn:
conn.execute(f'UPDATE user_permissions SET {field}=? WHERE user_id=?', (value, user_id))
conn.commit()