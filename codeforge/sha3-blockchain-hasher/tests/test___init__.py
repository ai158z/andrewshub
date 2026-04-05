import pytest
from unittest.mock import patch, MagicMock
import logging
from sha3_hasher import (
    get_version,
    __version__,
    __version_info__,
    DATABASE_URL,
    REDIS_URL,
    sha3_512_hash,
    benchmark_hashing_speed,
    create_ros2_node,
    util_sha3_512_hash
)

def test_get_version_returns_correct_version():
    assert get_version() == __version__

def test_version_info_tuple_matches_version_string():
    version_from_tuple = '.'.join(map(str, __version_info__))
    assert version_from_tuple == __version__

def test_database_url_from_environment():
    with patch.dict('os.environ', {'DATABASE_URL': 'test_db_url'}):
        import sha3_hasher
        assert sha3_hasher.DATABASE_URL == 'test_db_url'

def test_redis_url_from_environment():
    with patch.dict('os.environ', {'REDIS_URL': 'test_redis_url'}):
        import sha3_hasher
        assert sha3_hasher.REDIS_URL == 'test_redis_url'

def test_database_url_none_when_not_set():
    with patch.dict('os.environ', clear=True):
        import sha3_hasher
        assert sha3_hasher.DATABASE_URL is None

def test_redis_url_none_when_not_set():
    with patch.dict('os.environ', clear=True):
        import sha3_hasher
        assert sha3_hasher.REDIS_URL is None

def test_get_version_returns_string():
    version = get_version()
    assert isinstance(version, str)
    assert version == __version__

def test_sha3_512_hash_function_exists():
    assert callable(sha3_512_hash)

def test_benchmark_hashing_speed_function_exists():
    assert callable(benchmark_hashing_speed)

def test_create_ros2_node_function_exists():
    assert callable(create_ros2_node)

def test_util_sha3_512_hash_function_exists():
    assert callable(util_sha3_512_hash)

@patch('sha3_hasher.core.sha3_512_hash')
def test_sha3_512_hash_called_with_correct_input(mock_hash):
    mock_hash.return_value = 'test_hash'
    result = sha3_512_hash('test')
    mock_hash.assert_called_once_with('test')
    assert result == 'test_hash'

@patch('sha3_hasher.benchmark.benchmark_hashing_speed')
def test_benchmark_hashing_speed_called_with_correct_args(mock_bench):
    mock_bench.return_value = 100
    result = benchmark_hashing_speed(10)
    mock_bench.assert_called_once_with(10)
    assert result == 100

@patch('sha3_hasher.ros2_node.create_ros2_node')
def test_create_ros2_node_called_with_correct_args(mock_node):
    mock_node.return_value = MagicMock()
    result = create_ros2_node('test_node')
    mock_node.assert_called_once_with('test_node')
    assert isinstance(result, MagicMock)

@patch('sha3_hasher.utils.sha3_512_hash')
def test_util_sha3_512_hash_called_with_correct_input(mock_hash):
    mock_hash.return_value = 'util_hash'
    result = util_sha3_512_hash('test')
    mock_hash.assert_called_once_with('test')
    assert result == 'util_hash'

def test_logger_configured():
    import logging
    logger = logging.getLogger('sha3_hasher')
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0

@patch('sha3_hasher.logger')
def test_logger_handler_configured(mock_logger):
    with patch('sha3_hasher.logger.handlers', []):
        # Force reimport to test handler configuration
        import importlib
        import sha3_hasher
        importlib.reload(sha3_hasher)
        assert len(sha3_hasher.logger.handlers) > 0

def test_all_public_functions_imported():
    public_functions = [
        get_version,
        sha3_512_hash,
        benchmark_hashing_speed,
        create_ros2_node,
        util_sha3_512_hash
    ]
    for func in public_functions:
        assert callable(func)

def test_version_constants_defined():
    assert __version__ is not None
    assert isinstance(__version_info__, tuple)
    assert len(__version_info__) == 3

def test_module_level_logger_exists():
    import sha3_hasher
    assert hasattr(sha3_hasher, 'logger')
    assert isinstance(sha3_hasher.logger, logging.Logger)