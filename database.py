import sqlite3
from config import DATABASE_NAME


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_hash BLOB NOT NULL,
            salt BLOB NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def user_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def save_user(master_hash, salt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (master_hash, salt) VALUES (?, ?)",
        (master_hash, salt)
    )
    conn.commit()
    conn.close()


def get_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT master_hash, salt FROM users LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    return user


def add_credential(website, username, password, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO credentials (website, username, password, notes)
        VALUES (?, ?, ?, ?)
    """, (website, username, password, notes))
    conn.commit()
    conn.close()


def get_credentials():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, website, username, password, notes, created_at
        FROM credentials
        ORDER BY created_at DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def search_credentials(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, website, username, password, notes, created_at
        FROM credentials
        WHERE website LIKE ? OR username LIKE ?
        ORDER BY created_at DESC
    """, (f"%{keyword}%", f"%{keyword}%"))
    data = cursor.fetchall()
    conn.close()
    return data


def update_credential(credential_id, website, username, password, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE credentials
        SET website = ?, username = ?, password = ?, notes = ?
        WHERE id = ?
    """, (website, username, password, notes, credential_id))
    conn.commit()
    conn.close()


def delete_credential(credential_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credentials WHERE id = ?", (credential_id,))
    conn.commit()
    conn.close()