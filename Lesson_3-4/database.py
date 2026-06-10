import sqlite3

DB_PATH = "gamevault.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                genre       TEXT,
                year        INTEGER,
                rating      INTEGER,
                description TEXT,
                favorite    INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def add_game(name, genre, year, rating, description, favorite):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO games (name, genre, year, rating, description, favorite)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, genre, year, rating, description, int(favorite))
        )
        conn.commit()
        return cursor.lastrowid

def get_all_games():
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, name, genre, year, rating, description, favorite FROM games ORDER BY id DESC"
        )
        return cursor.fetchall()

def delete_game(game_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM games WHERE id = ?", (game_id,))
        conn.commit()