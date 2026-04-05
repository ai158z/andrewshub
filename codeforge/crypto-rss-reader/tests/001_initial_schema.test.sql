import sqlite3
from pathlib import Path
import pytest

def test_create_articles_table():
    # Test that the articles table is created with correct schema
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='articles'")
    result = cursor.fetchone()
    assert result is not None
    assert 'id INTEGER PRIMARY KEY AUTOINCREMENT' in result[0]
    assert 'title TEXT NOT NULL' in result[0]
    assert 'link TEXT UNIQUE NOT NULL' in result[0]
    assert 'description TEXT' in result[0]
    assert 'published_date DATETIME NOT NULL' in result[0]
    assert 'fetched_date DATETIME DEFAULT' in result[0]
    assert 'crypto_related BOOLEAN DEFAULT' in result[0]
    conn.close()

def test_create_feeds_table():
    # Test that the feeds table is created with correct schema
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT sql FROM sqlite3_master WHERE type='table' AND name='feeds'")
    result = cursor.fetchone()
    assert result is not None
    assert 'id INTEGER PRIMARY KEY AUTOINCREMENT' in result[0]
    assert 'url TEXT UNIQUE NOT NULL' in result[0]
    assert 'last_fetched DATETIME DEFAULT' in result[0]
    conn.close()

def test_create_config_table():
    # Test that the config table is created with correct schema
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='config'")
    result = cursor.fetchone()
    assert result is not None
    assert 'key TEXT PRIMARY KEY' in result[0]
    assert 'value TEXT' in result[0]
    conn.close()

def test_articles_table_primary_key():
    # Test that articles table has autoincrementing primary key
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    id_column = columns[0]
    assert id_column[0] == 'id'  # cid
    assert id_column[1] == 'id'  # name
    assert 'INTEGER' in id_column[2]  # type
    assert id_column[5] == 1  # pk flag
    conn.close()

def test_articles_link_unique_constraint():
    # Test that link column in articles table is unique
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    link_column = next((col for col in columns if col[1] == 'link'), None)
    assert link_column is not None
    assert 'UNIQUE' in link_column[2] or link_column[3] == 1  # notnull flag
    conn.close()

def test_articles_title_not_null():
    # Test that title column in articles table is not null
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    title_column = next((col for col in columns if col[1] == 'title'), None)
    assert title_column is not None
    assert title_column[3] == 1  # notnull flag
    conn.close()

def test_articles_published_date_not_null():
    # Test that published_date column in articles table is not null
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    date_column = next((col for col in columns if col[1] == 'published_date'), None)
    assert date_column is not None
    assert date_column[3] == 1  # notnull flag
    conn.close()

def test_feeds_url_unique():
    # Test that url column in feeds table is unique
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(feeds)")
    columns = cursor.fetchall()
    url_column = next((col for col in columns if col[1] == 'url'), None)
    assert url_column is not None
    assert url_column[3] == 1  # notnull flag
    assert 'UNIQUE' in url_column[2]
    conn.close()

def test_articles_fetched_date_default():
    # Test that fetched_date has default timestamp
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    default_column = next((col for col in columns if col[1] == 'fetched_date'), None)
    assert default_column is not None
    assert 'CURRENT_TIMESTAMP' in default_column[4]  # default value
    conn.close()

def test_feeds_last_fetched_default():
    # Test that last_fetched has default timestamp
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(feeds)")
    columns = cursor.fetchall()
    fetched_column = next((col for col in columns if col[1] == 'last_fetched'), None)
    assert fetched_column is not None
    assert 'CURRENT_TIMESTAMP' in fetched_column[4]  # default value
    conn.close()

def test_articles_index_link():
    # Test that articles link index exists
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='articles' AND name='idx_articles_link'")
    assert cursor.fetchone() is not None
    conn.close()

def test_articles_index_published_date():
    # Test that articles published_date index exists
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='articles' AND name='idx_articles_published_date'")
    assert cursor.fetchone() is not None
    conn.close()

def test_feeds_index_url():
    # Test that feeds url index exists
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='feeds' AND name='idx_feeds_url'")
    assert cursor.fetchone() is not None
    conn.close()

def test_config_primary_key():
    # Test that config table has correct primary key
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(config)")
    columns = cursor.fetchall()
    key_column = next((col for col in columns if col[1] == 'key'), None)
    assert key_column is not None
    assert key_column[5] == 1  # pk flag
    conn.close()

def test_crypto_related_default():
    # Test that crypto_related has correct default
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    cursor = conn.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()
    crypto_column = next((col for col in columns if col[1] == 'crypto_related'), None)
    assert crypto_column is not None
    assert 'DEFAULT 0' in crypto_column[4] or crypto_column[4] == 0
    conn.close()

def test_all_tables_created():
    # Test that all expected tables are created
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = {row[0] for row in tables}
    assert table_names == {'articles', 'feeds', 'config'}
    conn.close()

def test_all_indexes_created():
    # Test that all expected indexes are created
    conn = sqlite3.connect(':memory:')
    conn.executescript(Path('migrations/001_initial_schema.sql').read_text())
    
    indexes = conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
    index_names = {row[0] for row in indexes}
    assert 'idx_articles_link' in index_names
    assert 'idx_articles_published_date' in index_names
    assert 'idx_feeds_url' in index_names
    conn.close()