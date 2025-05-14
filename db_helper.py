import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "database.db"


def init_db():
    with sqlite3.connect(db_path) as connection:
        cur = connection.cursor()

    # ich mache zwei Tabellen: categories and words,
    # um die Funktionalität des Spieles zu erweitern
        cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                )
            """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    word TEXT NOT NULL UNIQUE,
                    letters INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                )
            """)
        # Befüllung mit Daten
        cur.executemany(
            "INSERT OR IGNORE INTO categories (id, name) VALUES (?, ?)",
            [(1, "Die Natur"), (2, "Data Science"), (3, "Technik")]
        )

        natur_words = [
            ("ZUG", 3, 1), ("WEG", 3, 1), ("TOR", 3, 1),
            ("SEE", 3, 1), ("BAUM", 4, 1), ("WALD", 4, 1),
            ("BERG", 4, 1), ("MOND", 4, 1), ("ERDE", 4, 1), ("LUFT", 4, 1),
            ("WOLKE", 5, 1), ("STERN", 5, 1), ("WIESE", 5, 1),
            ("REGEN", 5, 1), ("BLUME", 5, 1), ("BLATT", 5, 1), ("VOGEL", 5, 1),
            ("SONNE", 5, 1), ("FLUSS", 5, 1), ("MEER", 4, 1),
            ("GEBIRGE", 7, 1), ("NATUR", 5, 1), ("NEBELIG", 7, 1),
            ("GEWITTER", 8, 1), ("LAVASTROM", 9, 1)]

        ds_words = [
            ("AI", 2, 2), ("SQL", 3, 2), ("CSV", 3, 2),
            ("DATA", 4, 2), ("GRID", 4, 2), ("CODE", 4, 2),
            ("NODE", 4, 2), ("DEEP", 4, 2),  ("MODEL", 5, 2),
            ("CLOUD", 5, 2), ("FRAME", 5, 2), ("TRAIN", 5, 2),
            ("LABEL", 5, 2), ("TOKEN", 5, 2), ("LOGIC", 5, 2), ("PYTHON", 6, 2),
            ("TENSOR", 6, 2), ("KERNEL", 6, 2), ("SCIKIT", 6, 2), ("PANDAS", 6, 2),
            ("NUMPY", 5, 2), ("BIGDATA", 7, 2), ("LEARNING", 8, 2),
            ("DATABASE", 8, 2), ("ALGORITHM", 9, 2)]

        technik_words = [
            ("RAD", 3, 3), ("TV", 2, 3), ("BOHR", 4, 3),
            ("KABEL", 5, 3), ("MOTOR", 5, 3), ("ROBOT", 5, 3),
            ("LAMPE", 5, 3), ("LASER", 5, 3), ("RADAR", 5, 3),
            ("DRUCK", 5, 3), ("STROM", 5, 3), ("SENSOR", 6, 3),
            ("DRUCKER", 7, 3), ("KAMERA", 6, 3), ("BILDSCHIRM", 10, 3),
            ("LÜFTER", 6, 3), ("AKKU", 4, 3), ("STECKER", 7, 3),
            ("KÜHLER", 7, 3), ("PLATINE", 7, 3), ("SCHALTER", 8, 3),
            ("ANTENNE", 7, 3), ("MONITOR", 7, 3), ("BATTERIE", 8, 3),
            ("PROZESSOR", 9, 3)]

        cur.execute("SELECT COUNT(*) FROM words")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO words (word, letters, category_id) VALUES (?, ?, ?)",
                natur_words + ds_words+technik_words
            )
        connection.commit()


def get_random_word(category_id=None):
    with sqlite3.connect(db_path) as connection:
        cur = connection.cursor()
        query = "SELECT word FROM words"
        params = ()

        if category_id:
            query += " WHERE category_id = ?"
            params = (category_id,)

        query += " ORDER BY RANDOM() LIMIT 1"

        cur.execute(query, params)
        result = cur.fetchone()
        return result[0] if result else None


def get_categories():
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cur = connection.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
        if cur.fetchone():
            cur.execute("SELECT id, name FROM categories")
            return {row[0]: row[1] for row in cur.fetchall()}
        return {}


if __name__ == "__main__":
    init_db() 
    print("Die Tabelle:", get_categories())
    print("Path:", db_path.absolute())