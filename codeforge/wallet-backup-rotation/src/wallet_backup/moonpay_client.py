import requests
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MoonPayClient:
    """Client for interacting with MoonPay wallet APIs to fetch wallet data for backup."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.moonpay.com"):
        """
        Initialize the MoonPay client.
        
        Args:
            api_key: The MoonPay API key
            base_url: The base URL for MoonPay API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"ApiKey {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_wallet_data(self, wallet_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch data for a specific wallet from MoonPay.
        
        Args:
            wallet_id: The ID of the wallet to retrieve
            
        Returns:
            Dictionary containing wallet data or None if not found
        """
        try:
            url = f"{self.base_url}/v1/wallets/{wallet_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch wallet {wallet_id}: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when fetching wallet {wallet_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error when fetching wallet {wallet_id}: {str(e)}")
            return None
    
    def list_wallets(self) -> Optional[List[Dict[str, Any]]]:
        """
        List all wallets from MoonPay.
        
        Returns:
            List of wallets or None if request fails
        """
        try:
            url = f"{self.base_url}/v1/wallets"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to list wallets: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when listing wallets: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error when listing wallets: {str(e)}")
            return None