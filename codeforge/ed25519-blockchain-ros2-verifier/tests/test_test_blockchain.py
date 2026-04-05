import pytest
from unittest.mock import Mock, patch
from ed25519_verifier.blockchain import BlockchainVerifier
from ed25519_verifier.core import Ed25519Verifier
from ed25519_verifier.utils import encode_signature
from ed25519_verifier.exceptions import Ed25519VerificationError
import json

@pytest.fixture
def blockchain_verifier():
    return BlockchainVerifier()

@pytest.fixture
def ed25519_verifier():
    return Ed25519Verifier()

@pytest.fixture
def test_keypair():
    from cryptography.hazmat.primitives.asymmetric import ed25519
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def create_transaction():
    return {
        "from": "sender_address",
        "to": "recipient_address",
        "amount": 100,
        "timestamp": 1234567890,
        "nonce": 1
    }

def test_valid_signature_verification(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is True

def test_invalid_signature_verification(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    # Tamper with transaction
    transaction["amount"] = 999
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is False

def test_invalid_public_key_format(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, "invalid_key", signature_b58
    )
    assert result is False

def test_valid_base58_format(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    valid_signature = encode_signature(public_key.public_bytes_raw())
    result = blockchain_verifier.validate_blockchain_format(valid_signature)
    assert result is True

def test_invalid_base58_format(blockchain_verifier):
    result = blockchain_verifier.validate_blockchain_format("invalid_base64==")
    assert result is False

def test_valid_transaction_structure(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    signature_b58 = encode_signature(signature)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is True

def test_invalid_transaction_structure(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    signature_b58 = encode_signature(signature)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    
    invalid_transaction = {"invalid": "structure"}
    result = blockchain_verifier.verify_transaction_signature(
        invalid_transaction, public_key_b58, signature_b58
    )
    assert result is False

def test_empty_transaction_verification(blockchain_verifier):
    result = blockchain_verifier.verify_transaction_signature(
        {}, "valid_key", "valid_sig"
    )
    assert result is False

def test_none_transaction_verification(blockchain_verifier):
    result = blockchain_verifier.verify_transaction_signature(
        None, "valid_key", "valid_sig"
    )
    assert result is False

def test_transaction_missing_required_fields(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = {"incomplete": "transaction"}
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is False

def test_transaction_with_extra_fields(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = {
        "from": "sender",
        "to": "recipient",
        "amount": 100,
        "extra_field": "extra"
    }
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is True

def test_signature_verification_with_different_data(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction1 = create_transaction()
    transaction2 = create_transaction()
    transaction2["amount"] = 200
    
    message1 = json.dumps(transaction1, sort_keys=True).encode('utf-8')
    message2 = json.dumps(transaction2, sort_keys=True).encode('utf-8')
    
    signature1 = private_key.sign(message1)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature1)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction2, public_key_b58, signature_b58
    )
    assert result is False

def test_valid_signature_invalid_key(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, "invalid_key_format", signature_b58
    )
    assert result is False

def test_transaction_serialization_consistency(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    message = json.dumps(transaction, sort_keys=True).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    # Verify same transaction twice
    result1 = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    result2 = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result1 == result2

def test_base58_encoding_decoding(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    public_key_bytes = public_key.public_bytes_raw()
    encoded = encode_signature(public_key_bytes)
    result = blockchain_verifier.validate_blockchain_format(encoded)
    assert result is True

def test_signature_verification_edge_case_empty_strings(blockchain_verifier):
    result = blockchain_verifier.verify_transaction_signature(
        {}, "", ""
    )
    assert result is False

def test_signature_verification_none_values(blockchain_verifier):
    result = blockchain_verifier.verify_transaction_signature(
        None, None, None
    )
    assert result is False

def test_signature_verification_empty_signature(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, ""
    )
    assert result is False

def test_signature_verification_malformed_transaction(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = "not_a_dict"
    message = str(transaction).encode('utf-8')
    signature = private_key.sign(message)
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    signature_b58 = encode_signature(signature)
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, signature_b58
    )
    assert result is False

def test_signature_verification_valid_key_invalid_sig(blockchain_verifier, test_keypair):
    private_key, public_key = test_keypair
    transaction = create_transaction()
    public_key_b58 = encode_signature(public_key.public_bytes_raw())
    
    result = blockchain_verifier.verify_transaction_signature(
        transaction, public_key_b58, "invalid_signature"
    )
    assert result is False