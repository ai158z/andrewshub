CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    description TEXT,
    published_date DATETIME NOT NULL,
    fetched_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    crypto_related BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    last_fetched DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_articles_link ON articles (link);
CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles (published_date);
CREATE INDEX IF NOT EXISTS idx_feeds_url ON feeds (url);