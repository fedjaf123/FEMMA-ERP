from typing import Optional
from core.db import get_conn
from core.security import hash_password

ADMIN_DEFAULTS = {
    'username': 'admin',
    'password': 'admin123',  # promijeniti nakon prvog logina
    'full_name': 'Administrator',
}


def get_user_by_username(username: str) -> Optional[tuple]:
    with get_conn() as conn:
        cur = conn.execute(
            'SELECT id, username, password_hash, full_name, role, active '
            'FROM users WHERE username=?',
            (username,)
        )
        return cur.fetchone()


def create_user(username: str, password: str, full_name: str = '',
                role: str = 'admin', active: int = 1) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            'INSERT INTO users(username, password_hash, full_name, role, active) '
            'VALUES (?, ?, ?, ?, ?)',
            (username, hash_password(password), full_name, role, active)
        )
        user_id = cur.lastrowid

        # Kreiramo default permissions entry
        conn.execute(
            'INSERT INTO user_permissions(user_id) VALUES (?)',
            (user_id,)
        )
        conn.commit()
        return user_id


def bootstrap_admin():
    # Ako admin ne postoji → kreiraj ga
    if get_user_by_username(ADMIN_DEFAULTS['username']) is None:
        create_user(
            ADMIN_DEFAULTS['username'],
            ADMIN_DEFAULTS['password'],
            ADMIN_DEFAULTS['full_name'],
            role='admin',
            active=1
        )
