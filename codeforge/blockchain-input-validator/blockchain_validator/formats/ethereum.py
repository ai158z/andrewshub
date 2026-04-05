import re
import logging
from typing import Dict, Any, Union
import rlp
from eth_utils import is_hex, is_0x_prefixed, to_checksum_address

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            required_fields = [
                'from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 
                'chainId', 'r', 's', 'v'
            ]
            
            for field in required_fields:
                if field not in transaction:
                    logger.error(f"Missing required field: {field}")
                    return False
                    
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from']):
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to']):
                logger.error("Invalid 'to' address")
                return False
            
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate signature fields
            if not isinstance(transaction['r'], int) or transaction['r'] < 0:
                logger.error("Invalid signature r value")
                return False
                
            if not isinstance(transaction['s'], int) or transaction['s'] < 0:
                logger.error("Invalid signature s value")
                return False
                
            if not isinstance(transaction['v'], int) or transaction['v'] < 0:
                logger.error("Invalid signature v value")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error validating transaction: {str(e)}")
            return False
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            logger.error("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            logger.error("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                logger.error("Invalid checksum address")
                return False
                
        return True

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            required_fields = [
                'from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 
                'chainId', 'r', 's', 'v'
            ]
            
            for field in required_fields:
                if field not in transaction:
                    logger.error(f"Missing required field: {field}")
                    return False
                    
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from']):
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to']):
                logger.error("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate signature fields
            if not isinstance(transaction['r'], int) or transaction['r'] < 0:
                logger.error("Invalid signature r value")
                return False
                
            if not isinstance(transaction['s'], int) or transaction['s'] < 0:
                logger.error("Invalid signature s value")
                return False
                
            if not isinstance(transaction['v'], int) or transaction['v'] < 0:
                logger.error("Invalid signature v value")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID")
                return False
                
            return True
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            required_fields = [
                'from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 
                'chainId', 'r', 's', 'v'
            ]
            
            for field in required_fields:
                if field not in transaction:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating transaction: {str(e)}")
            return False

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            logger.error("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            logger.error("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                logger.error("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
        # Define the transaction structure
        transaction_structure = List([
                BigEndianInt(),  # nonce
                BigEndianInt(),  # gas_price
                BigEndianInt(),  # gas_limit
                Binary(),         # to address
                BigEndianInt(),  # value
                Binary(),         # data
                BigEndianInt(),  # v
                BigEndianInt(),  # r
                BigEndian0x_prefix = '0x' if isinstance(raw_transaction, str) and len(raw_transaction) > 2 else '0x' in raw_transaction:
                Binary(),         # s
                BigEndianInt(),  # v
                BigEndianInt(),  # r
                BigEndianInt(),  # s
            ])
            
            # Decode the RLP data
            decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }
            
        except Exception as e:
            logger.error(f"Error parsing transaction: {str(e)}")
            return False

    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
        # Define the transaction structure
        transaction_structure = List([
                BigEndianInt(),  # nonce
                BigEndianInt(),  # gas_price
                BigEndianInt(),  # gas_limit
                Binary(),         # to address
                BigEndianInt(),  # value
                Binary(),         # data
                BigEndianInt(),  # v
                BigEndianInt(),  # r
                BigEndianInt(),  # s
            ])
            
        # Decode the RLP data
        decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }
            
        except Exception as e:
            logger.error(f"Error parsing transaction: {str(e)}")
            return False

    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
        # Define the transaction structure
        transaction_structure = List([
                BigEndianInt(),  # nonce
                BigEndianInt(),  # gas_price
                BigEndianInt(),  # gas_limit
                Binary(),         # to address
                BigEndianInt(),  # value
                Binary(),         # data
                BigEndianInt(),  # v
                BigEndianInt(),  # r
                BigEndianInt(),  # s
            ])
            
        # Decode the RLP data
        decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }

import re
import logging
from typing import Dict, Any, Union
from eth_utils import is_hex, is_0x_prefixed, to_checksum_address

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            required_fields = [
                'from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 
                'chainId', 'r', 's', 'v'
            ]
            
            for field in required_fields:
                if field not in transaction:
                    logger.error(f"Missing required field: {field}")
                    return False
                    
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from']):
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to']):
                logger.error("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID
            return True
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            logger.error("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            logger.error("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                logger.error("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_pref to '0x' prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
            # Define the transaction structure
            transaction_structure = List([
                BigEndianInt(),  # nonce
                BigEndianInt(),  # gas_price
                BigEndianInt(),  # gas_limit
                Binary(),         # to address
                BigEndianInt(),  # value
                Binary(),         # data
                BigEndianInt(),  # v
                BigEndianInt(),  # r
                BigEndianInt(),  # s
            ])
            
            # Decode the RLP data
            decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }

import re
import logging
from typing import Dict, Any, Union
from eth_utils import is_hex, is_0x_prefixed, to_checksum_address

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from'])):
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to}]):
                logger.error("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate signature fields
            if not isinstance(transaction['r'], int) or transaction['r'] < 0:
                logger.error("Invalid signature r value")
                return False
                
            if not isinstance(transaction['s'], int) or transaction['s'] < 0:
                logger.error("Invalid signature s value")
                return False
                
            if not isinstance(transaction['v'], int) or transaction['v'] < 0:
                logger.error("Invalid signature v value")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID")
                return False
                
            return True
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            logger.error("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            logger.error("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                logger.error("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
            # Define the transaction structure
            transaction_structure = List([
                    BigEndianInt(),  # nonce
                    BigEndianInt(),  # gas_price
                    BigEndianInt(),  # gas_limit
                    Binary(),         # to address
                    BigEndianInt(),  # value
                    Binary(),         # data
                    BigEndianInt(),  # v
                    BigEndianInt(),  # r
                    BigEndianInt(),  # s
                ])
            
            # Decode the RLP data
            decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }
            
        except Exception as e:
            logger.error(f"Error parsing transaction: {str(e)}")
            return False
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }

import re
import logging
from typing import Dict, Any, Union
from eth_utils import is_hex, is_0x_prefixed, to_checksum_address

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary
            return False
                
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from}'] as e:
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to}']):
                logger.error("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID")
                return False
                
            return True
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            logger.error("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            logger.error("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                logger.error("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, str):
                transaction_bytes = raw_transaction
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import BigEndianInt, Binary
            
            transaction_structure = [
                    BigEndianInt(),  # nonce
                    BigEndianInt(),  # gas_price
                    BigEndianInt(),  # gas_limit
                    Binary(),         # to address
                    BigEndianInt(),  # value
                    Binary(),         # data
                    BigEndianInt(),  # v
                    BigEndianInt(),  # r
                    BigEndianInt(),  # s
                ]
            
            # Decode the RLP data
            decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }
            
        except Exception as e:
            logger.error(f"Error parsing transaction: {str(e)}")
            return False

    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                logger.error("Transaction must be a dictionary")
                return False
                
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from}']):
                logger.error("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to}']):
                logger.error("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                logger.error("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                logger.error("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                logger.error("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                logger.error("Invalid nonce")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                logger.error("Invalid chain ID")
                return False
                
            return True
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            print("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            print("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                print("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from r to '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,                 # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35 else None,
                'r': decoded[7],
                's': decoded[8],
                'v': decoded[6]
            }
            
        except Exception as e:
            print(f"Error parsing transaction: {str(e)}")
            return False

import re
import logging
from typing import Dict, Any, Union
from eth_utils import is_hex, is_0x_prefixed, to_checksum_address

logger = logging.getLogger(__name__)

class EthereumFormat:
    """Ethereum transaction and address format handler"""
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate Ethereum transaction format
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not isinstance(transaction, dict):
                print("Transaction must be a dictionary")
                return False
                
            required_fields = [
                'from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 
                'chainId', 'r', 's', 'v'
            ]
            
            for field in required_fields:
                if field not in transaction:
                    print(f"Missing required field: {field}")
                    return False
                    
            # Validate address formats
            if not EthereumFormat.validate_address(transaction['from}']):
                print("Invalid 'from' address")
                return False
                
            if not EthereumFormat.validate_address(transaction['to}']):
                print("Invalid 'to' address")
                return False
                
            # Validate numeric fields
            if not isinstance(transaction['value'], (int, float)) or transaction['value'] < 0:
                print("Invalid transaction value")
                return False
                
            if not isinstance(transaction['gas'], int) or transaction['gas'] <= 0:
                print("Invalid gas value")
                return False
                
            if not isinstance(transaction['gasPrice'], (int, float)) or transaction['gasPrice'] < 0:
                print("Invalid gas price")
                return False
                
            if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
                print("Invalid nonce")
                return False
                
            # Validate chain ID
            if not isinstance(transaction['chainId'], int) or transaction['chainId'] <= 0:
                print("Invalid chain ID")
                return False
                
            return True
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Ethereum address format
        
        Args:
            address: Ethereum address string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(address, str):
            print("Address must be a string")
            return False
            
        # Check if it's a valid Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            print("Invalid Ethereum address format")
            return False
            
        # Validate checksum address if it has uppercase letters
        if any(c.isupper() for c in address[2:]):
            try:
                to_checksum_address(address)
            except Exception:
                print("Invalid checksum address")
                return False
                
        return True
    
    @staticmethod
    def parse_transaction(raw_transaction: Union[str, bytes]) -> Dict[str, Any]:
        """
        Parse raw Ethereum transaction data
        
        Args:
            raw_transaction: Raw transaction data as hex string or bytes
            
        Returns:
            Dict containing parsed transaction data
        """
        try:
            if isinstance(raw_transaction, str):
                if is_0x_prefixed(raw_transaction):
                    raw_transaction = raw_transaction[2:]
                    
                # Convert hex to bytes
                transaction_bytes = bytes.fromhex(raw_transaction)
            elif isinstance(raw_transaction, bytes):
                transaction_bytes = raw_transaction
            else:
                raise TypeError("Raw transaction must be string or bytes")
                
            # Parse RLP encoded transaction
            from rlp import decode
            from rlp.sedes import List, BigEndianInt, Binary
            
            # Define the transaction structure
            transaction_structure = List([
                    BigEndianInt(),  # nonce
                    BigEndianInt(),  # gas_price
                    BigEndianInt(),  # gas_limit
                    Binary(),         # to address
                    BigEndianInt(),  # value
                    Binary(),         # data
                    BigEndianInt(),  # v
                    BigEndianInt(),  # r
                    BigEndianInt(),  # s
                ])
            
            # Decode the RLP data
            decoded = decode(transaction_bytes, transaction_structure)
            
        return {
                'nonce': decoded[0],
                'gasPrice': decoded[1],
                'gas': decoded[2],
                'to': '0x' + decoded[3].hex() if len(decoded[3]) == 20 else None,
                'from': None,  # From address needs to be recovered from signature
                'value': decoded[4],
                'data': '0x' + decoded[5].hex() if decoded[5] else '0x',
                'chainId': (decoded[6] - 35) // 2 if decoded[6] >= 35