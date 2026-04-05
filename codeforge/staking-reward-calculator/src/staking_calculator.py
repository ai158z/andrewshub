import logging
from typing import Dict, Any
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate
from src.validator import validate_stake_amount
from src.utils import format_currency

logger = logging.getLogger(__name__)

def calculate_rewards(stake_data: StakeData, reward_rate: RewardRate) -> Dict[str, Any]:
    """
    Calculate staking rewards based on stake data and reward rate.
    
    Args:
        stake_data: StakeData object containing stake information
        reward_rate: RewardRate object containing reward rate information
        
    Returns:
        Dictionary containing calculated rewards and related information
    """
    try:
        # Validate stake amount
        if not validate_stake_amount(stake_data.amount):
            raise ValueError(f"Invalid stake amount: {stake_data.amount}")
        
        # Calculate rewards
        # Simple interest calculation: reward = principal * rate * time
        # Assuming annual rate and time in days
        time_fraction = stake_data.stake_duration_days / 365.0
        estimated_reward = stake_data.amount * reward_rate.annual_rate * time_fraction
        
        # Apply compounding if specified
        if reward_rate.is_compounded:
            # Compound interest formula: A = P(1 + r/n)^(nt)
            # For simplicity, assuming daily compounding (n=365)
            compounded_amount = stake_data.amount * (
                (1 + reward_rate.annual_rate / 365) ** stake_data.stake_duration_days
            )
            total_amount = compounded_amount
            estimated_reward = total_amount - stake_data.amount
        else:
            total_amount = stake_data.amount + estimated_reward
            
        result = {
            "stake_amount": stake_data.amount,
            "stake_duration_days": stake_data.stake_duration_days,
            "reward_rate": reward_rate.annual_rate,
            "is_compounded": reward_rate.is_compounded,
            "estimated_reward": estimated_reward,
            "total_amount_after_reward": total_amount,
            "formatted_stake_amount": format_currency(stake_data.amount),
            "formatted_estimated_reward": format_currency(estimated_reward),
            "formatted_total_amount": format_currency(total_amount),
        }
        
        logger.info(f"Calculated rewards for stake amount {stake_data.amount}")
        return result
        
    except Exception as e:
        logger.error(f"Error calculating rewards: {str(e)}")
        raise e