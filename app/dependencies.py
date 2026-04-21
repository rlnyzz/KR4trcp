from threading import Lock
from itertools import count

# In-memory storage
db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)

def clear_db():
    """Для очистки БД между тестами"""
    global db, _id_seq
    db.clear()
    _id_seq = count(start=1)