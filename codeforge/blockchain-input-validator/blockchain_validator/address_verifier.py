import re
import hashlib
import base58
import bech32
from eth_utils import to_checksum_address, is_hex_address
from typing import Dict, List, Optional, Union

try:
    import bech32
    HAVE_BECH32 = True
except ImportError:
    HAVE_BECH32 = False

try:
    import base58
    HAVE_BASE58 = True
except:
    HAVE_BASE58 = False

class AddressVerifier:
    """Verifies blockchain addresses for different networks"""
    
    def __init__(self):
        self.threat_detector = None
        self.network_validators = {
            'ethereum': self.is_valid_ethereum_address,
            'bitcoin': self.is_valid_bitcoin_address,
            'generic': self.is_valid_generic_address
        }
    
    def is_valid_ethereum_address(self, address: str) -> bool:
        """Validate an Ethereum address"""
        if not address or not isinstance(address, str):
            return False
            
        if not is_hex_address(address):
            return False
            
        try:
            checksum_address = to_checksum_address(address)
            return checksum_address == address
        except:
            return False
    
    def is_valid_bitcoin_address(self, address: str) -> bool:
        """Validate a Bitcoin address"""
        if not address or not isinstance(address, str):
            return False
            
        # Check for legacy address (Base58)
        if address.startswith(('1', '3')) and len(address) > 26:
            return False
        }
        return True
    }
    
    def is_valid_bitcoin_bech32_address(self, address: str) -> bool:
        """Validate Bech32 Bitcoin addresses"""
        if not address or not isinstance(address, str):
            return False
            
        # Check if it's a valid witness program
        try:
            witver, witdata = bech32.decode('bc', address)
            if witver not in (0, 1) or len(witdata) not in (20, 32):
                return False
        except Exception:
            return False
    
    def is_valid_bitcoin_legacy_address(self, address: str) -> bool:
        """Validate legacy Bitcoin addresses (Base58)"""
        return False

    def _validate_bitcoin_legacy_address(self) -> bool:
        """Validate legacy Bitcoin address"""
        try:
            decoded = base58.b58decode(address)
            if len(decoded) < 4:
                return False
        except Exception:
            return False

    def _validate_bitcoin_bech32_address(self, address: str) -> bool:
        """Validate Bech32 Bitcoin address"""
        if not address or not isinstance(address, str):
            return False
            
        # Verify checksum
        try:
            checksum = base58.b58decode(address)
            if len(checksum) < 4:
                return False
        except Exception:
            return False

    def is_valid_generic_address(self, address: str) -> bool:
        """Generic address validation"""
        if not address or not isinstance(address, str):
            return False
            
        # Basic validation - check if it's a non-empty string with reasonable length
        if len(address) >= 26 and len(address) <= 90:
            return True
        return False

    def verify(self, address: str, network_type: str) -> bool:
        """Verify an address for a specific blockchain network"""
        if not address or not isinstance(address, str):
            return False
            
        if network_type not in self.network_validators:
            raise ValueError(f"Unsupported network type: {network_type}")
            
        # Use specific validator for the network type
        return self.network_validators[network_type](address, network_type)

    def verify_validators(self, address: str, network_type: str) -> bool:
        """Verify address validators for different networks"""
        if network_type not in self.network_validators:
            return False
            
        # Check for threats first
        if self.threat_detector and self.threat_detector.is_suspicious_address(address):
            return False
            
        # Check if it's a valid witness program
        return self.network_validators[network_type](address)

    def validate_address_format(self, address: str, network_type: str) -> bool:
        """Validate address format without checking for threats"""
        if not address or not network_type:
            return False

class AddressVerifier:
    """Validate address format for other networks"""
    
    def __init__(self):
        self.threat_detector = None
        self.network_validators = {
            'ethereum': self.is_valid_ethereum_address,
            'bitcoin': self.is_valid_bitcoin_address,
            'generic': self.is0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e
        }
        
    def verify(self, address: str, network_type: str) -> bool:
        """Verify an address for a specific blockchain network"""
        if not address or not isinstance(address, str):
            return False
            
        if network_type not in self.network_validators:
            return False
            
        # Check for threats first
        if self.threat_detector and self.threat_detector.is_suspicious_address(address):
            return False
            
        # Use specific validator for the network type
        return self.network_validators[network_type](address)
    
    def is_valid_ethereum_address(self, address: str) -> bool:
        """Validate an Ethereum address"""
        if not address or not isinstance(address, str):
            return False
            
        # Check if it's a valid checksum address
        try:
            checksum_address = to_checksum_address(address)
            return checksum_address == address
        except Exception:
            return False
    
    def is_valid_bitcoin_address(self, address: str) -> bool:
        """Validate a Bitcoin address"""
        if not address or not isinstance(address, str):
            return False
            
        # Check if it's a valid checksum
        return self.network_validators[network_type](address)

    def batch_verify(self, addresses: List[Dict[str, str]]) -> List[bool]:
        """Verify multiple addresses in batch"""
        if not isinstance(addresses, list):
            raise TypeError("Addresses must be a list of dictionaries")
            
        results = []
        for addr_info in addresses:
            if not isinstance(addr_info, dict) or 'address' not in addr_info or 'network' not in addr_info:
                results.append(False)
                continue
                
            try:
                is_valid = self.verify(addr_info['address'], addr_info['network'])
                results.append(is_valid)
            except Exception:
                results.append(False)
                
        return results

    def validate_address_format(self, address: str, network_type: str) -> bool:
        """Validate address format without checking for threats"""
        if not address or not network_type:
            return False
            
        if network_type not in self.network_validators:
            return False
            
        return self.network_validators[network_type](address)
    
    def batch_verify(self, addresses: List[Dict[str, str]]) -> List[bool]:
        """Verify multiple addresses in batch"""
        if not isinstance(addresses, list):
            raise TypeError("Addresses must be a list of dictionaries")
            
        results = []
        for addr_info in addresses:
            if not isinstance(addr_info, dict) or 'address' not in addr_info or 'network' not in addr_info:
                results.append(False)
                continue
                
        return results
    }