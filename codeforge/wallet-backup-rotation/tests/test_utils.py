import pytest
from unittest.mock import patch
from datetime import datetime
from src.wallet_backup.utils import (
    get_current_timestamp,
    format_backup_name,
    get_backup_date,
    verify_backup_integrity
)

def test_get_current_timestamp():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01T12:00:00"
        result = get_current_timestamp()
        assert result == "2023-01-01T12:00:00"

def test_format_backup_name_with_timestamp():
    timestamp = "2023-01-01T12:00:00"
    with patch('src.wallet_backup.utils.get_current_timestamp', return_value=timestamp):
        name = format_backup_name("wallet123", timestamp)
        assert name == "wallet_backup_wallet123_2023-01-01T12-00-00.dat"

def test_format_backup_name_without_timestamp():
    with patch('src.wallet_backup.utils.get_current_timestamp', return_value="2023-01-01T12:00:00"):
        name = format_backup_name("wallet123")
        assert name == "wallet_backup_wallet123_2023-01-01T12-00-00.dat"

def test_get_backup_date():
    backup_name = "wallet_backup_wallet123_2023-01-01T12-00-00.dat"
    date = get_backup_date(backup_name)
    assert date == "2023-01-01T12-00-00"

def test_get_backup_date_no_match():
    backup_name = "invalid_backup_name"
    date = get_backup_date(backup_name)
    assert date == ""

def test_verify_backup_integrity_match():
    backup_data = b"test data"
    expected_hash = hashlib.sha256(backup_data).hexdigest()
    assert verify_backup_integrity(backup_data, expected_hash) == True

def test_verify_backup_integrity_mismatch():
    backup_data = b"test data"
    expected_hash = "wrong_hash"
    actual_result = verify_backup_integrity(backup_data, expected_hash)
    assert actual_result == False

def test_format_backup_name_colon_replacement():
    with patch('src.wallet_backup.utils.get_current_timestamp', return_value="2023-01-01T12:00:00"):
        name = format_backup_name("wallet123")
        assert "wallet_backup_wallet123_2023-01-01T12-00-00.dat" == name

def test_format_backup_name_custom_timestamp():
    name = format_backup_name("wallet123", "2023-01-01T12:00:00")
    assert name == "wallet_backup_wallet123_2023-01-01T12-00-00.dat"

def test_get_backup_date_with_custom_input():
    date = get_backup_date("wallet_backup_wallet123_2023-01-01T12-00-00.dat")
    assert date == "2023-01-01T12-00-00"

def test_get_backup_date_edge_cases():
    # Test with various inputs
    assert get_backup_date("") == ""
    assert get_backup_date("no_date_here") == ""

def test_format_backup_name_edge_cases():
    # Test empty wallet_id
    name = format_backup_name("")
    assert ".dat" in name or name.endswith('.dat')
    
    # Test with special characters in wallet_id
    name = format_backup_name("wallet$#123")
    assert "wallet$#123" in name

def test_verify_backup_integrity_edge_cases():
    # Test with empty data
    assert verify_backup_integrity(b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855") == True
    
    # Test data that produces known hash
    test_bytes = b"hello world"
    test_hash = "b94d27b9f5633e440d7d7c72de9a2d77e9f8673e325f064bb76a0d683f0b0f70"
    assert verify_backup_integrity(test_bytes, test_hash) == False

def test_get_current_timestamp_format():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01T12:00:00"
        result = get_current_timestamp()
        assert result == "2023-01-01T12:00:00"

def test_get_backup_date_parsing():
    # Test if it correctly parses date from name
    result = get_backup_date("wallet_backup_test_2023-01-01T12-00-00.dat")
    assert result == "2023-01-01T12-00-00"

def test_format_backup_name_timestamp_replacement():
    with patch('src.wallet_backup.utils.get_current_timestamp', return_value="2023-01-01T12:00:00"):
        name = format_backup_name("test")
        assert "2023-01-01T12-00-00" in name

def test_verify_backup_integrity_empty_data():
    empty_hash = hashlib.sha256(b"").hexdigest()
    assert verify_backup_integrity(b"", empty_hash) == True

def test_format_backup_name_with_colons():
    name = format_backup_name("wallet:123")
    assert "wallet:123" in name and ".dat" in name

def test_get_backup_date_various_inputs():
    # Valid date format
    assert get_backup_date("backup_2023-01-01T12-00-00") == "2023-01-01T12-00-00"
    # No date in string
    assert get_backup_date("backup_no_date") == ""

def test_edge_case_empty_wallet_id():
    name = format_backup_name("")
    assert name.startswith("wallet_backup__")

def test_get_current_timestamp_mock():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        result = get_current_timestamp()
        assert result == "2023-01-01T12:00:00"