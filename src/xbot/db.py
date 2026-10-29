import sqlite3
from datetime import datetime, timezone

VALID = {"drafted", "approved", "posted", "skipped"}


def init_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, text TEXT NOT NULL, "
        "pillar TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)"
    )
    conn.commit()
    return conn


def _check(status):
    if status not in VALID:
        raise ValueError(f"invalid status: {status}")


def add_post(conn, text, pillar, status="drafted"):
    _check(status)
    cur = conn.execute(
        "INSERT INTO posts (text, pillar, status, created_at) VALUES (?, ?, ?, ?)",
        (text, pillar, status, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    return cur.lastrowid


def set_status(conn, post_id, status):
    _check(status)
    cur = conn.execute("UPDATE posts SET status = ? WHERE id = ?", (status, post_id))
    if cur.rowcount == 0:
        raise KeyError(post_id)
    conn.commit()


def get_post(conn, post_id):
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        raise KeyError(post_id)
    return dict(row)


def next_day_number(conn):
    n = conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'posted'").fetchone()[0]
    return n + 1


def past_texts(conn):
    rows = conn.execute("SELECT text FROM posts WHERE status = 'posted' ORDER BY id").fetchall()
    return [r[0] for r in rows]
