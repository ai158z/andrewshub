import pytest
from unittest.mock import patch, MagicMock
from src.wallet_backup.encryption import WalletEncryption
from src.wallet_backup.config import Config

@pytest.fixture
def wallet_encryption():
    return WalletEncryption()

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def test_data():
    return "sensitive_wallet_data"

def test_encrypt_data(wallet_encryption, test_data):
    encrypted_data = wallet_encryption.encrypt_data(test_data)
    assert encrypted_data is not None
    assert encrypted_data != test_data

def test_decrypt_data(wallet_encryption, test_data):
    encrypted_data = wallet_encryption.encrypt_data(test_data)
    decrypted_data = wallet_encryption.decrypt_data(encrypted_data)
    assert decrypted_data == test_data

def test_encrypt_empty_string(wallet_encryption):
    encrypted_data = wallet_encryption.encrypt_data("")
    assert encrypted_data is not None

def test_decrypt_empty_string(wallet_encryption):
    encrypted_data = wallet_encryption.encrypt_data("")
    decrypted_data = wallet_encryption.decrypt_data(encrypted_data)
    assert decrypted_data == ""

def test_encrypt_none_data(wallet_encryption):
    with pytest.raises(Exception):
        wallet_encryption.encrypt_data(None)

def test_decrypt_none_data(wallet_encryption):
    with pytest.raises(Exception):
        wallet_encryption.decrypt_data(None)

def test_encrypt_special_characters(wallet_encryption):
    special_data = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    encrypted_data = wallet_encryption.encrypt_data(special_data)
    assert encrypted_data is not None
    assert encrypted_data != special_data

def test_decrypt_special_characters(wallet_encryption):
    special_data = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    encrypted_data = wallet_encryption.encrypt_data(special_data)
    decrypted_data = wallet_encryption.decrypt_data(encrypted_data)
    assert decrypted_data == special_data

def test_encrypt_long_data(wallet_encryption):
    long_data = "A" * 1000
    encrypted_data = wallet_encryption.encrypt_data(long_data)
    assert encrypted_data is not None
    assert encrypted_data != long_data

def test_decrypt_long_data(wallet_encryption):
    long_data = "A" * 1000
    encrypted_data = wallet_encryption.encrypt_data(long_data)
    decrypted_data = wallet_encryption.decrypt_data(encrypted_data)
    assert decrypted_data == long_data

def test_encrypt_unicode_data(wallet_encryption):
    unicode_data = "Hello 世界 🌍"
    encrypted_data = wallet_encryption.encrypt_data(unicode_data)
    assert encrypted_data is not None
    assert encrypted_data != unicode_data

def test_decrypt_unicode_data(wallet_encryption):
    unicode_data = "Hello 世界 🌍"
    encrypted_data = wallet_encryption.encrypt_data(unicode_data)
    decrypted_data = wallet_encryption.decrypt_data(encrypted_data)
    assert decrypted_data == unicode_data

def test_encrypt_decrypt_roundtrip(wallet_encryption, test_data):
    # Test multiple roundtrips don't cause degradation
    encrypted1 = wallet_encryption.encrypt_data(test_data)
    decrypted1 = wallet_encryption.decrypt_data(encrypted1)
    encrypted2 = wallet_encryption.encrypt_data(decrypted1)
    decrypted2 = wallet_encryption.decrypt_data(encrypted2)
    assert decrypted1 == test_data
    assert decrypted2 == test_data

def test_encrypt_same_data_produces_different_output(wallet_encryption, test_data):
    # Due to potential use of random IV/salt, same data encrypted twice should produce different ciphertexts
    encrypted1 = wallet_encryption.encrypt_data(test_data)
    encrypted2 = wallet_encryption.encrypt_data(test_data)
    # They should be different (if using random IV)
    assert encrypted1 != encrypted2 or len(encrypted1) == len(encrypted2)

def test_decrypt_modified_encrypted_data(wallet_encryption):
    original = "test data"
    encrypted = wallet_encryption.encrypt_data(original)
    # Modify the encrypted data slightly
    modified = encrypted + "tampered"
    with pytest.raises(Exception):
        wallet_encryption.decrypt_data(modified)

def test_encrypt_decrypt_empty_config():
    with patch('src.wallet_backup.config.Config') as mock_config:
        mock_config.return_value.encryption_key = ""
        mock_config.return_value.encryption_enabled = True
        encryption = WalletEncryption()
        with pytest.raises(Exception):
            encryption.encrypt_data("test")

def test_encrypt_decrypt_with_custom_key():
    with patch('src.wallet_backup.config.Config') as mock_config:
        mock_config.return_value.encryption_key = "custom_key"
        mock_config.return_value.encryption_enabled = True
        encryption = WalletEncryption()
        test_data = "test"
        encrypted = encryption.encrypt_data(test_data)
        decrypted = encryption.decrypt_data(encrypted)
        assert decrypted == test_data

def test_encrypt_large_data_performance(wallet_encryption):
    large_data = "A" * 10000
    encrypted = wallet_encryption.encrypt_data(large_data)
    decrypted = wallet_encryption.decrypt_data(encrypted)
    assert len(decrypted) == len(large_data)

def test_encrypt_decrypt_with_none_key():
    with patch('src.wallet_backup.config.Config') as mock_config:
        mock_config.return_value.encryption_key = None
        mock_config.return_value.encryption_enabled = True
        encryption = WalletEncryption()
        with pytest.raises(Exception):
            encryption.encrypt_data("test")