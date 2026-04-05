import os
import sqlite3
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest
from src.database_manager import (
    initialize_db, save_articles, get_feed_urls, get_last_run_timestamp, 
    update_last_run_timestamp, get_db_path
)

def test_get_db_path_default():
    with patch.dict(os.environ, {}, clear=True):
        assert get_db_path() == 'data.db'

def test_get_db_path_from_env():
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
        assert get_db_path() == 'test.db'

def test_initialize_db_creates_tables():
    # Create a temporary database file
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Initialize the database
        initialize_db(tmp_path)
        
        # Check that tables exist
        conn = sqlite3.connect(tmp_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert 'articles' in tables
        assert 'feeds' in tables
        assert 'meta' in tables
        conn.close()
    finally:
        os.unlink(tmp_path)

def test_save_articles_empty_list():
    with patch('src.database_manager.get_db_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_cursor
        save_articles([], 'dummy.db')
        # Should not call execute if list is empty
        mock_cursor.execute.assert_not_called()

def test_save_articles_success():
    articles = [
        {
            'title': 'Test Article',
            'link': 'http://example.com/1',
            'description': 'Test description',
            'published_date': '2023-01-01T00:00:00',
            'feed_url': 'http://example.com'
        }
    ]
    
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        save_articles(articles, 'dummy.db')
        
        # Verify SQL was called
        mock_cursor.execute.assert_called()
        assert mock_cursor.execute.call_count >= 1

def test_get_feed_urls_success():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('http://feed1.com',), ('http://feed2.com',)]
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        urls = get_feed_urls()
        assert urls == ['http://feed1.com', 'http://feed2.com']

def test_get_feed_urls_exception():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_get_db.side_effect = Exception("DB Error")
        urls = get_feed_urls()
        assert urls == []

def test_get_last_run_timestamp_exists():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('2023-01-01T12:00:00',)
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        timestamp = get_last_run_timestamp()
        assert isinstance(timestamp, datetime)

def test_get_last_run_timestamp_not_exists():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        timestamp = get_last_run_timestamp()
        assert timestamp == datetime.min

def test_update_last_run_timestamp_insert():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Simulate no rows updated
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        update_last_run_timestamp()
        # Should call both UPDATE and INSERT
        assert mock_cursor.execute.call_count == 2

def test_update_last_run_timestamp_update():
    with patch('src.database_manager.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Simulate successful update
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        update_last_run_timestamp()
        # Should only call UPDATE
        assert mock_cursor.execute.call_count == 1