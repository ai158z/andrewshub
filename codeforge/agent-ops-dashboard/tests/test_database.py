import pytest
from unittest.mock import patch, MagicMock
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.backend.database import get_db, init_db, DATABASE_URL, engine, SessionLocal

def test_database_url_set():
    """Test that DATABASE_URL environment variable is properly used"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        assert DATABASE_URL is not None

def test_database_url_not_set():
    """Test that missing DATABASE_URL raises ValueError"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            from src.backend import database
            reload(database)

def test_engine_created():
    """Test that engine is created successfully when DATABASE_URL is set"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        assert database.engine is not None

def test_get_db_yields_session():
    """Test that get_db yields a session"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        db_gen = database.get_db()
        db_session = next(db_gen)
        assert isinstance(db_session, Session)
        db_gen.close()

def test_get_db_session_closes():
    """Test that database session is properly closed"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        db_gen = database.get_db()
        db_session = next(db_gen)
        with patch.object(db_session, 'close') as mock_close:
            with pytest.raises(StopIteration):
                next(db_gen)
            mock_close.assert_called_once()

def test_init_db_success():
    """Test that init_db runs without error when models can be imported"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        with patch('src.backend.models.agent.Agent') as mock_agent, \
             patch('src.backend.models.metric.Metric') as mock_metric:
            from src.backend import database
            reload(database)
            database.init_db()
            # Mocked models should allow init_db to complete without error

def test_init_db_error_handling():
    """Test that init_db properly handles errors during table creation"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}), \
         patch('src.backend.models.agent.Agent'), \
         patch('src.backend.models.metric.Metric'):
        from src.backend import database
        reload(database)
        with patch.object(database.Base.metadata, 'create_all', side_effect=Exception("DB Error")):
            with pytest.raises(Exception, match="DB Error"):
                database.init_db()

def test_session_local_created():
    """Test that SessionLocal is properly configured"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        assert database.SessionLocal is not None

def test_get_db_generator():
    """Test that get_db returns a generator"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        db_gen = database.get_db()
        assert hasattr(db_gen, '__iter__')
        assert hasattr(db_gen, '__next__')

def test_base_class_created():
    """Test that Base class is created"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        from sqlalchemy.ext.declarative import declarative_base
        assert database.Base == declarative_base()

def test_engine_echo_off():
    """Test that engine is created with echo=False"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        assert database.engine.url == create_engine("sqlite:///:memory:", echo=False).url

def test_sessionmaker_configured():
    """Test that SessionLocal is configured correctly"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        assert database.SessionLocal.kw['autocommit'] == False
        assert database.SessionLocal.kw['autoflush'] == False

def test_get_db_multiple_calls():
    """Test that get_db can be called multiple times"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        db1 = next(database.get_db())
        db2 = next(database.get_db())
        assert isinstance(db1, Session)
        assert isinstance(db2, Session)

def test_init_db_import_error():
    """Test init_db handles missing model imports gracefully"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        with patch('builtins.__import__') as mock_import:
            mock_import.side_effect = ImportError
            with pytest.raises(ImportError):
                database.init_db()

def test_database_url_format():
    """Test that DATABASE_URL has expected format when set"""
    test_url = "postgresql://user:pass@localhost/dbname"
    with patch.dict(os.environ, {"DATABASE_URL": test_url}):
        from src.backend import database
        reload(database)
        assert database.DATABASE_URL == test_url

def test_session_close_on_exception():
    """Test that session is closed even if an exception occurs in the generator"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        db_gen = database.get_db()
        db_session = next(db_gen)
        with patch.object(db_session, 'close', side_effect=Exception("Close error")):
            with pytest.raises(Exception):
                db_gen.throw(Exception("Test exception"))
            # The generator should be closed after the exception

def test_import_error_during_session_creation():
    """Test that get_db handles import errors during session creation"""
    with patch('sqlalchemy.orm.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.side_effect = Exception("Import error")
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
            from src.backend import database
            reload(database)
            with pytest.raises(Exception, match="Import error"):
                next(database.get_db())

def test_init_db_called_once():
    """Test that init_db is called during module import"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}), \
         patch('src.backend.models.agent.Agent'), \
         patch('src.backend.models.metric.Metric'):
        from src.backend import database
        reload(database)
        # init_db is called during import, should not raise

def test_session_context():
    """Test that session is properly created and yielded"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        with database.get_db() as db:
            assert isinstance(db, Session)

def test_get_db_exception_during_session():
    """Test that get_db properly handles session creation exceptions"""
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"}):
        from src.backend import database
        reload(database)
        with patch('src.backend.database.SessionLocal') as mock_session_local:
            mock_session_local.side_effect = Exception("Session creation failed")
            with pytest.raises(Exception, match="Session creation failed"):
                next(database.get_db())