import pytest
from unittest.mock import patch, MagicMock
import os
from src.backend.quantum.encryption import (
    QuantumKeyDistribution, 
    QuantumEncryption, 
    get_quantum_encryption, 
    encrypt, 
    decrypt
)

def test_quantum_key_distribution_generate_key():
    qkd = QuantumKeyDistribution()
    node_id = b"test_node"
    key = qkd.generate_quantum_key(node_id)
    assert isinstance(key, bytes)
    assert len(key) == 32
    assert node_id in qkd.keys

def test_quantum_key_distribution_get_existing_key():
    qkd = QuantumKeyDistribution()
    node_id = b"test_node"
    key1 = qkd.generate_quantum_key(node_id)
    key2 = qkd.get_key(node_id)
    assert key1 == key2

def test_quantum_key_distribution_get_new_key():
    qkd = QuantumKeyDistribution()
    node_id1 = b"node1"
    node_id2 = b"node2"
    key1 = qkd.get_key(node_id1)
    key2 = qkd.get_key(node_id2)
    assert key1 != key2
    assert node_id1 in qkd.keys
    assert node_id2 in qkd.keys

def test_quantum_encryption_encrypt_decrypt():
    data = b"test data for encryption"
    node_id = b"test_node"
    
    # Test encryption
    encryptor = QuantumEncryption()
    encrypted_data = encryptor.encrypt(data, node_id)
    assert isinstance(encrypted_data, bytes)
    assert len(encrypted_data) > len(data)
    
    # Test decryption
    key = encryptor.qkd.get_key(node_id)
    decrypted_data = encryptor.decrypt(encrypted_data, key)
    assert decrypted_data == data

def test_quantum_encryption_unique_nonce():
    data = b"test data"
    encryptor1 = QuantumEncryption()
    encryptor2 = QuantumEncryption()
    
    # Reset nonce counters to ensure different nonces
    encryptor1.nonce_counter = 0
    encryptor2.nonce_counter = 0
    
    encrypted1 = encryptor1.encrypt(data)
    encrypted2 = encryptor2.encrypt(data)
    
    # First 12 bytes are the nonce
    assert encrypted1[:12] != encrypted2[:12]

def test_encrypt_decrypt_functions():
    data = b"end-to-end test data"
    node_id = b"test_node"
    
    # Encrypt
    encrypted = encrypt(data)
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > len(data)
    
    # Get key for decryption
    qe = get_quantum_encryption()
    key = qe.qkd.get_key(node_id)
    
    # Decrypt
    decrypted = decrypt(encrypted, key)
    assert decrypted == data

def test_decrypt_with_wrong_key():
    data = b"test data"
    encrypted = encrypt(data)
    
    # Try to decrypt with wrong key
    wrong_key = os.urandom(32)
    with pytest.raises(Exception):
        decrypt(encrypted, wrong_key)

def test_encrypt_empty_data():
    data = b""
    encrypted = encrypt(data)
    qe = get_quantum_encryption()
    key = qe.qkd.get_key(b'default')
    decrypted = decrypt(encrypted, key)
    assert decrypted == data

def test_encrypt_large_data():
    data = b"A" * 10000  # 10KB of data
    encrypted = encrypt(data)
    qe = get_quantum_encryption()
    key = qe.qkd.get_key(b'default')
    decrypted = decrypt(encrypted, key)
    assert decrypted == data

def test_get_quantum_encryption_singleton():
    qe1 = get_quantum_encryption()
    qe2 = get_quantum_encryption()
    assert qe1 is qe2

@patch('os.urandom')
def test_encryption_with_mocked_random(mock_urandom):
    mock_urandom.side_effect = [b'\x00' * 16, b'\x01' * 16]
    
    data = b"test data"
    encrypted = encrypt(data)
    qe = get_quantum_encryption()
    key = qe.qkd.get_key(b'default')
    decrypted = decrypt(encrypted, key)
    assert decrypted == data

def test_encryption_fails_with_none_data():
    with pytest.raises(Exception):
        encrypt(None)

def test_decryption_fails_with_invalid_data():
    with pytest.raises(Exception):
        decrypt(b"invalid data", b"some key")

def test_nonce_uniqueness_in_multiple_encryptions():
    data = b"same data"
    encryptor = QuantumEncryption()
    
    enc1 = encryptor.encrypt(data)
    enc2 = encryptor.encrypt(data)
    
    nonce1 = enc1[:12]
    nonce2 = enc2[:12]
    assert nonce1 != nonce2

def test_key_derivation_uniqueness():
    qkd = QuantumKeyDistribution()
    node1 = b"node1"
    node2 = b"node2"
    
    key1 = qkd.get_key(node1)
    key2 = qkd.get_key(node2)
    assert key1 != key2

def test_encrypt_decrypt_empty_node_id():
    data = b"test"
    qe = QuantumEncryption()
    encrypted = qe.encrypt(data, b'')
    key = qe.qkd.get_key(b'')
    decrypted = qe.decrypt(encrypted, key)
    assert decrypted == data

def test_encrypt_decrypt_consistent_key():
    data = b"consistent key test"
    qe = QuantumEncryption()
    node_id = b"consistent_node"
    
    # Encrypt twice with same node_id
    enc1 = qe.encrypt(data, node_id)
    enc2 = qe.encrypt(data, node_id)
    
    # Should use same key but different nonces
    key = qe.qkd.get_key(node_id)
    dec1 = qe.decrypt(enc1, key)
    dec2 = qe.decrypt(enc2, key)
    
    assert dec1 == dec2 == data

def test_multiple_encryptors_independent():
    data = b"independent encryptors"
    qe1 = QuantumEncryption()
    qe2 = QuantumEncryption()
    
    enc1 = qe1.encrypt(data)
    enc2 = qe2.encrypt(data)
    
    # Should have different nonces and ciphertexts
    assert enc1 != enc2
    assert enc1[:12] != enc2[:12]  # Different nonces

def test_encrypt_function_with_default_node():
    data = b"default node test"
    encrypted = encrypt(data)
    qe = get_quantum_encryption()
    key = qe.qkd.get_key(b'default')
    decrypted = decrypt(encrypted, key)
    assert decrypted == data