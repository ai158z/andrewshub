import base58
import hashlib
import logging
from typing import Any, Dict, Union

# Try to import bech32 module - do this at module level to avoid repeated imports
try:
    import bech32
    BECH32_AVAILABLE = True
except ImportError:
    bech32 = None
    BECH32_AVAILABLE = False


class BitcoinFormat:
    """Handler for Bitcoin transaction and address validation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate a Bitcoin transaction structure and content.
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Validate transaction structure
            if not isinstance(transaction, dict):
                self.logger.error("Transaction must be a dictionary")
                return False
                
            required_fields = ['version', 'inputs', 'outputs']  # locktime is optional in some cases
            for field in required_fields:
                if field not in transaction:
                    self.logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate inputs and outputs
            if not self._validate_inputs(transaction.get('inputs', [])):
                self.logger.error("Invalid transaction inputs")
                return False
                
            if not self._validate_outputs(transaction.get('outputs', [])):
                self.logger.error("Invalid transaction outputs")
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Error validating transaction: {str(e)}")
            return False
    
    def _validate_inputs(self, inputs: list) -> bool:
        """Validate transaction inputs."""
        if not isinstance(inputs, list):
            return False
            
        for input_data in inputs:
            if not isinstance(input_data, dict):
                return False
            if 'txid' not in input_data or 'vout' not in input_data:
                return False
            # Additional validation could be added here
        return True
    
    def _validate_outputs(self, outputs: list) -> bool:
        """Validate transaction outputs."""
        if not isinstance(outputs, list):
            return False
            
        for output in outputs:
            if not isinstance(output, dict):
                return False
            if 'value' not in output or 'script_pubkey' not in output:
                return False
        return True
    
    def validate_address(self, address: str) -> bool:
        """
        Validate a Bitcoin address format.
        
        Args:
            address: Bitcoin address string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check if it's a valid string
            if not isinstance(address, str) or not address:
                return False
            
            # Try to decode as base58 address (P2PKH, P2SH)
            try:
                # Verify base58 checksum
                decoded = base58.b58decode(address)
                if len(decoded) < 4:  # Minimum for checksum validation
                    return False
                    
                # Verify checksum
                checksum = decoded[-4:]
                data = decoded[:-4]
                hash_result = hashlib.sha256(hashlib.sha256(data).digest()).digest()
                if hash_result[:4] != checksum:
                    return False
                    
                # Check address type by length
                if len(decoded) not in [25, 21]:  # P2PKH (25) or P2SH (21)
                    return False
                    
                return True
            except Exception:
                # If base58 fails, try bech32 (SegWit) if available
                if BECH32_AVAILABLE and address.startswith(('bc1', 'tb1')):
                    try:
                        hrp, data = bech32.bech32_decode(address)
                        if hrp is None or data is None:
                            return False
                        return True
                    except Exception:
                        return False
                else:
                    return False
        except Exception as e:
            self.logger.error(f"Error validating address: {str(e)}")
            return False
    
    def parse_transaction(self, raw_transaction: Union[str, Dict]) -> Dict:
        """
        Parse raw Bitcoin transaction data into a structured format.
        
        Args:
            raw_transaction: Raw transaction data in hex or dict format
            
        Returns:
            Dict: Parsed transaction data
        """
        # Import here to avoid circular dependencies
        try:
            from bitcoinlib.transactions import Transaction
        except ImportError:
            self.logger.error("bitcoinlib not available")
            return {}
            
        try:
            if isinstance(raw_transaction, str):
                # Parse from hex string
                tx = Transaction().from_raw(raw_transaction)
                return {
                    'version': tx.version,
                    'inputs': [
                        {
                            'txid': inp.previous_txid.hex(),
                            'vout': inp.output_n,
                            'script_sig': inp.unlocking_script.hex() if inp.unlocking_script else '',
                            'sequence': inp.sequence
                        }
                        for inp in tx.inputs
                    ],
                    'outputs': [
                        {
                            'value': out.value,
                            'script_pubkey': out.locking_script.hex()
                        }
                        for out in tx.outputs
                    ],
                    'locktime': tx.locktime
                }
            elif isinstance(raw_transaction, dict):
                # Already parsed, validate structure
                return raw_transaction
            else:
                raise ValueError("Invalid raw transaction format")
        except Exception as e:
            self.logger.error(f"Error parsing transaction: {str(e)}")
            return {}