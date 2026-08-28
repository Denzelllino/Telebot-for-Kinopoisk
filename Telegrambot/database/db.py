import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        search_date TEXT NOT NULL,
        title TEXT,
        description TEXT,
        rating REAL,
        year TEXT,
        genre TEXT,
        age_rating TEXT,
        poster TEXT,
        media_type TEXT,
        viewed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def save_item(user_id, item, search_date=None):
    conn = connect()
    cur = conn.cursor()
    search_date = search_date or datetime.now().strftime("%Y-%m-%d")

    title = item.get("title") or item.get("name") or ""
    description = item.get("description") or item.get("shortDescription") or item.get("overview") or ""
    rating = item.get("rating")
    if isinstance(rating, dict):
        rating = rating.get("kp")
    year = str(item.get("year") or "")
    genre = ", ".join(g.get("name", "") for g in item.get("genres", []) if g.get("name"))
    age_rating = str(item.get("ageRating") or item.get("ratingMpaa") or "")
    poster = item.get("poster")
    if isinstance(poster, dict):
        poster = poster.get("url") or ""
    media_type = item.get("type") or ""

    cur.execute("""
    INSERT INTO history
    (user_id, search_date, title, description, rating, year, genre, age_rating, poster, media_type, viewed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (user_id, search_date, title, description, rating, year, genre, age_rating, poster, media_type))
    conn.commit()
    conn.close()

def get_history(user_id, search_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, search_date, title, description, rating, year, genre, age_rating, poster, viewed
    FROM history
    WHERE user_id=? AND search_date=?
    ORDER BY id DESC
    """, (user_id, search_date))
    rows = cur.fetchall()
    conn.close()
    return rows

def set_viewed(history_id, viewed):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE history SET viewed=? WHERE id=?", (1 if viewed else 0, history_id))
    conn.commit()
    conn.close()