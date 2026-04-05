import logging
from typing import Dict, Any, List, Union
from dataclasses import dataclass
import re

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ThreatDetectionResult:
    is_threat: bool = False
    threat_type: str = None
    confidence: float = 0.0
    details: Dict[str, Any] = None

class ThreatDetector:
    """Blockchain transaction threat detector."""
    
    def __init__(self):
        self._initialize_threat_patterns()
    
    def _initialize_threat_patterns(self):
        """Initialize known malicious patterns and addresses."""
        self.malicious_patterns = [
            'selfdestruct',
            'delegatecall',
            'DROP',
            'contract'
        ]
        
        # Known malicious addresses
        self.known_malicious_addresses = {
            '0x0000000000000000000000000000000000000000',
            '0x0000000000000000000000000000000000000001'
        }
        
        # Suspicious address patterns
        self.suspicious_address_patterns = [
            r'^0x0+$',  # Null address pattern
            r'^0x[0]{30,}',  # Excessive zeros
            r'[13][a-km-zA-HJ-NP-Z0-9]{25,34}$'  # Bitcoin addresses
        ]
    
    def detect(self, transaction_data: Dict[str, Any]) -> ThreatDetectionResult:
        """Main threat detection method that analyzes transaction data for security threats."""
        try:
            # Validate transaction structure first
            if not self._validate_transaction_structure(transaction_data):
                return ThreatDetectionResult(
                    is_threat=True,
                    threat_type="invalid_structure",
                    confidence=0.9,
                    details={"reason": "Invalid transaction structure"}
                )
            
            # Check for malicious patterns
            if self.is_malicious_pattern(transaction_data):
                return ThreatDetectionResult(
                    is_threat=True,
                    threat_type="malicious_pattern",
                    confidence=0.8,
                    details={"reason": "Malicious pattern detected in transaction data"}
                )
            
            # Check for suspicious addresses
            addresses_to_check = [
                transaction_data.get('from', ''),
                transaction_data.get('to', '')
            ]
            
            for address in addresses_to_check:
                if self.is_suspicious_address(address):
                    return ThreatDetectionResult(
                        is_threat=True,
                        threat_type="suspicious_address",
                        confidence=0.7,
                        details={"suspicious_address": address}
                    )
            
            # No threats found
            return ThreatDetectionResult(
                is_threat=False,
                threat_type="none",
                confidence=1.0,
                details={}
            )
        except Exception as e:
            logger.error(f"Error during threat detection: {str(e)}")
            return ThreatDetectionResult(
                is_threat=False,
                threat_type="error",
                confidence=0.0,
                details={"error": str(e)}
            )
    
    def _validate_transaction_structure(self, data: Dict[str, Any]) -> bool:
        """Validate basic transaction structure."""
        required_fields = ['from', 'to', 'value']
        return all(field in data for field in required_fields)
    
    def is_suspicious_address(self, address: str) -> bool:
        """Check if an address is suspicious based on known patterns."""
        if address in self.known_malicious_addresses:
            return True
            
        for pattern in self.suspicious_address_patterns:
            if re.match(pattern, address):
                return True
        return False
    
    def is_malicious_pattern(self, data: Dict[str, Any]) -> bool:
        """Check if transaction data contains known malicious patterns."""
        # Check for dust transactions
        if data.get('value', 1) == 0:
            return True
            
        # Check for null address
        if data.get('to') == '0x0000000000000000000000000000000000000000':
            return True
            
        # Check data field for destructive opcodes
        data_field = data.get('data', '')
        for pattern in self.malicious_patterns:
            if pattern in data_field:
                return True
                
        return False
    
    def scan_for_anomalies(self, transactions: List[Dict[str, Any]]) -> List[ThreatDetectionResult]:
        """Scan multiple transactions for anomalies."""
        results = []
        for transaction in transactions:
            result = self.detect(transaction)
            results.append(result)
        return results
    
    def get_threat_statistics(self, transactions: List[Dict[str, Any]]) -> Dict[str, Union[int, float]]:
        """Get statistics about detected threats."""
        if not transactions:
            return {
                'total_transactions': 0,
                'threat_count': 0,
                'threat_percentage': 0.0
            }
            
        threat_count = 0
        for transaction in transactions:
            result = self.detect(transaction)
            if result.is_threat:
                threat_count += 1
                
        total = len(transactions)
        threat_percentage = (threat_count / total * 100) if total > 0 else 0
        
        return {
            'total_transactions': total,
            'threat_count': threat_count,
            'threat_percentage': threat_percentage
        }