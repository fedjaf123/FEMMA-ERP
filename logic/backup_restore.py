from pathlib import Path
from shutil import copy2
from datetime import datetime
from core.db import DB_PATH, get_conn


BACKUP_DIR = DB_PATH.parent / 'backups'


def backup_db(user_id: int | None) -> Path:
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
target = BACKUP_DIR / f'femma_backup_{ts}.db'
copy2(DB_PATH, target)
with get_conn() as conn:
conn.execute('INSERT INTO backup_history(ts, action, file_path, user_id) VALUES(datetime("now"), ?, ?, ?)',
('BACKUP', str(target), user_id))
conn.commit()
return target


def restore_db(backup_file: Path, user_id: int | None):
copy2(backup_file, DB_PATH)
with get_conn() as conn:
conn.execute('INSERT INTO backup_history(ts, action, file_path, user_id) VALUES(datetime("now"), ?, ?, ?)',
('RESTORE', str(backup_file), user_id))
conn.commit()