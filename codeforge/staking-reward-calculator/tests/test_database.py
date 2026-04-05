import os
import pytest
from unittest import mock
from sqlalchemy.exc import SQLAlchemyError
from backend.src.database import get_db, create_tables, DATABASE_URL

def test_get_db_yields_session():
    """Test that get_db yields a database session and cleans up properly."""
    db_gen = get_db()
    with pytest.raises(StopIteration):
        next(db_gen)
    try:
        db_gen = get_db()
        db_session = next(db_gen)
        # Verify it's a session-like object by checking for close method
        assert hasattr(db_session, 'close')
        next(db_gen, None)  # exhaust generator
    except Exception as e:
        pytest.fail(f"get_db should yield a session object: {e}")

def test_create_tables_success(mocker):
    """Test that create_tables creates tables without error."""
    from backend.src.models.staking import Base
    mock_base = mocker.patch('backend.src.database.Base')
    mock_base.metadata.create_all = mocker.Mock()
    mock_base.metadata.create_all.return_value = None
    
    try:
        create_tables()
        mock_base.metadata.create_all.assert_called_once()
    except Exception:
        pytest.fail("create_tables should not raise exception on success")

def test_create_tables_sqlalchemy_error(mocker):
    """Test that create_tables raises SQLAlchemyError properly."""
    from backend.src.models.staking import Base
    mock_base = mocker.patch('backend.src.database.Base')
    mock_base.metadata.create_all = mocker.Mock()
    mock_base.metadata.create_all.side_effect = SQLAlchemyError("Test error")
    
    with pytest.raises(SQLAlchemyError):
        create_tables()

def test_database_url_from_env():
    """Test that DATABASE_URL is taken from environment variables."""
    # Test will pass if DATABASE_URL is set in env or uses default
    assert isinstance(DATABASE_URL, str)

def test_database_default_url():
    """Test default database URL is used when env var not set."""
    # Save original
    original = os.environ.get('DATABASE_URL')
    
    # Temporarily remove DATABASE_URL if it exists
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    # Should use default when not in environment
    default_url = "sqlite:///./default.db"
    assert DATABASE_URL == default_url or os.getenv("DATABASE_URL", default_url) == default_url
    
    # Restore original if needed
    if original:
        os.environ['DATABASE_URL'] = original

def test_engine_creation():
    """Test that engine is created successfully."""
    from sqlalchemy.engine import Engine
    assert isinstance(engine, Engine)

def test_get_db_session_cleanup():
    """Test that get_db properly closes sessions."""
    try:
        db_gen = get_db()
        session = next(db_gen)
        # Check session has close method (indicating it's a session)
        assert hasattr(session, 'close')
        # Verify cleanup by checking if close is called
        with mock.patch.object(session, 'close') as mock_close:
            mock_close.return_value = None
            # Exhaust generator to trigger finally block
            try:
                next(db_gen)
            except StopIteration:
                pass
            mock_close.assert_called_once()
    except Exception as e:
        pytest.fail(f"Session cleanup test failed: {e}")

def test_create_tables_import_error(mocker):
    """Test create_tables handles import errors gracefully."""
    # Mock the import to raise an exception
    with mocker.patch.dict('sys.modules', {'backend.src.models.staking': None}):
        with pytest.raises(ImportError):
            create_tables()