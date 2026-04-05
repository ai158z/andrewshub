import requests
import logging
from typing import Dict, Any
from decimal import Decimal, InvalidOperation
import unittest.mock
from typing import Dict, Any, Union, List
from decimal import Decimal, InvalidOperation
import logging
from typing import Dict, Any, Union, List
from decimal import Decimal, InvalidOperation

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

_converter = CurrencyConverter()

def convert_to_fiat(amount: float, crypto: str, fiat: str = 'USD') -> float:
    """Public API function for currency conversion."""
    global _converter
    return _converter.convert_to_fiat(amount, crypto, fiat)

class CurrencyConverter:
    """Handles conversion of cryptocurrency amounts to fiat currency equivalents."""
    
    def __init__(self):
        self._cache: Dict[str, float] = {}
        self._base_url = "https://api.coingecko.com/api/v3/simple/price"

    def convert_to_fiat(self, amount: float, crypto: str, fiat: str = 'USD') -> float:
        """
        Convert cryptocurrency amount to fiat currency equivalent.

        Args:
            amount: The amount of cryptocurrency to convert
            crypto: The cryptocurrency symbol (e.g., 'BTC', 'ETH')
            fiat: Target fiat currency (default: 'USD')
        """
        # Input validation
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a non-negative number")
        if not isinstance(crypto, str) or not crypto:
            raise ValueError("Crypto must be a non-empty string")
        if not isinstance(fiat, str) or not fiat:
            raise ValueError("Fiat must be a non-empty string")
        
        # Normalize inputs
        crypto = crypto.upper()
        fiat = fiat.upper()
        
        try:
            # Check if we have cached rate
            cache_key = f"{crypto}_{fiat}"
            if cache_key in self._cache:
                rate = self._cache[cache_key]
                return float(amount) * rate

            # Fetch current price data
            params = {
                'ids': self._get_coingecko_id(crypto),
                'vs_currencies': fiat.lower()
            }
            response = requests.get(self._base_url, params=params, timeout=10)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to fetch price data: {response.status_code}")
            
            data = response.json()
            crypto_id = self._get_coingecko_id(crypto)
            if crypto_id not in data:
                raise RuntimeError(f"Failed to get price for {crypto}")
            if fiat.lower() not in data[crypto_id]:
                raise RuntimeError(f"Failed to get {fiat} price for {crypto}")
            
            rate = data[crypto_id][fiat.lower()]
            self._cache[cache_key] = rate
            return float(amount) * rate
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during conversion: {str(e)}")
            raise RuntimeError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Error in currency conversion: {str(e)}")
            raise RuntimeError(f"Conversion error: {str(e)}")

    def _get_coingecko_id(self, crypto: str) -> str:
        """Map common crypto symbols to CoinGecko IDs."""
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'DOT': 'polkadot',
            'ATOM': 'cosmos',
            'ADA': 'cardano',
            'XRP': 'ripple',
            'DOGE': 'dogecoin',
            'AVAX': 'avalanche-2',
            'MATIC': 'matic-network',
            'BNB': 'binancecoin',
            'LTC': 'litecoin'
        }
        return mapping.get(crypto, crypto.lower())