import logging
from typing import Dict, Any
from blockchain_validator.threat_detector import ThreatDetector
from blockchain_validator.address_verifier import AddressVerifier
from blockchain_validator.rules.security import SecurityValidator
from blockchain_validator.rules.semantics import SemanticValidator
from blockchain_validator.rules.syntax import SyntaxValidator

# Import format validators dynamically to avoid dependency issues
def get_format_validator(name):
    if name == 'ethereum':
        from blockchain_validator.formats.ethereum import EthereumFormat
        return EthereumFormat()
    elif name == 'bitcoin':
        from blockchain_validator.formats.bitcoin import BitcoinFormat
        return BitcoinFormat()
    else:
        from blockchain_validator.formats.generic import GenericFormat
        return GenericFormat()

logger = logging.getLogger(__name__)

class TransactionValidator:
    def __init__(self):
        self.threat_detector = ThreatDetector()
        self.address_verifier = AddressVerifier()
        self.security_validator = SecurityValidator()
        self.semantic_validator = SemanticValidator()
        self.syntax_validator = SyntaxValidator()
    
    def validate_format(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate the format of a transaction
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValueError: If transaction is malformed
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")
            
        if not transaction:
            raise ValueError("Transaction cannot be empty")
            
        # Validate basic structure
        from blockchain_validator.formats.generic import GenericFormat
        generic_validator = GenericFormat()
        structure_valid = generic_validator.validate_structure(transaction)
        if not structure_valid:
            return False
            
        # Validate fields
        fields_valid = self.syntax_validator.validate_fields(transaction)
        if not fields_valid:
            return False
            
        # Validate types
        types_valid = self.syntax_validator.validate_types(transaction)
        if not types_valid:
            return False
            
        # Validate blockchain-specific format
        if 'blockchain' in transaction:
            blockchain_type = transaction.get('blockchain', '').lower()
            if blockchain_type == 'ethereum':
                from blockchain_validator.formats.ethereum import EthereumFormat
                ethereum_validator = EthereumFormat()
                return ethereum_validator.validate_transaction(transaction)
            elif blockchain_type == 'bitcoin':
                from blockchain_validator.formats.bitcoin import BitcoinFormat
                bitcoin_validator = BitcoinFormat()
                return bitcoin_validator.validate_transaction(transaction)
            else:
                # For other blockchain types, validate with generic rules
                generic_validator = GenericFormat()
                return generic_validator.validate_format(transaction)
        else:
            # If no blockchain type specified, use generic validation
            generic_validator = GenericFormat()
            return generic_validator.validate_format(transaction)
    
    def validate_signature(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate the signature of a transaction
        
        Args:
            transaction: Dictionary containing transaction data with signature information
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Raises:
            ValueError: If transaction is missing required signature fields
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")
            
        # Check required signature fields
        if 'signature' not in transaction:
            raise ValueError("Transaction missing signature field")
            
        if 'public_key' not in transaction:
            raise ValueError("Transaction missing public key field")
            
        if 'hash' not in transaction and 'data' not in transaction:
            raise ValueError("Transaction missing data or hash field")
        
        # Validate signature using security validator
        return self.security_validator.check_signatures(transaction)
    
    def validate_amounts(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate the amounts in a transaction
        
        Args:
            transaction: Dictionary containing transaction data with amount information
            
        Returns:
            bool: True if amounts are valid, False otherwise
            
        Raises:
            ValueError: If transaction is missing required amount fields
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")
            
        # Check required amount fields
        if 'amount' not in transaction:
            raise ValueError("Transaction missing amount field")
            
        if 'from' not in transaction and 'to' not in transaction:
            raise ValueError("Transaction missing from/to fields")
        
        # Validate amount is numeric and positive
        amount = transaction.get('amount')
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")
            
        if amount < 0:
            raise ValueError("Amount cannot be negative")
            
        # Validate semantic meaning of amounts
        semantic_valid = self.semantic_validator.validate_values(transaction)
        if not semantic_valid:
            return False
            
        # Validate context
        context_valid = self.semantic_validator.validate_context(transaction)
        if not context_valid:
            return False
            
        return True

    def validate(self, transaction_data: Dict[str, Any]) -> bool:
        """
        Run complete transaction validation pipeline
        
        Args:
            transaction_data: Dictionary containing transaction data
            
        Returns:
            bool: True if all validations pass, False otherwise
        """
        if not isinstance(transaction_data, dict):
            raise ValueError("Transaction data must be a dictionary")
            
        try:
            # Run format validation
            format_valid = self.validate_format(transaction_data)
            if not format_valid:
                logger.error("Transaction format validation failed")
                return False
                
            # Run signature validation
            signature_valid = self.validate_signature(transaction_data)
            if not signature_valid:
                logger.error("Transaction signature validation failed")
                return False
                
            # Run amounts validation
            amounts_valid = self.validate_amounts(transaction_data)
            if not amounts_valid:
                logger.error("Transaction amounts validation failed")
                return False
                
            # Run threat detection
            threat_detected = self.threat_detector.detect(transaction_data)
            if threat_detected:
                logger.warning("Threat detected in transaction")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Transaction validation error: {str(e)}")
            return False