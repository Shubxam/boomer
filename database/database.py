"""
Database module for the Bookmark Manager application.

This module provides the core functionality for storing and retrieving bookmarks.
It implements a SQLite-based persistence layer with support for full-text search,
tagging, and bookmark categorization.

Classes:
    DuplicateBookmarkError: Custom exception for duplicate bookmark entries
    BookmarkDatabase: Main database handler for bookmark operations

Database Schema:
    - bookmarks: Stores bookmark metadata (URL, title, description, etc.)
    - tags: Stores available tags for categorizing bookmarks
    - bookmark_tags: Junction table linking bookmarks to tags
    - bookmark_fts: Full-text search virtual table for efficient text searching
"""

import contextlib
import os
import sqlite3
import sys
from datetime import datetime

sys.path.append(os.getcwd())

from config import DB_FILE


class DuplicateBookmarkError(ValueError):
    """Exception raised when attempting to add a bookmark that already exists."""

    pass


class BookmarkDatabase:
    """Manages bookmark storage and retrieval operations.

    This class provides a database interface for the Bookmark Manager application,
    handling bookmark CRUD operations, tagging, and text search capabilities.
    """

    def __init__(self, db_file=DB_FILE):
        """Initialize the database connection and ensure tables exist.

        Args:
            db_file: Path to the SQLite database file.
                Defaults to the value specified in config.DB_FILE.
        """
        self.db_file = db_file
        # Create tables on initialization
        with self.get_connection() as conn:
            self._create_tables(conn)

    @contextlib.contextmanager
    def get_connection(self):
        """Context manager for database connections.

        Creates and manages a database connection that automatically handles
        commits and rollbacks based on whether operations succeed or fail.

        Yields:
            An active database connection with row_factory set to sqlite3.Row
            for dictionary-like access to rows.
        """
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_tables(self, conn):
        """Create necessary database tables if they don't exist.

        Sets up the database schema including tables for bookmarks, tags,
        and the relationship between them. Also configures full-text search
        capabilities and necessary triggers.

        Args:
            conn: An active database connection.
        """
        cursor = conn.cursor()

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

        # Create triggers to keep FTS index in sync with bookmarks table
        # Trigger for new bookmarks
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS bookmarks_ai AFTER INSERT ON bookmarks BEGIN
                INSERT INTO bookmark_fts(rowid, title, description, content_snippet)
                VALUES (new.id, new.title, new.description, new.content_snippet);
            END;
        """)

        # Trigger for updated bookmarks
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS bookmarks_au AFTER UPDATE ON bookmarks BEGIN
                UPDATE bookmark_fts SET
                    title = new.title,
                    description = new.description,
                    content_snippet = new.content_snippet
                WHERE rowid = old.id;
            END;
        """)

        # Trigger for deleted bookmarks
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS bookmarks_ad AFTER DELETE ON bookmarks BEGIN
                DELETE FROM bookmark_fts WHERE rowid = old.id;
            END;
        """)

        # Initial population of FTS table if it might be empty
        # but bookmarks table has data (handles existing databases)
        cursor.execute("""
            INSERT OR IGNORE INTO bookmark_fts(rowid, title, description, content_snippet)
            SELECT id, title, description, content_snippet FROM bookmarks
        """)

    def add_bookmark(self, title, url, description=None, content_snippet=None, source=None):
        """Add a new bookmark to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO bookmarks (title, url, description, content_snippet, source, date_added)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (title, url, description, content_snippet, source, datetime.now()),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            # Handle unique constraint violation
            raise DuplicateBookmarkError() from e

    def get_bookmarks(self):
        """Retrieve all bookmarks from the database.

        Returns:
            A list of sqlite3.Row objects representing bookmarks.
            Each row can be accessed like a dictionary.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM bookmarks")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving bookmarks: {e}")
            return []

    def delete_bookmark(self, bookmark_id):
        """Delete a bookmark by its ID.

        Removes a bookmark entry and all associated data (tags, etc.) from the database.
        Due to CASCADE constraints, related entries in junction tables will also be removed.

        Args:
            bookmark_id: The ID of the bookmark to delete

        Returns:
            True if the bookmark was successfully deleted, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting bookmark: {e}")
            return False

    def search_bookmarks(self, query):
        """Search bookmarks using full-text search.

        Performs a search across bookmark titles, descriptions, and content snippets
        using SQLite's FTS5 extension for efficient full-text search capability.

        Args:
            query: The search query to find matching bookmarks

        Returns:
            A list of sqlite3.Row objects representing matching bookmarks,
            ordered by relevance rank
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Using the FTS5 table to perform the search
                cursor.execute(
                    """
                    SELECT b.*
                    FROM bookmark_fts fts
                    JOIN bookmarks b ON fts.rowid = b.id
                    WHERE bookmark_fts MATCH ?
                    ORDER BY rank
                """,
                    (query,),
                )
                return cursor.fetchall()
        except Exception as e:
            print(f"Error searching bookmarks: {e}")
            return []


if __name__ == "__main__":
    # Example usage
    db = BookmarkDatabase()
    db.add_bookmark("Example Title", "http://example.com", "Example Description")
    bookmarks = db.get_bookmarks()
    for bookmark in bookmarks:
        print(dict(bookmark))
    db.delete_bookmark(1)
    print(db.get_bookmarks())
