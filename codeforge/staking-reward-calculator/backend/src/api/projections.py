from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, root_validator
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import logging

from src.models.staking import NetworkStats
from src.services.chain_api import ChainAPIClient
from src.services.price_oracle import PriceOracle
from src.utils.calculations import project_rewards
from src.utils.validators import validate_staking_input, validate_duration
from src.database import get_db
from src.config import settings

router = APIRouter()

class ProjectionRequest(BaseModel):
    stake: float
    duration: int
    network: str
    compound_frequency: Optional[str] = "daily"
    
    @staticmethod
    def validate_stake(stake: float):
        if stake < 0:
            raise ValueError("Stake must be non-negative")
        return stake
    
    @staticmethod
    def validate_duration(duration: int):
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return duration

    @root_validator
    def validate_inputs(cls, values):
        stake = values.get("stake")
        duration = values.get("duration")
        if stake is not None:
            cls.validate_stake(stake)
        if duration is not None:
            cls.validate_duration(duration)
        return values

class ProjectionResponse(BaseModel):
    projections: Dict[str, Any]
    total_rewards: float
    apy: float
    currency: str

@router.post('/projections', response_model=ProjectionResponse)
async def calculate_projections(
    request: ProjectionRequest,
    db: Session = Depends(get_db)
):
    try:
        # Validate input
        if request.stake < 0 or not validate_staking_input({"stake": request.stake}):
            raise HTTPException(status_code=400, detail="Invalid staking input")
        
        if request.duration <= 0 or not validate_duration(request.duration):
            raise HTTPException(status_code=400, detail="Invalid duration")
        
        # Get network stats
        chain_client = ChainAPIClient()
        network_stats = await chain_client.fetch_network_stats(request.network)
        
        if not network_stats:
            raise HTTPException(status_code=400, detail="Unable to fetch network stats")
        
        # Get current price
        price_oracle = PriceOracle()
        try:
            current_price = price_oracle.get_current_price(network_stats.currency)
        except Exception as e:
            logging.error(f"Error fetching price: {str(e)}")
            current_price = 0.0  # Default to 0 if price fetching fails
        
        # Calculate projections
        projection_params = {
            "stake": request.stake,
            "duration": request.duration,
            "network": request.network,
            "compound_frequency": request.compound_frequency,
            "apy": network_stats.apy,
            "currency": network_stats.currency,
            "current_price": current_price
        }
        
        try:
            projections = project_rewards(projection_params)
        except Exception as e:
            logging.error(f"Error calculating projections: {str(e)}")
            raise HTTPException(status_code=500, detail="Error calculating projections")
        
        # Return results
        return ProjectionResponse(
            projections=projections,
            total_rewards=projections["total_rewards"],
            apy=network_stats.apy,
            currency=network_stats.currency
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        logging.error(f"Error calculating projections: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating projections")