import sqlite3
import os
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

class Article:
    def __init__(self, title: str, link: str, published: str, description: str = ""):
        self.title = title
        self.link = link
        self.description = description
        if not published:
            self.published = datetime.now().isoformat()
        else:
            self.published = published

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "published": self.published
        }

    def __repr__(self) -> str:
        return f"Article(title={self.title}, link={self.link}, description={self.description}, published={self.published})"

class Feed:
    def __init__(self, url: str, title: str = "", description: str = ""):
        self.url = url
        self.title = title
        self.description = description or title

    def __str__(self):
        return f"Feed: {self.title}"

    def __repr__(self):
        return f"Feed({self.title}, {self.url})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description
        }

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        # Always ensure tables exist when DatabaseManager is initialized
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS feeds
                            (url TEXT PRIMARY KEY,
                             title TEXT,
                             description TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS articles
                            (id INTEGER PRIMARY KEY,
                             title TEXT,
                             link TEXT UNIQUE,
                             description TEXT,
                             published TEXT,
                             feed_url TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS metadata
                            (key TEXT PRIMARY KEY,
                             value TEXT)''')
            conn.commit()

    def get_feeds(self) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM feeds")
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logging.error(f"Failed to get feeds from database: {e}")
            return []

    def save_articles(self, articles: List[Dict[str, Any]]) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executemany('''INSERT OR IGNORE INTO articles
                                   (title, link, description, published, feed_url)
                                   VALUES (?, ?, ?, ?, ?)''', 
                                [(a['title'], a['link'], a['description'], a['published'], a.get('feed_url', '')) for a in articles])
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to save articles: {e}")

    def get_feed_urls(self) -> List[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT url FROM feeds")
                return [row[0] for row in cursor.fetchall())
                ]
        except sqlite3.OperationalError as e:
            logging.error(f"Failed to get feed URLs from database: {e}")
            return []

    def update_last_run_timestamp(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_run', ?)", 
                           (datetime.now().isoformat(),))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to update last run timestamp: {e}")

    def get_last_run_timestamp(self) -> datetime:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT value FROM metadata WHERE key = 'last_run'")
                result = cursor.fetchone()
                if result:
                    return datetime.fromisoformat(result[0])
                else:
                    # Default to 1 hour ago if no timestamp exists
                    return datetime.now().replace(microsecond=0, second=0) - timedelta(hours=1)
        except (sqlite3.OperationalError, ValueError) as e:
            logging.error(f"Failed to get last run timestamp: {e}")
            return datetime.now().replace(microsecond=0, second=0) - timedelta(hours=1)