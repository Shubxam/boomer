import sqlite3

from config import DB_FILE


class BookmarkDatabase:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()

        # Create bookmarks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                date_added TIMESTAMP NOT NULL,
                content_snippet TEXT,
                source TEXT
            )
        """)

        # Create tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                auto_generated BOOLEAN
            )
        """)

        # Create bookmark_tags junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmark_tags (
                bookmark_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                confidence FLOAT,
                PRIMARY KEY (bookmark_id, tag_id),
                FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)

        # Create full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS bookmark_fts USING fts5(
                title,
                description,
                content_snippet,
                content=bookmarks
            )
        """)

        self.conn.commit()

    def add_bookmark(self, title, url):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO bookmarks (title, url)
            VALUES (?, ?)
        """,
            (title, url),
        )
        self.conn.commit()

    def get_bookmarks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bookmarks")
        return cursor.fetchall()

    def delete_bookmark(self, bookmark_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
