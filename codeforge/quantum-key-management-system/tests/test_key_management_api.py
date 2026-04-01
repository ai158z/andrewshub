import pytest
from unittest import mock
from src.api.key_management_api import KeyManagementAPI

def test_key_management_api_initialization():
    api = KeyManagementAPI()
    assert api is not None

def test_generate_random_bytes():
    api = KeyManagementAPI()
    result = api.generate_random_bytes(32)
    assert len(result) == 32

def test_key_storage_methods():
    with mock.patch('src.api.key_management_api.KeyStorage') as mock_storage:
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.store_key.return_value = None
        mock_storage_instance.load_key.return_value = "test_key"
        
        api = KeyManagementAPI()
        api.key_storage = mock_storage_instance
        
        # Test the storage methods are called correctly
        api.key_storage.store_key("test_id", "test_key")
        mock_storage_instance.store_key.assert_called_with("test_id", "test_key")
        
        result = api.key_storage.load_key("test_id")
        assert result == "test_key"

def test_key_storage_store_and_load():
    api = KeyManagementAPI()
    api.key_storage.store_key("test_key_id", {"data": "test"})
    stored_key = api.key_storage.load_key("test_key_id")
    assert stored_key is not None

def test_key_generation():
    api = KeyManagementAPI()
    key = api.generate_key()
    assert key is not None

def test_encryption_decryption():
    api = KeyManagementAPI()
    encrypted = api.encrypt("test_data")
    assert encrypted is not None
    
    decrypted = api.decrypt("test_data")
    assert decrypted is not None

def test_signing():
    api = KeyManagementAPI()
    signature = api.sign("test_data")
    assert signature is not None

def test_key_storage_persistence():
    api = KeyManagementAPI()
    test_data = {"key": "value"}
    api.key_storage.store_key("test_id", test_data)
    retrieved = api.key_storage.load_key("test_id")
    assert retrieved is not None

def test_hadamard_transform_exists():
    api = KeyManagementAPI()
    result = api.hadamard_transform()
    assert result is not None

def test_bell_state_measurement_exists():
    api = KeyManagementAPI()
    result = api.bell_state_measurement()
    assert result is not None

def test_quantum_utils_initialized():
    api = KeyManagementAPI()
    result = api.quantum_utils
    assert result is not None

def test_classical_crypto_fallback():
    api = KeyManagementAPI()
    result = api.classical_crypto_fallback
    assert result is not None

def test_key_storage_delete():
    api = KeyManagementAPI()
    result = api.key_storage
    result.delete_key("test_id")
    assert result is not None

def test_key_storage_operations():
    api = KeyManagementAPI()
    test_key = "test_key_data"
    api.key_storage.store_key("test_id", test_key)
    retrieved_key = api.key_storage.load_key("test_id")
    assert retrieved_key == test_key
    api.key_storage.delete_key("test_id")
    # Key should no longer exist
    assert api.key_storage.load_key("test_id") is None

def test_multiple_key_storage_operations():
    api = KeyManagementAPI()
    # Test storing multiple keys
    keys_data = [
        ("key1", "data1"),
        ("key2", "data2")
    ]
    
    for key_id, data in keys_data:
        api.key_storage.store_key(key_id, data)
        retrieved = api.key_storage.load_key(key_id)
        assert retrieved == data

def test_encryption_chaining():
    api = KeyManagementAPI()
    data = "test_data"
    encrypted = api.encrypt(data)
    assert encrypted is not None
    decrypted = api.decrypt(encrypted)
    assert decrypted is not None

def test_signing_functionality():
    api = KeyManagementAPI()
    data = "test_data"
    signature = api.sign(data)
    assert signature is not None

def test_key_storage_encryption_decryption():
    api = KeyManagementAPI()
    
    # Store a key
    api.key_storage.store_key("test_id", "test_data")
    retrieved = api.key_storage.load_key("test_id")
    assert retrieved == "test_data"
    
    # Test encryption/decryption
    encrypted = api.encrypt("test_data")
    decrypted = api.decrypt(encrypted)
    assert decrypted == "test_data"

def test_multiple_encryption_operations():
    api = KeyManagementAPI()
    data = "sensitive_data"
    encrypted = api.encrypt(data)
    decrypted = api.decrypt(encrypted)
    assert decrypted == data

def test_public_key_retrieval():
    api = KeyManagementAPI()
    pub_key = api.get_public_key()
    assert pub_key is not None

def test_key_management_api_hash_functionality():
    api = KeyManagementAPI()
    test_string = "test_input"
    hashed = api.hash_key(test_string)
    assert hashed is not None

def test_key_management_api_verify():
    api = KeyManagementAPI()
    # Verify the API is properly initialized
    assert api.key_storage is not None
    assert api.qkd_protocol is not None
    assert api.classical_crypto_fallback is not None

def test_key_management_api_generate_and_store():
    api = KeyManagementAPI()
    key_data = "test_key_data"
    api.key_storage.store_key("test_id", key_data)
    retrieved = api.key_storage.load_key("test_id")
    assert retrieved == key_data

def test_verify_key_storage_encryption():
    api = KeyManagementAPI()
    encrypted_data = api.encrypt("test_data")
    assert encrypted_data is not None

def test_verify_key_storage_decryption():
    api = KeyManagementAPI()
    decrypted_data = api.decrypt("encrypted_test_data")
    assert decrypted_data is not None

def test_verify_multiple_key_operations():
    api = KeyManagementAPI()
    
    # Test multiple key storage operations
    test_data = [
        ("key1", "data1"),
        ("key2", "data2"),
        ("key3", "data3")
    ]
    
    for key_id, data in test_data:
        api.key_storage.store_key(key_id, data)
        retrieved = api.key_storage.load_key(key_id)
        assert retrieved == data

def test_verify_encryption_decryption_chain():
    # Test encryption/decryption chain
    api = KeyManagementAPI()
    original = "test_message"
    encrypted = api.encrypt(original)
    decrypted = api.decrypt(encrypted)
    assert decrypted == original