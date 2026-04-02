import logging
from typing import Dict
from src.models import StakingResult, StakingConfig
from src.validators import validate_inputs
from src.utils import calculate_compound_interest, calculate_penalty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StakingCalculator:
    def __init__(self, apy: float, compound_frequency: int = 1, penalty_rate: float = 0.0):
        """
        Initialize the StakingCalculator with staking configuration.
        
        Args:
            apy: Annual percentage yield as a decimal (e.g., 0.08 for 8%)
            compound_frequency: How many times per year interest is compounded (default: 1)
            penalty_rate: Penalty rate as a decimal for early withdrawal (default: 0%)
        """
        self.config = StakingConfig(apy, compound_frequency, penalty_rate)
        logger.info("StakingCalculator initialized with APY: %f, compound frequency: %d, penalty rate: %f", 
                   apy, compound_frequency, penalty_rate)

    def calculate_rewards(self, stake_amount: float, duration_days: int, lockup_days: int = 0) -> Dict:
        """
        Calculate staking rewards with optional compounding and early withdrawal penalty.
        
        Args:
            stake_amount: The amount being staked
            duration_days: The duration of staking in days
            lockup_days: The lockup period in days (for early withdrawal penalty calculation)
            
        Returns:
            A dictionary containing the staking results
        """
        # Validate inputs
        if not validate_inputs(stake_amount, duration_days, lockup_days):
            logger.error("Invalid input parameters")
            raise ValueError("Invalid input parameters")
            
        try:
            # Calculate gross reward with compounding
            annual_rate = self.config.apy
            compound_freq = self.config.compound_frequency
            
            # Convert annual rate to daily equivalent for the calculation period
            # Time in years is duration_days / 365
            time_in_years = duration_days / 365.0
            gross_reward = calculate_compound_interest(
                stake_amount, 
                annual_rate, 
                time_in_years, 
                compound_freq
            ) - stake_amount
            
            # Ensure gross reward is not negative
            gross_reward = max(0, gross_reward)
            
            # Calculate penalty if applicable
            penalty = 0.0
            if lockup_days > 0 and lockup_days < duration_days:
                penalty = calculate_penalty(gross_reward, self.config.penalty_rate)
                
            net_reward = gross_reward - penalty
            
            result = {
                "gross_reward": gross_reward,
                "net_reward": net_reward,
                "penalty": penalty,
                "duration": duration_days
            }
            
            logger.info("Calculated rewards for stake amount %f: gross=%f, net=%f, penalty=%f", 
                      stake_amount, gross_reward, net_reward, penalty)
            
            return result
            
        except Exception as e:
            logger.error("Error calculating staking rewards: %s", str(e))
            raise RuntimeError(f"Error calculating rewards: {str(e)}") from e