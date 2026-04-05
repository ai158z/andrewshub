import logging
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

class SemanticValidator:
    """
    Validates the semantic meaning and context of blockchain data.
    """
    
    def __init__(self):
        # Lazy loading to avoid circular imports
        self.transaction_validator = None
        self.threat_detector = None
        self.address_verifier = None
        self.generic_format = None
        self.ethereum_format = None
        self.bitcoin_format = None
        
    def _initialize_components(self):
        """Lazy initialization of components to avoid circular imports"""
        if self.transaction_validator is None:
            try:
                from blockchain_validator.validator import TransactionValidator
                self.transaction_validator = TransactionValidator()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("TransactionValidator could not be initialized")
                self.transaction_validator = None
        if self.threat_detector is None:
            try:
                from blockchain_validator.threat_detector import ThreatDetector
                self.threat_detector = ThreatDetector()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("ThreatDetector could not be initialized")
                self.threat_detector = None
        if self.address_verifier is None:
            try:
                from blockchain_validator.address_verifier import AddressVerifier
                self.address_verifier = AddressVerifier()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("AddressVerifier could not be initialized")
                self.address_verifier = None
        if self.generic_format is None:
            try:
                from blockchain_validator.formats.generic import GenericFormat
                self.generic_format = GenericFormat()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("GenericFormat could not be initialized")
                self.generic_format = None
        if self.ethereum_format is None:
            try:
                from blockchain_validator.formats.ethereum import EthereumFormat
                self.ethereum_format = EthereumFormat()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("EthereumFormat could not be initialized")
                self.ethereum_format = None
        if self.bitcoin_format is None:
            try:
                from blockchain_validator.formats.bitcoin import BitcoinFormat
                self.bitcoin_format = BitcoinFormat()
            except (ImportError, ModuleNotFoundError, SyntaxError):
                logger.warning("BitcoinFormat could not be initialized")
                self.bitcoin_format = None
        
    def validate_meaning(self, data: Union[Dict[str, Any], str]) -> bool:
        """
        Validates that the data has meaningful values according to blockchain standards.
        
        Args:
            data: The data to validate, either as a parsed dictionary or raw string
            
        Returns:
            bool: True if semantic meaning is valid, False otherwise
        """
        try:
            self._initialize_components()
            
            # Validate transaction structure first
            if self.generic_format is not None and hasattr(self.generic_format, 'validate_structure'):
                if not self.generic_format.validate_structure(data):
                    return False
            else:
                return False
                
            # If it's a transaction, validate amounts and fees
            if isinstance(data, dict) and 'transaction' in data:
                if self.transaction_validator is not None and hasattr(self.transaction_validator, 'validate'):
                    return self.transaction_validator.validate(data['transaction'])
                else:
                    return False
                
            return True
        except Exception as e:
            logger.error(f"Error validating meaning: {str(e)}")
            return False
    
    def validate_context(self, data: Union[Dict[str, Any], str]) -> bool:
        """
        Validates that the data is contextually appropriate for the blockchain type.
        
        Args:
            data: The data to validate
            
        Returns:
            bool: True if context is valid, False otherwise
        """
        try:
            self._initialize_components()
            
            # Check if data has blockchain type identification
            if not isinstance(data, dict):
                logger.error("Data must be a dictionary for context validation")
                return False
                
            # Determine blockchain type and validate accordingly
            blockchain_type = data.get('blockchain_type', '').lower()
            
            if blockchain_type == 'ethereum' and self.ethereum_format is not None and hasattr(self.ethereum_format, 'validate_transaction'):
                # Validate Ethereum-specific context
                return self.ethereum_format.validate_transaction(data)
            elif blockchain_type == 'bitcoin' and self.bitcoin_format is not None and hasattr(self.bitcoin_format, 'validate_transaction'):
                # Validate Bitcoin-specific context
                return self.bitcoin_format.validate_transaction(data)
            elif 'transaction' in data:
                # Generic transaction validation
                if self.transaction_validator is not None and hasattr(self.transaction_validator, 'validate'):
                    return self.transaction_validator.validate(data['transaction'])
                else:
                    return False
            else:
                # Fallback to generic structure validation
                if self.generic_format is not None and hasattr(self.generic_format, 'validate_structure'):
                    return self.generic_format.validate_structure(data)
                else:
                    return False
                
        except Exception as e:
            logger.error(f"Error validating context: {str(e)}")
            return False
    
    def validate_values(self, data: Dict[str, Any]) -> bool:
        """
        Validates the values within the data for correctness and consistency.
        
        Args:
            data: The data to validate
            
        Returns:
            bool: True if values are valid, False otherwise
        """
        try:
            self._initialize_components()
            
            if not isinstance(data, dict):
                logger.error("Data must be a dictionary for value validation")
                return False
                
            # Validate addresses if present
            if 'from_address' in data:
                if self.address_verifier is not None and hasattr(self.address_verifier, 'verify'):
                    if not self.address_verifier.verify(data['from_address'], data.get('network', 'generic')):
                        return False
                    
            if 'to_address' in data:
                if self.threat_detector is not None and hasattr(self.threat_detector, 'is_suspicious_address'):
                    if self.threat_detector.is_suspicious_address(data['to_address']):
                        return False
            
            # Check for malicious patterns
            if self.threat_detector is not None and hasattr(self.threat_detector, 'is_malicious_pattern'):
                if self.threat_detector.is_malicious_pattern(data):
                    return False
                
            # Validate amounts if present
            if 'amount' in data:
                if not self._validate_amount(data['amount']):
                    return False
                    
            # Check for required fields
            required_fields = ['from_address', 'to_address', 'amount']
            for field in required_fields:
                if field in data and not data[field]:
                    logger.warning(f"Required field {field} is missing or empty")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error validating values: {str(e)}")
            return False
    
    def _validate_amount(self, amount: Union[int, float, str]) -> bool:
        """
        Validates that an amount is a positive number and within acceptable range.
        
        Args:
            amount: The amount to validate
            
        Returns:
            bool: True if amount is valid, False otherwise
        """
        try:
            # Convert to float if it's a string
            if isinstance(amount, str):
                amount = float(amount)
                
            # Check if it's a positive number
            if amount <= 0:
                return False
                
            # In a real implementation, we might check against network limits or other constraints
            return True
        except (ValueError, TypeError):
            return False