import logging
from typing import Dict, Any
try:
    from blockchain_validator.formats.generic import GenericFormat
    from blockchain_validator.formats.ethereum import EthereumFormat
    from blockchain_validator.formats.bitcoin import BitcoinFormat
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    # Mock the classes if dependencies aren't available
    GenericFormat = object
    EthereumFormat = object
    BitcoinFormat = object
    DEPENDENCIES_AVAILABLE = False

logger = logging.getLogger(__name__)

class SyntaxValidator:
    def __init__(self):
        self.generic_format = GenericFormat() if DEPENDENCIES_AVAILABLE else None
        self.ethereum_format = EthereumFormat() if DEPENDENCIES_AVAILABLE else None
        self.bitcoin_format = BitcoinFormat() if DEPENDENCIES_AVAILABLE else None

    def validate_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate the basic structure of blockchain data.
        
        Args:
            data: Dictionary containing blockchain data to validate
            
        Returns:
            bool: True if structure is valid, False otherwise
        """
        if not isinstance(data, dict):
            logger.error("Data must be a dictionary")
            return False

        required_fields = ['type', 'data']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        data_content = data.get('data', {})
        if not isinstance(data_content, dict):
            logger.error("Data content must be a dictionary")
            return False

        return True

    def validate_fields(self, data: Dict[str, Any]) -> bool:
        """
        Validate that all required fields are present in the data.
        
        Args:
            data: Dictionary containing blockchain data to validate
            
        Returns:
            bool: True if all required fields are present, False otherwise
        """
        if not isinstance(data, dict):
            logger.error("Data must be a dictionary")
            return False

        required_fields = ['type', 'data']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        data_type = data.get('type')
        if not data_type:
            logger.error("Missing data type")
            return False

        data_content = data.get('data', {})
        if not isinstance(data_content, dict):
            logger.error("Data content must be a dictionary")
            return False

        # For field validation, we don't need to check the actual format validation
        # This is handled in validate_types
        return True

    def validate_types(self, data: Dict[str, Any]) -> bool:
        """
        Validate the data types of fields in the data.
        
        Args:
            data: Dictionary containing blockchain data to validate
            
        Returns:
            bool: True if all data types are valid, False otherwise
        """
        if not isinstance(data, dict):
            logger.error("Data must be a dictionary")
            return False

        data_type = data.get('type')
        if not data_type:
            logger.error("Missing data type")
            return False

        if data_type == "ethereum_transaction":
            if DEPENDENCIES_AVAILABLE and self.ethereum_format:
                return self.ethereum_format.validate_transaction(data.get('data', {}))
            else:
                # If dependencies aren't available, do basic validation
                return isinstance(data.get('data'), dict)
        elif data_type == "bitcoin_transaction":
            if DEPENDENCIES_AVAILABLE and self.bitcoin_format:
                return self.bitcoin_format.validate_transaction(data.get('data', {}))
            else:
                # If dependencies aren't available, do basic validation
                return isinstance(data.get('data'), dict)
        elif data_type == "generic":
            if DEPENDENCIES_AVAILABLE and self.generic_format:
                return self.generic_format.validate_structure(data.get('data', {}))
            else:
                # If dependencies aren't available, do basic validation
                return isinstance(data.get('data'), dict)
        else:
            logger.error(f"Unsupported data type: {data_type}")
            return False

        return True