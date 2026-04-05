import logging
from typing import Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.src.models.staking import NetworkStats
from backend.src.services.chain_api import ChainAPIClient
from backend.src.services.price_oracle import PriceOracle
from backend.src.utils.calculations import calculate_rewards, project_rewards
from backend.src.utils.validators import validate_staking_input, validate_duration
from backend.src.database import get_db

logger = logging.getLogger(__name__)

class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class CalculationRequest(BaseModel):
    stake: float
    duration: int
    network: str
    compound: bool = False

class CalculationResponse(BaseModel):
    daily_rewards: float
    total_rewards: float
    usd_value: float
    projected_rewards: Dict[str, Any]

async def calculate_staking_rewards(request: Dict, db: Session = None):
    """
    Calculate staking rewards based on user input
    """
    try:
        # Validate input
        if not validate_staking_input(request):
            raise HTTPException(400, "Invalid staking input data")
        
        if not validate_duration(request["duration"]):
            raise HTTPException(400, "Invalid staking duration")
        
        # Fetch network stats
        chain_client = ChainAPIClient()
        network_stats = await chain_client.fetch_network_stats(request["network"])
        if not network_stats:
            raise HTTPException(status_code=400, detail="Failed to fetch network statistics")
        
        # Calculate rewards
        daily_rewards = calculate_rewards(request["stake"], network_stats.apr, 1)
        total_rewards = calculate_rewards(request["stake"], network_stats.apr, request["duration"])
        
        # Get current token price
        price_oracle = PriceOracle()
        token_price = price_oracle.get_current_price(network_stats.token_symbol)
        
        usd_value = total_rewards * token_price if token_price else 0.0
        
        # Project rewards over time
        projection_params = {
            "stake": request["stake"],
            "apr": network_stats.apr,
            "duration": request["duration"],
            "compound": request["compound"]
        }
        projected_rewards_data = project_rewards(projection_params)
        
        return CalculationResponse(
            daily_rewards=daily_rewards,
            total_rewards=total_rewards,
            usd_value=usd_value,
            projected_rewards=projected_rewards_data
        )
    except Exception as e:
        logger.error(f"Error calculating staking rewards: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating staking rewards")

def get_calculator_config():
    """
    Return calculator configuration
    """
    return {
        "min_stake": 1.0,
        "max_stake": 1000000.0,
        "min_duration": 1,
        "max_duration": 365,
        "supported_networks": ["ethereum", "solana", "polygon", "cosmos"]
    }