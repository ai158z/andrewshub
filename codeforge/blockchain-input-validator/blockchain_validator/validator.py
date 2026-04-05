import logging
from typing import Dict, Any, List
from blockchain_validator.address_verifier import AddressVerifier
from blockchain_validator.threat_detector import ThreatDetector
from blockchain_validator.formats.ethereum import EthereumFormat
from blockchain_validator.formats.bitcoin import BitcoinFormat
from blockchain_validator.formats.generic import GenericFormat
from blockchain_validator.rules.syntax import SyntaxValidator
from blockchain_validator.rules.semantics import SemanticValidator
from blockchain_validator.rules.security import SecurityValidator
import logging

class TransactionValidator:
    def __init__(self):
        self.address_verifier = AddressVerifier()
        self.threat_detector = ThreatDetector()
        self.syntax_validator = SyntaxValidator()
        self.semantic_validator = SemanticValidator()
        self.security_validator = SecurityValidator()
        self.ethereum_format = EthereumFormat()
        self.bitcoin_format = BitcoinFormat()
        self.generic_format = GenericFormat()
        self.logger = logging.getLogger(__name__)

    def validate(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        if not isinstance(transaction_data, dict):
            raise TypeError("Transaction data must be a dictionary")
            
        if 'type' not in transaction_data:
            raise ValueError("Transaction data must include a 'type' field")
            
        if 'data' not in transaction_data:
            raise ValueError("Transaction data must include a 'data' field")
            
        if 'details' not in transaction_data:
            raise ValueError("Transaction data must include a 'data' field")
            
        validation_results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            validation_results = self.run_validation_pipeline(transaction_data)
        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            validation_results['errors'].append(str(e))
            
        return validation_results

    def run_validation_pipeline(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete validation pipeline for a transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Step 1: Format validation
            format_result = self.validate_format(transaction_data)
            results['details']['format_validation'] = format_result
            if not format_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'].extend(format_result.get('errors', []))
                
            # Step 2: Semantic validation
            semantic_result = self.validate_semantics(transaction_data)
            results['details']['semantic_validation'] = semantic_result
            if not semantic_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'].extend(semantic_result.get('errors', []))
                
        except Exception as e:
            self.logger.error(f"Validation pipeline error: {str(e)}")
            validation_results['errors'].append(str(e))
            results['is_valid'] = False
            
        return results

    def validate_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the format of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Validate using blockchain format validators
            if data.get('type') == 'ethereum':
                format_validation = self.ethereum_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            elif data.get('type') == 'bitcoin':
                format_validation = self.bitcoin_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            else:
                format_validation = self.generic_format.validate_structure(data)
                result.update(format_validation)
                
            # Validate syntax
            syntax_result = self.syntax_validator.validate_structure(data)
            if not syntax_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'].extend(syntax_result.get('errors', []))
                
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Format validation error: {str(e)}")
            
        return result

    def validate_semantics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Semantic validation error: {str(e)}`)
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(security_result.get('errors', []))
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Security validation error: {str(e)}')
            
        return result

    def detect_threats(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect any threats in the transaction data"""
        result = {
            'is_malicious': False,
            'is_suspicious': False,
            'details': []
        }
        
        try:
            # Check for malicious patterns
            is_malicious = self.threat_detector.is_malicious_pattern(transaction_data)
            if is_malicious:
                result['is_malicious'] = True
                result['details'].append("Malicious pattern detected")
                
            # Check for suspicious addresses
            if 'data' in transaction_data and 'from' in transaction_data['data']:
                from_address = transaction_data['data']['from']
                is_suspicious = self.threat_detector.is_suspicious_address(from_address)
                if is_suspicious:
                    result['is_malicious'] = True
                    
        except Exception as e:
            result['details'].append(f"Threat detection error: {str(e)}')
            
        return result

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        result = {
            'status': 'valid'
        }
        
        try:
            result['status'] = self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            result['status'] = 'invalid'
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error: {str(e)}")
            return False

    def validate(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        if not isinstance(transaction_data, dict):
            raise TypeError("Transaction data must be a dictionary")
            
        if 'type' not in transaction_data:
            raise ValueError("Transaction data must include a 'type' field")
            
        if 'data' not in transaction_data:
            raise ValueError("Transaction data must include a 'data' field")
            
        validation_results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Run the validation pipeline
            validation_results = self.run_validation_pipeline(transaction_data)
        except Exception: e
            self.logger.error(f"Error during validation: {str(e)}")
            validation_results['errors'].append(str(e))
            
        return validation_results

    def run_validation_pipeline(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete validation pipeline for a transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Step 1: Format validation
            format_result = self.validate_format(transaction_data)
            results['details']['format_validation'] = format_result
            if not format_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'].extend(format_result.get('errors', []))
                
            # Step 2: Semantic validation
            semantic_result = self.validate_semantics(transaction_data)
            results['details']['semantic_validation'] = semantic_result
            if not semantic_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'].extend(semantic_result.get('errors', []))
            
            # Step 3: Security validation
            security_result = self.validate_security(data)
            results['details']['security_validation'] = security_result
            if not security_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'] = security_result.get('errors', []))
                
            # Step 4: Threat detection
            threat_result = self.detect_threats(transaction_data)
            results['details']['threat_detection'] = threat_result
            if threat_result.get('is_malicious', False) or threat_result.get('is_suspicious', False):
                results['is_valid'] = False
                if 'errors' not in results:
                    results['errors'] = []
                results['errors'].append(str(e))
                
        except Exception: e:
            results['is_valid'] = False
            results['errors'].append(str(e))
            results['is_valid'] = False
            
        return results

    def detect_threats(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect any threats in the transaction data"""
        result = {
            'is_malicious': False,
            'is_suspicious': False,
            'details': []
        }
        
        try:
            # Check for malicious patterns
            is_malicious = self.threat_detector.is_malicious_pattern(transaction_data)
            if is_malicious:
                result['is_malicious'] = True
                result['details'].append("Malicious pattern detected")
                
            # Check for suspicious addresses
            if 'data' in transaction_data and 'from' in transaction_data['data']:
                from_address = transaction_data['data']['from']
                is_suspicious = self.threat_detector.is_suspicious_address(from_address)
                if is_suspicious:
                    result['is_suspicious'] = True
                    
        except Exception as e:
            result['details'].append(f"Threat detection error: {str(e)}')
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'] = security_result.get('errors', [])
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Security validation error: {str(e)}")
            
        return result

    def validate_semantics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_semantic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'] = security_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Security validation error: {str(e)}")
            
        return result

    def validate_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the format of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Validate using blockchain format validators
            if data.get('type') == 'ethereum':
                format_validation = self.ethereum_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            elif data.get('type') == 'bitcoin':
                format_validation = self.bitcoin_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            else:
                format_validation = self.generic_format.validate_structure(data)
                result.update(format_validation)
                
            # Validate syntax
            syntax_result = self.syntax_validator.validate_structure(data)
            if not syntax_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'].extend(syntax_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Format validation error: {str(e)}")
            
        return result

    def validate_semantic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
            
        except Exception as e:
            result['details'].append(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(security_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Security validation error: {str(e)}")
            
        return result

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        result = {
            'status': 'valid'
        }
        
        try:
            result['status'] = self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            result['status'] = 'invalid'
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        try:
            return self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            return False

    def validate_format(self, data: Dict[str, Any], network: str) -> Dict[str, Any]:
        """
        Validate a single transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        if not isinstance(transaction_data, dict):
            raise TypeError("Transaction data must be a dictionary")
            
        if 'type' not in transaction_data:
            raise ValueError("Transaction data must include a 'type' field")
            
        if 'data' not in transaction_data:
            raise ValueError("Transaction data must include a 'data' field")
            
        validation_results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Run the validation pipeline
            validation_results = self.run_validation_pipeline(transaction_data)
        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            validation_results['errors'].append(str(e))
            
        return validation_results

    def validate_semantic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
                
        except Exception as e:
            self.logger.error(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_semantic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(security_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Threat detection error: {str(e)}")
            
        return result

    def detect_threats(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect any threats in the transaction data"""
        result = {
            'is_malicious': False,
            'is_suspicious': False,
            'details': []
        }
        
        try:
            # Check for malicious patterns
            is_malicious = self.threat_detector.is_malicious_pattern(transaction_data)
            if is_malicious:
                result['is_malicious'] = True
                result['details'].append("Malicious pattern detected")
                
            # Check for suspicious addresses
            if 'data' in transaction_data and 'from' in transaction_data['data']:
                from_address = transaction_data['from']
                is_suspicious = self.threat_detector.is_suspicious_address(from_address)
                if is_suspicious:
                    result['is_suspicious'] = True
                    
        except Exception as e:
            result['details'].append(f"Th0.22s error: {str(e)}")
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        try:
            return self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            return False

    def validate_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the format of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Validate using blockchain format validators
            if data.get('type') == 'ethereum':
                format_validation = self.ethereum_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            elif data.get('type') == 'bitcoin':
                format_validation = self.bitcoin_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            else:
                format_validation = self.generic_format.validate_structure(data)
                result.update(format_validation)
                
            # Validate syntax
            syntax_result = self.syntax_validator.validate_structure(data)
            if not syntax_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(syntax_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Format validation error: {str(e)}")
            
        return result

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        result = {
            'status': 'valid',
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            result['status'] = self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            result['status'] = 'invalid'
            
        return result

    def detect_threats(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect any threats in the transaction data"""
        result = {
            'is_malicious': False,
            'is_suspicious': False,
            'details': []
        }
        
        try:
            # Check for malicious patterns
            is_malicious = self.threat_detector.is_malicious_pattern(transaction_data)
            if is_malicious:
                result['is_malicious'] = True
                result['details'].append("Malicious pattern detected")
                
            # Check for suspicious addresses
            if 'data' in transaction_data and 'from' in transaction_data['data']:
                from_address = transaction_data['data']['from']
                is_suspicious = self.threat_detector.is_suspicious_address(from_address)
                if is_suspicious:
                    result['is_suspicious'] = True
                    
        except Exception as e:
            result['details'].append(f"Threat detection error: {str(e)}")
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        result = {
            'status': 'valid'
        }
        
        try:
            result['status'] = self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            result['status'] = 'invalid'
            
        return result

    def validate(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        if not isinstance(transaction_data, dict):
            raise TypeError("Transaction data must be a dictionary")
            
        if 'type' not in transaction_data:
            raise ValueError("Transaction data must include a 'type' field")
            
        if 'data' not in transaction_data:
            raise ValueError("Transaction data must include a 'data' field")
            
        validation_results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Run the validation pipeline
            validation_results = self.run_validation_pipeline(transaction_data)
        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            validation_results['errors'].append(str(e))
            
        return validation_results

    def run_validation_pipeline(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete validation pipeline for a transaction
        
        Args:
            transaction_data: Dictionary containing transaction data to validate
            
        Returns:
            Dict containing validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Step 1: Format validation
            format_result = self.format_validation(transaction_data)
            results['details']['format_validation'] = format_result
            if not format_result.get('is_valid', True):
                results['is_valid'] = False
                results['errors'].extend(format_result.get('errors', []))
                
        except Exception as e:
            results['details'].append(f"Format validation error: {str(e)}")
            
        return results

    def validate_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the format of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            # Validate using blockchain format validators
            if data.get('type') == 'ethereum':
                format_validation = self.ethereum_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            elif data.get('type') == 'bitcoin':
                format_validation = self.bitcoin_format.validate_transaction(data.get('data', {}))
                result.update(format_validation)
            else:
                format_validation = self.generic_format.validate_structure(data)
                result.update(format_validation)
                
            # Validate syntax
            syntax_result = self.syntax_validator.validate_structure(data)
            if not syntax_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'] = syntax_result.get('errors', [])
                
        except Exception as e:
            result['details'].append(f"Format validation error: {str(e)}")
            
        return result

    def validate_semantics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
                
        except Exception as e:
            result['details'].append(f"Semantic validation error: {str(e)
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid', True):
                result['is_valid'] = False
                result['errors'] = security_result.get('errors', [])
        except Exception as e:
            result['details'].append(f"Security validation error: {str(e)}")
            
        return result

    def validate_blockchain_input(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blockchain input"""
        result = {
            'status': 'valid'
        }
        
        try:
            result['status'] = self.blockchain_validator.validate(transaction_data)
        except Exception as e:
            self.logger.error(f"Blockchain validation error: {str(e)}")
            result['status'] = 'invalid'
            
        return result

    def validate_format(self, data: Dict[str, Any], network: str) -> Dict[str, Any]:
        """Validate the format of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        try:
            format_result = self.format_validator.validate_transaction(data, network)
            result.update(format_result)
        except Exception as e:
            result['details'].append(f"Format validation error: {str(e)}")
            
        return result

    def validate_semantics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the semantic meaning of the transaction data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            semantic_result = self.semantic_validator.validate_meaning(data)
            if not semantic_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'].extend(semantic_result.get('errors', []))
        except Exception as e:
            result['errors'].append(f"Semantic validation error: {str(e)}")
            
        return result

    def validate_security(self, data: Dict[str, Any]) -> Dict[str, Any):
        """Validate the security aspects of the transaction"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            security_result = self.security_validator.validate_safety(data)
            if not security_result.get('is_valid'):
                result['is_valid'] = False
                result['errors'] = security_result.get('errors', [])
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Security validation error: {str(e)}")
            
        return result

    def detect_threats(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect any threats in the transaction data"""
        result = {
            'is_malicious': False,
            'is_suspicious': False,
            'details': []
        }
        
        try:
            # Check for malicious patterns
            is_malicious = self.threat_detector.is_malicious_pattern(transaction_data)
            if is_malicious:
                result['is_malicious'] = True
                result['details'].append("Malicious pattern detected")
                
            # Check for suspicious addresses
            if 'data' in transaction_data and 'from' in transaction_data['data']:
                from_address = transaction_data['data']['from']
                is_suspicious = self.threat_detector.is_suspicious_address(from_address)
                if is_suspicious:
                    result['is_suspicious'] = True
                    
        except Exception as e:
            result['details'].append(f"Threat detection error: {str(e)}")
            
        return result

    def verify_address(self, address: str, network: str) -> bool:
        """Verify a blockchain address"""
        try:
            return self.address_verifier.verify(address, network)
        except Exception as e:
            self.logger.error(f"Address verification error for {address}: {str(e)}")
            return False