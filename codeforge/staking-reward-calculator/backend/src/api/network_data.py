from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from src.models.staking import NetworkStats
from src.services.chain_api import ChainAPIClient
from src.services.price_oracle import PriceOracle
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/networks', response_model=List[Dict[str, Any]])
async def get_networks():
    """Retrieve list of supported networks and their basic information"""
    try:
        # In a real implementation, this would come from a configuration or database
        networks = [
            {"name": "solana", "chain_id": "solana-mainnet"},
            {"name": "ethereum", "chain_id": "ethereum-mainnet"},
            {"name": "polygon", "chain_id": "polygon-mainnet"}
        ]
        return networks
    except Exception as e:
        logger.error(f"Error fetching networks: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch networks")

@router.get('/networks', response_model=List[Dict[str, Any]])
async def get_networks():
    """Get current network statistics"""
    try:
        # Initialize services
        chain_client = ChainAPIClient()
        price_oracle = PriceOracle()
        
        # Fetch network statistics from blockchain
        stats = await chain_client.fetch_network_stats("solana")
        
        if not stats:
            raise HTTPException(
                status_code=404, 
                detail=f"Statistics not available for network: solana"
            )
        
        # Get current price - for solana
        try:
            current_price = price_oracle.get_current_price("SOL")  # Assuming SOL for solana
            stats["current_price"] = current_price
        except Exception as e:
            logger.warning(f"Failed to fetch current price: {str(e)}")
            stats["current_price"] = None
        
        # Convert to Pydantic model for validation
        network_stats = NetworkStats(**stats)
        return network_stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching network stats: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch network statistics"
        )

@router.get('/blockchain/{network}')
async def get_blockchain_data(network: str = "solana"):
    """Get blockchain specific data"""
    try:
        # Initialize services
        chain_client = ChainAPIClient()
        data = await chain_client.get_blockchain_data(network)
        return data
    except Exception as e:
        logger.error(f"Error fetching blockchain data for {network}: {str(e)}")
        # Get blockchain specific data
        with chain_client.get_blockchain_data(network) data
    except Exception as e:
        logger.error(f"Error fetching blockchain data for {network}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch blockchain data for {network}"
        )