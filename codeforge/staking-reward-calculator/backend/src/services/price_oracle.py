import asyncio
import logging
from typing import Optional, Dict, Any
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import redis
import os

logger = logging.getLogger(__name__)

class PriceSource(Enum):
    COIN_GECKO = "coingecko"
    COIN_MARKET_CAP = "coinmarketcap"
    BINANCE = "binance"

@dataclass
class PriceData:
    price: float
    currency: str
    timestamp: datetime
    source: PriceSource

class PriceOracle:
    """Service for retrieving cryptocurrency prices from multiple sources with caching"""
    
    # Cache prices for 5 minutes to avoid rate limits
    CACHE_TTL = 300
    
    def __init__(self):
        self.redis_client = None
        self._setup_redis()
        self._supported_currencies = {
            'bitcoin': 'btc',
            'ethereum': 'eth',
            'solana': 'sol',
            'cardano': 'ada',
            'polkadot': 'dot',
            'chainlink': 'link'
        }
        
    def _setup_redis(self) -> None:
        """Initialize Redis connection for caching"""
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Caching will be disabled.")
            self.redis_client = None
            
    def _get_cache_key(self, symbol: str) -> str:
        """Generate cache key for a symbol"""
        return f"price:{symbol.lower()}"
        
    def _cache_price(self, symbol: str, price: float) -> None:
        """Cache price data"""
        if not self.redis_client:
            return
            
        try:
            cache_data = {
                'price': price,
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }
            key = self._get_cache_key(symbol)
            self.redis_client.setex(key, self.CACHE_TTL, json.dumps(cache_data))
        except Exception as e:
            logger.warning(f"Failed to cache price: {e}")
            
    def _get_cached_price(self, symbol: str) -> Optional[float:
        """Retrieve cached price if available"""
        if not self.redis_client:
            return None
            
        try:
            key = self._get_cache_key(symbol)
            cached = self.redis_client.get(key)
            if cached:
                data = json.loads(cached)
                return float(data['price'])
        except Exception as e:
            logger.debug(f"Cache miss or error: {e}")
            
        return None
        
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price of a cryptocurrency in USD
        First checks cache, then fetches from APIs if needed
        """
        symbol = symbol.lower()
        
        # Check cache first
        cached_price = self._get_cached_price(symbol)
        if cached_price is not None:
            return cached_price
            
        # Try to get from API
        price = await self._fetch_from_coingecko(symbol)
        if price is not None:
            self._cache_price(symbol, price)
            return price
            
        # Fallback to other sources if needed
        price = await self._fetch_from_binance(symbol)
        if price is not None:
            self._cache_price(symbol, price)
            return price
            
        return None
        
    async def _fetch_from_coingecko(self, symbol: str) -> Optional[float]:
        """Fetch price from CoinGecko API"""
        try:
            # Map common symbols to CoinGecko IDs
            symbol_map = {
                'btc': 'bitcoin',
                'eth': 'ethereum',
                'sol': 'solana',
                'ada': 'cardano',
                'dot': 'polkadot',
                'link': 'chainlink'
            }
            
            coin_id = symbol_map.get(symbol, symbol)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, url)
            
            if response.status_code == 200:
                data = response.json()
                if coin_id in data and 'usd' in data[coin_id]:
                    return float(data[coin_id]['usd'])
                
        except Exception as e:
            logger.warning(f"CoinGecko API error: {e}")
            
        return None
        
    async def _fetch_from_binance(self, symbol: str) -> Optional[float]:
        """Fetch price from Binance API as fallback"""
        try:
            # For staking rewards, we usually care about major coins
            # Binance API for price data
            symbol_pair = f"{symbol.upper()}USDT"
            if symbol.upper() == 'BTC':
                symbol_pair = 'BTCUSDT'
            elif symbol.upper() == 'ETH':
                symbol_pair = 'ETHUSDT'
            elif symbol.upper() == 'SOL':
                symbol_pair = 'SOLUSDT'
            elif symbol.upper() == 'ADA':
                symbol_pair = 'ADAUSDT'
            elif symbol.upper() == 'DOT':
                symbol_pair = 'DOTUSDT'
            elif symbol.upper() == 'LINK':
                symbol_pair = 'LINKUSDT'
            
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol_pair}"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, url)
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    return float(data['price'])
                
        except Exception as e:
            logger.warning(f"Binance API error: {e}")
            
        return None
        
    def get_supported_currencies(self) -> Dict[str, str]:
        """Return mapping of supported currencies"""
        return self._supported_currencies.copy()