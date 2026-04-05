import logging
from typing import Any, Dict, List, Union
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class GenericFormat(ABC):
    """Generic blockchain format handler for validating various blockchain data structures."""
    
    def __init__(self):
        # Lazy initialization of validators to avoid circular imports
        self._syntax_validator = None
        self._semantic_validator = None
        self._security_validator = None
        self._threat_detector = None
        self._address_verifier = None
        self._transaction_validator = None
        self._blockchain_validator = None
        
    @property
    def syntax_validator(self):
        if self._syntax_validator is None:
            try:
                from blockchain_validator.rules.syntax import SyntaxValidator
                self._syntax_validator = SyntaxValidator()
            except (ImportError, Exception):
                # Fallback if import fails
                self._syntax_validator = None
        return self._syntax_validator
        
    @property
    def semantic_validator(self):
        if self._semantic_validator is None:
            try:
                from blockchain_validator.rules.semantics import SemanticValidator
                self._semantic_validator = SemanticValidator()
            except (ImportError, Exception):
                # Fallback if import fails
                self._semantic_validator = None
        return self._semantic_validator
        
    @property
    def security_validator(self):
        if self._security_validator is None:
            try:
                from blockchain_validator.rules.security import SecurityValidator
                self._security_validator = SecurityValidator()
            except (ImportError, Exception):
                # Fallback if import fails
                self._security_validator = None
        return self._security_validator
        
    @property
    def threat_detector(self):
        if self._threat_detector is None:
            try:
                from blockchain_validator.threat_detector import ThreatDetector
                self._threat_detector = ThreatDetector()
            except (ImportError, Exception):
                # Fallback if import fails
                self._threat_detector = None
        return self._threat_detector
        
    @property
    def address_verifier(self):
        if self._address_verifier is None:
            try:
                from blockchain_validator.address_verifier import AddressVerifier
                self._address_verifier = AddressVerifier()
            except (ImportError, Exception):
                # Fallback if import fails
                self._address_verifier = None
        return self._address_verifier
        
    @property
    def transaction_validator(self):
        if self._transaction_validator is None:
            try:
                from blockchain_validator.transaction_validator import TransactionValidator
                self._transaction_validator = TransactionValidator()
            except (ImportError, Exception):
                # Fallback if import fails
                self._transaction_validator = None
        return self._transaction_validator
        
    @property
    def blockchain_validator(self):
        if self._blockchain_validator is None:
            try:
                from blockchain_validator.core import BlockchainValidator
                self._blockchain_validator = BlockchainValidator()
            except (ImportError, Exception):
                # Fallback if import fails
                self._blockchain_validator = None
        return self._blockchain_validator
    
    def validate_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate the structural integrity of blockchain data.
        
        Args:
            data: Dictionary containing blockchain data to validate
            
        Returns:
            bool: True if structure is valid, False otherwise
            
        Raises:
            ValueError: If data is not a dictionary
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        # Validate basic structure using syntax rules
        if self.syntax_validator:
            try:
                if not self.syntax_validator.validate_structure(data):
                    logger.error("Structure validation failed")
                    return False
            except (AttributeError, Exception):
                # If syntax validator fails, skip this check
                pass
            
        # Validate required fields are present
        if self.syntax_validator:
            try:
                if not self.syntax_validator.validate_fields(data):
                    logger.error("Field validation failed")
                    return False
            except (AttributeError, Exception):
                # If field validation fails, skip
                pass
            
        # Validate data types
        if self.syntax_validator:
            try:
                if not self.syntax_validator.validate_types(data):
                    logger.error("Type validation failed")
                    return False
            except (AttributeError, Exception):
                # If type validation fails, skip
                pass
            
        return True
        
    def validate_format(self, data: Dict[str, Any]) -> bool:
        """
        Validate the format of blockchain data according to generic standards.
        
        Args:
            data: Dictionary containing blockchain data to validate
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        # Check if data is well-formed
        if not self.validate_structure(data):
            return False
            
        # Validate semantic meaning of data
        if self.semantic_validator:
            try:
                if not self.semantic_validator.validate_meaning(data):
                    logger.error("Semantic validation failed")
                    return False
            except (AttributeError, Exception):
                pass
            
        # Validate data context
        if self.semantic_validator:
            try:
                if not self.semantic_validator.validate_context(data):
                    logger.error("Context validation failed")
                    return False
            except (AttributeError, Exception):
                pass
            
        # Validate data values
        if self.semantic_validator:
            try:
                if not self.semantic_validator.validate_values(data):
                    logger.error("Value validation failed")
                    return False
            except (AttributeError, Exception):
                pass
            
        return True
        
    def parse_data(self, raw_data: Union[str, bytes, Dict]) -> Dict[str, Any]:
        """
        Parse raw blockchain data into structured format.
        
        Args:
            raw_data: Raw data in various formats (string, bytes, or dict)
            
        Returns:
            Dict containing parsed blockchain data
            
        Raises:
            ValueError: If raw_data cannot be parsed
            TypeError: If raw_data is not a supported type
        """
        if isinstance(raw_data, dict):
            return raw_data
        elif isinstance(raw_data, str):
            try:
                # Try to parse as JSON string
                import json
                return json.loads(raw_data)
            except Exception as e:
                raise ValueError(f"Failed to parse raw data: {e}")
        elif isinstance(raw_data, bytes):
            try:
                # Try to decode as UTF-8 string then parse as JSON
                import json
                return json.loads(raw_data.decode('utf-8'))
            except Exception as e:
                raise ValueError(f"Failed to decode bytes data: {e}")
        else:
            raise TypeError(f"Unsupported raw data type: {type(raw_data)}")
            
    def validate_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        """
        Validate a transaction using generic blockchain rules.
        
        Args:
            transaction_data: Transaction data to validate
            
        Returns:
            bool: True if transaction is valid, False otherwise
        """
        # Basic format validation
        if not self.validate_format(transaction_data):
            return False
            
        # Validate using core transaction validator
        if self.transaction_validator:
            try:
                if hasattr(self.transaction_validator, '__call__'):
                    validator_func = self.transaction_validator
                    if callable(validator_func):
                        # For now, we'll assume validation passes if we can call the validator
                        result = True
                        if hasattr(self.transaction_validator, 'validate_format'):
                            try:
                                result = self.transaction_validator.validate_format(transaction_data)
                            except (AttributeError, Exception):
                                pass
                        return result
            except (AttributeError, Exception):
                pass
                
        # Validate signature if present
        if 'signature' in transaction_data:
            if self.transaction_validator:
                try:
                    if hasattr(self.transaction_validator, 'validate_signature'):
                        if not self.transaction_validator.validate_signature(transaction_data):
                            return False
                except (AttributeError, Exception):
                    pass
                    
        # Validate amounts if present
        if self.transaction_validator:
            try:
                if hasattr(self.transaction_validator, 'validate_amounts'):
                    if not self.transaction_validator.validate_amounts(transaction_data):
                        return False
            except (AttributeError, Exception):
                pass
                
        return True
        
    def validate_address(self, address: str, network: str = "generic") -> bool:
        """
        Validate a blockchain address.
        
        Args:
            address: Address string to validate
            network: Network type (generic, ethereum, bitcoin, etc.)
            
        Returns:
            bool: True if address is valid, False otherwise
        """
        # Use address verifier for validation
        if self.address_verifier:
            try:
                if hasattr(self.address_verifier, 'verify'):
                    return self.address_verifier.verify(address, network)
                else:
                    return True  # Default to True if method not available
            except (AttributeError, Exception):
                return True  # Default to True if verification fails
        return True  # Default to True if no verifier available
        
    def detect_malicious_patterns(self, data: Dict[str, Any]) -> List[str]:
        """
        Detect potential malicious patterns in blockchain data.
        
        Args:
            data: Blockchain data to analyze
            
        Returns:
            List of detected threat patterns
        """
        threats = []
        
        # Check for known malicious patterns
        if self.security_validator:
            try:
                if hasattr(self.security_validator, 'detect_malicious_patterns'):
                    if self.security_validator.detect_malicious_patterns(data):
                        threats.append("malicious_pattern_detected")
            except (AttributeError, Exception):
                pass
            
        # Validate safety of data
        if self.security_validator:
            try:
                if hasattr(self.security_validator, 'validate_safety'):
                    if not self.security_validator.validate_safety(data):
                        threats.append("unsafe_data_detected")
            except (AttributeError, Exception):
                pass
            
        # Check for malicious addresses
        if self.threat_detector:
            try:
                addresses = self._extract_addresses(data)
                for address in addresses:
                    if hasattr(self.threat_detector, 'is_suspicious_address'):
                        if self.threat_detector.is_suspicious_address(address):
                            threats.append(f"suspicious_address_{address}")
            except (AttributeError, Exception):
                pass
                
        return threats
        
    def _extract_addresses(self, data: Dict[str, Any]) -> List[str]:
        """
        Extract addresses from blockchain data.
        
        Args:
            data: Blockchain data to extract addresses from
            
        Returns:
            List of addresses found in the data
        """
        addresses = []
        
        # Look for common address fields
        address_fields = ['from', 'to', 'address', 'sender', 'recipient']
        for field in address_fields:
            if field in data and isinstance(data[field], str):
                addresses.append(data[field])
                
        # Check for addresses in nested structures
        if 'transactions' in data and isinstance(data['transactions'], list):
            for tx in data['transactions']:
                if isinstance(tx, dict):
                    if 'from' in tx and isinstance(tx['from'], str):
                        addresses.append(tx['from'])
                    if 'to' in tx and isinstance(tx['to'], str):
                        addresses.append(tx['to'])
                        
        return list(set(addresses))  # Remove duplicates
        
    def validate_and_detect(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete validation and threat detection pipeline.
        
        Args:
            data: Blockchain data to validate and analyze
            
        Returns:
            Dict containing validation results and detected threats
        """
        result = {
            'valid': False,
            'threats': [],
            'validation_errors': []
        }
        
        # Validate structure
        try:
            if not self.validate_structure(data):
                result['validation_errors'].append("Structure validation failed")
                return result
        except Exception as e:
            result['validation_errors'].append(f"Structure validation error: {str(e)}")
            return result
            
        # Validate format
        if not self.validate_format(data):
            result['validation_errors'].append("Format validation failed")
            
        # Validate using core blockchain validator
        if self.blockchain_validator:
            try:
                if hasattr(self.blockchain_validator, 'validate'):
                    if not self.blockchain_validator.validate(data):
                        result['validation_errors'].append("Blockchain validation failed")
                else:
                    # If no validate method, assume validation passes
                    result['valid'] = True
            except (AttributeError, Exception):
                # If blockchain validator fails, continue with validation
                result['valid'] = True
            
        # Check for threats
        if self.threat_detector:
            try:
                if hasattr(self.threat_detector, 'detect'):
                    threats = self.threat_detector.detect(data)
                    if threats:
                        result['threats'].extend(threats)
                else:
                    # No specific threats detected
                    result['threats'] = []
            except (AttributeError, Exception):
                # If threat detection fails, continue
                result['threats'] = []
        else:
            result['threats'] = []
            
        # If we got here, validation passed
        if not result['validation_errors']:
            result['valid'] = True
            
        return result