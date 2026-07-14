import sqlite3
import pandas as pd
from datetime import datetime

DATABASE = "database.db"


def get_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode_type TEXT,
        barcode_value TEXT,
        scan_date TEXT,
        scan_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_scan(barcode_type, barcode_value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM scan_history WHERE barcode_value=?",
        (barcode_value,)
    )

    if cursor.fetchone() is None:

        now = datetime.now()

        cursor.execute("""
        INSERT INTO scan_history(
            barcode_type,
            barcode_value,
            scan_date,
            scan_time
        )
        VALUES(?,?,?,?)
        """, (
            barcode_type,
            barcode_value,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ))

        conn.commit()

    conn.close()


def get_history():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM scan_history ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def delete_scan(scan_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM scan_history WHERE id=?",
        (scan_id,)
    )

    conn.commit()

    conn.close()


def clear_history():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM scan_history")

    conn.commit()

    conn.close()


def search_history(keyword):

    conn = get_connection()

    query = """
    SELECT *
    FROM scan_history
    WHERE barcode_value LIKE ?
       OR barcode_type LIKE ?
    ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(f"%{keyword}%", f"%{keyword}%")
    )

    conn.close()

    return df


def statistics():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM scan_history
    WHERE barcode_type='QRCODE'
    """)
    qr = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM scan_history
    WHERE barcode_type!='QRCODE'
    """)
    barcode = cursor.fetchone()[0]

    conn.close()

    return total, qr, barcode


create_table()
