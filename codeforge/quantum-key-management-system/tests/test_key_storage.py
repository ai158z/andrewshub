import pytest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
from cryptography.fernet import Fernet

from src.core.key_storage import KeyStorage


@pytest.fixture
def key_storage():
    """Fixture to create a KeyStorage instance with a temporary storage path."""
    storage = KeyStorage("test_key_storage.json")
    return storage


@pytest.fixture
def mock_file_operations():
    """Mock file operations for testing."""
    with patch("os.path.exists") as mock_exists, \
         patch("builtins.open", mock_open(read_data="{}")) as mock_file:
        mock_exists.return_value = False
        yield mock_file


def test_init_with_default_storage_path():
    with patch("os.path.exists") as mock_exists, \
         patch("builtins.open", mock_open(read_data="{}")):
        mock_exists.return_value = False
        storage = KeyStorage()
        assert storage.storage_path == "key_storage.json"


def test_init_loads_existing_storage(mock_file_operations):
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        with patch("json.load", return_value={"key1": {"data": "encrypted_data", "hash": "abc123"}}):
            storage = KeyStorage("test_path")
            assert "key1" in storage.keys


def test_store_key_success(key_storage):
    key_data = b"test_key_data"
    result = key_storage.store_key("test_key", key_data)
    assert result is True
    assert key_storage.key_exists("test_key") is True


def test_store_key_with_metadata(key_storage):
    key_data = b"test_key_data"
    metadata = {"created_by": "test_user", "purpose": "testing"}
    key_storage.store_key("test_key", key_data, metadata)
    stored_metadata = key_storage.get_key_metadata("test_key")
    assert stored_metadata == metadata


def test_store_key_encryption(key_storage):
    key_data = b"sensitive_key_data"
    key_storage.store_key("encrypted_key", key_data)
    
    # Verify that stored data is encrypted
    key_info = key_storage.keys["encrypted_key"]
    assert key_info["data"] != key_data.decode('utf-8')  # Should be encrypted
    assert key_info["hash"] == "8d5e5b4f5e3f8c6c4f3e5b4e3f8c6c4f3e5b4e3f8c6c4f3e5b4e3f8c6c4f3e5b"  # Mocked hash


def test_retrieve_key_success(key_storage):
    key_data = b"test_key_data"
    key_storage.store_key("retrieval_key", key_data)
    
    retrieved_data = key_storage.retrieve_key("retrieval_key")
    assert retrieved_data == key_data


def test_retrieve_key_not_found(key_storage):
    result = key_storage.retrieve_key("nonexistent_key")
    assert result is None


def test_retrieve_key_decryption_failure(key_storage):
    key_data = b"test_key_data"
    key_storage.store_key("bad_key", key_data)
    
    # Corrupt the encryption key to cause decryption failure
    original_key = key_storage.encryption_key
    key_storage.encryption_key = Fernet.generate_key()
    key_storage.cipher_suite = Fernet(key_storage.encryption_key)
    
    result = key_storage.retrieve_key("bad_key")
    assert result is None


def test_delete_key_success(key_storage):
    key_storage.store_key("delete_key", b"test_data")
    result = key_storage.delete_key("delete_key")
    assert result is True
    assert not key_storage.key_exists("delete_key")


def test_delete_key_not_exists(key_storage):
    result = key_storage.delete_key("nonexistent_key")
    assert result is False


def test_key_exists(key_storage):
    key_storage.store_key("exists_key", b"test_data")
    assert key_storage.key_exists("exists_key") is True
    assert key_storage.key_exists("nonexistent_key") is False


def test_list_keys(key_storage):
    key_storage.store_key("key1", b"data1")
    key_storage.store_key("key2", b"data2")
    keys = key_storage.list_keys()
    assert "key1" in keys
    assert "key2" in keys
    assert len(keys) == 2


def test_get_key_metadata(key_storage):
    metadata = {"owner": "alice", "permissions": "read-only"}
    key_storage.store_key("meta_key", b"key_data", metadata)
    result = key_storage.get_key_metadata("meta_key")
    assert result == metadata


def test_get_key_metadata_not_found(key_storage):
    result = key_storage.get_key_metadata("nonexistent_key")
    assert result is None


def test_update_metadata_success(key_storage):
    key_storage.store_key("update_key", b"key_data")
    new_metadata = {"updated": True, "version": "1.0"}
    result = key_storage.update_metadata("update_key", new_metadata)
    assert result is True
    metadata = key_storage.get_key_metadata("update_key")
    assert metadata.get("updated") is True


def test_update_metadata_key_not_found(key_storage):
    result = key_storage.update_metadata("nonexistent_key", {"test": "data"})
    assert result is False


def test_update_metadata_file_save_failure(key_storage):
    key_storage.store_key("save_key", b"key_data")
    
    with patch("src.core.key_storage.KeyStorage._save_storage") as mock_save:
        mock_save.side_effect = Exception("Save failed")
        result = key_storage.update_metadata("save_key", {"fail_test": True})
        assert result is False


def test_concurrent_access(key_storage):
    import threading
    import time
    
    key_data = b"concurrent_test_data"
    
    def store_key():
        key_storage.store_key("concurrent_key", key_data)
    
    # Simulate concurrent access with multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=store_key)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Should only store once due to locking
    assert key_storage.key_exists("concurrent_key") is True
    assert key_storage.retrieve_key("concurrent_key") == key_data


def test_thread_safety_during_operations(key_storage):
    import threading
    
    # Test that concurrent operations don't corrupt data
    def operation():
        key_storage.store_key("thread_key", b"thread_data")
        key_storage.retrieve_key("thread_key")
        key_storage.delete_key("thread_key")
    
    threads = [threading.Thread(target=operation) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # After all operations, key should not exist
    assert key_storage.key_exists("thread_key") is False


def test_persistence_across_instances(key_storage):
    key_storage.store_key("persistent_key", b"persistent_data")
    
    # Create new instance to simulate restart
    new_storage = KeyStorage(key_storage.storage_path)
    assert new_storage.key_exists("persistent_key") is True
    assert new_storage.retrieve_key("persistent_key") == b"persistent_data"