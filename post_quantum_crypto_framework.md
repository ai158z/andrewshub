# Post-Quantum Cryptography Framework for Blockchain Integration

Based on NIST FIPS 205 standards and arXiv research findings (https://arxiv.org/abs/2603.19340v4, https://arxiv.org/abs/1912.00916v4)

## Features
- ML-DSA-44 simulation for blockchain transaction signing
- ML-KEM-512 simulation for key exchange
- Python implementation with test examples

## Implementation Details
- `MLDSA44` class: Simulates key generation and signing operations
- `MLKEM512` class: Simulates key exchange with encapsulation/decapsulation
- Uses standard Python libraries (hashlib, json, datetime)

## Usage Example
```python
from post_quantum_crypto_test import MLDSA44, MLKEM512

# Test ML-DSA-44
mldsa = MLDSA44()
keys = mldsa.generate_keys()
print('ML-DSA-44 Keys:', keys)

signature = mldsa.sign('Blockchain transaction data')
print('Signature:', signature)

# Test ML-KEM-512
mlkem = MLKEM512()
kem_keys = mlkem.generate_keys()
print('ML-KEM-512 Keys:', kem_keys)

encapsulated = mlkem.encapsulate_key(kem_keys['public_key'])
print('Encapsulation:', encapsulated)

decapsulated = mlkem.decapsulate_key(encapsulated['ciphertext'])
print('Decapsulation:', decapsulated)
```

## Research Basis
- [ML-DSA-44 and ML-KEM-512 performance on resource-constrained devices](https://arxiv.org/abs/2603.19340v4)
- [Energy requirements for post-quantum cryptography in IoT](https://arxiv.org/abs/1912.00916v4)
- [NIST FIPS 205: Automated Cryptographic Key Agreement Protocols](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)