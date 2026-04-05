import logging
from typing import Dict, Any, List, Union
from blockchain_validator.threat_detector import ThreatDetector
from blockchain_validator.transaction_validator import TransactionValidator
from blockchain_validator.address_verifier import AddressVerifier

class SecurityValidator:
    """Security validation and threat detection rules implementation"""
    
    def __init__(self):
        self.threat_detector = ThreatDetector()
        self.transaction_validator = TransactionValidator()
        self.address_verifier = AddressVerifier()
        self.logger = logging.getLogger(__name__)
    
    def detect_malicious_patterns(self, data: Union[str, Dict[str, Any]]) -> bool:
        """
        Detects known malicious patterns in blockchain data
        
        Args:
            data: The data to check for malicious patterns
            
        Returns:
            bool: True if malicious patterns detected, False otherwise
        """
        try:
            # Check for malicious patterns using threat detector
            return self.threat_detector.is_malicious_pattern(data)
        except Exception as e:
            self.logger.error(f"Error detecting malicious patterns: {e}")
            return False
    
    def validate_safety(self, data: Dict[str, Any]) -> bool:
        """
        Validates the safety of blockchain data by checking for threats and vulnerabilities
        
        Args:
            data: The data to validate for safety
            
        Returns:
            bool: True if data is safe, False otherwise
        """
        try:
            # Check for threats
            threats_detected = self.threat_detector.detect(data)
            
            # Validate transaction if it's a transaction object
            if isinstance(data, dict) and 'transaction' in data:
                transaction_valid = self.transaction_validator.validate(data['transaction'])
                return not threats_detected and transaction_valid
            
            return not threats_detected
        except Exception as e:
            self.logger.error(f"Error validating safety: {e}")
            return False
    
    def check_signatures(self, transaction: Dict[str, Any]) -> bool:
        """
        Checks the cryptographic signatures of a transaction
        
        Args:
            transaction: The transaction to validate signatures for
            
        Returns:
            bool: True if signatures are valid, False otherwise
        """
        try:
            # Validate transaction signatures
            if not transaction:
                return False
            return self.transaction_validator.validate_signature(transaction)
        except Exception as e:
            self.logger.error(f"Error checking signatures: {e}")
            return False