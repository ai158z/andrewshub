from typing import Union


class StakingResult:
    """
    Data model representing the result of a staking calculation.
    
    Attributes:
        gross_reward (float): The total reward before any penalties
        net_reward (float): The reward after applying penalties
        penalty (float): The penalty amount deducted from gross reward
        duration (int): The staking duration in days
    """
    
    def __init__(self, gross_reward: float, net_reward: float, penalty: float, duration: int):
        """
        Initialize a StakingResult instance.
        
        Args:
            gross_reward: The total reward before any penalties
            net_reward: The reward after applying penalties
            penalty: The penalty amount deducted from gross reward
            duration: The staking duration in days
        """
        if gross_reward < 0:
            raise ValueError("Gross reward cannot be negative")
        if net_reward < 0:
            raise ValueError("Net reward cannot be negative")
        if penalty < 0:
            raise ValueError("Penalty cannot be negative")
        if duration < 0:
            raise ValueError("Duration cannot be negative")
            
        self.gross_reward = gross_reward
        self.net_reward = net_reward
        self.penalty = penalty
        self.duration = duration
    
    def __repr__(self) -> str:
        """String representation of StakingResult."""
        return (f"StakingResult(gross_reward={self.gross_reward}, "
                f"net_reward={self.net_reward}, penalty={self.penalty}, "
                f"duration={self.duration})")
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality with another StakingResult.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if objects are equal, False otherwise
        """
        if not isinstance(other, StakingResult):
            return False
        return (self.gross_reward == other.gross_reward and 
                self.net_reward == other.net_reward and
                self.penalty == other.penalty and
                self.duration == other.duration)
    
    def __ne__(self, other: object) -> bool:
        """
        Check inequality with another StakingResult.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if objects are not equal, False otherwise
        """
        return not self.__eq__(other)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StakingResult':
        """
        Create a StakingResult from a dictionary.
        
        Args:
            data: Dictionary containing staking result data
            
        Returns:
            StakingResult instance
        """
        return cls(
            gross_reward=data['gross_reward'],
            net_reward=data['net_reward'],
            penalty=data['penalty'],
            duration=data['duration']
        )


class StakingConfig:
    """
    Configuration for staking calculations.
    
    Attributes:
        apy (float): Annual Percentage Yield as a decimal (e.g., 0.05 for 5%)
        compound_frequency (int): Number of times interest compounds per year
        penalty_rate (float): Penalty rate as a decimal (e.g., 0.01 for 1%)
    """
    
    def __init__(self, apy: float, compound_frequency: int = 1, penalty_rate: float = 0.0):
        """
        Initialize a StakingConfig instance.
        
        Args:
            apy: Annual Percentage Yield as a decimal
            compound_frequency: Number of compounding periods per year
            penalty_rate: Penalty rate as a decimal
        """
        if not 0 <= apy <= 1:
            raise ValueError("APY must be between 0 and 1")
        if compound_frequency <= 0:
            raise ValueError("Compound frequency must be positive")
        if not 0 <= penalty_rate <= 1:
            raise ValueError("Penalty rate must be between 0 and 1")
            
        self.apy = apy
        self.compound_frequency = compound_frequency
        self.penalty_rate = penalty_rate
    
    def __repr__(self) -> str:
        """String representation of StakingConfig."""
        return (f"StakingConfig(apy={self.apy}, "
                f"compound_frequency={self.compound_frequency}, "
                f"penalty_rate={self.penalty_rate})")
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality with another StakingConfig.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if objects are equal, False otherwise
        """
        if not isinstance(other, StakingConfig):
            return False
        return (self.apy == other.apy and 
                self.compound_frequency == other.compound_frequency and
                self.penalty_rate == other.penalty_rate)
    
    def __ne__(self, other: object) -> bool:
        """
        Check inequality with another StakingConfig.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if objects are not equal, False otherwise
        """
        return not self.__eq__(other)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StakingConfig':
        """
        Create a StakingConfig from a dictionary.
        
        Args:
            data: Dictionary containing staking configuration data
            
        Returns:
            StakingConfig instance
        """
        return cls(
            apy=data['apy'],
            compound_frequency=data.get('compound_frequency', 1),
            penalty_rate=data.get('penalty_rate', 0.0)
        )
    
    def to_dict(self) -> dict:
        """
        Convert StakingConfig to a dictionary.
        
        Returns:
            Dictionary representation of the config
        """
        return {
            'apy': self.apy,
            'compound_frequency': self.compound_frequency,
            'penalty_rate': self.penalty_rate
        }