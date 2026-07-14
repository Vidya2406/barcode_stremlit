import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "scanvibe.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                type TEXT NOT NULL,
                format TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )


def add_scan(content: str, scan_type: str, scan_format: str = ""):
    """scan_type should be 'QR Code' or 'Barcode'. scan_format is the raw
    symbology, e.g. QRCODE, EAN13, CODE128."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scans (content, type, format, timestamp) VALUES (?, ?, ?, ?)",
            (content, scan_type, scan_format, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def get_history():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM scans ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]


def delete_scan(scan_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM scans WHERE id = ?", (scan_id,))


def clear_history():
    with get_connection() as conn:
        conn.execute("DELETE FROM scans")


def search_history(query: str):
    with get_connection() as conn:
        like = f"%{query}%"
        rows = conn.execute(
            "SELECT * FROM scans WHERE content LIKE ? OR type LIKE ? OR format LIKE ? ORDER BY id DESC",
            (like, like, like),
        ).fetchall()
        return [dict(r) for r in rows]


def statistics():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) as c FROM scans").fetchone()["c"]
        qr = conn.execute("SELECT COUNT(*) as c FROM scans WHERE type = 'QR Code'").fetchone()["c"]
        barcode = conn.execute("SELECT COUNT(*) as c FROM scans WHERE type = 'Barcode'").fetchone()["c"]
        return total, qr, barcode


init_db()
