import logging
from decimal import Decimal, InvalidOperation
from typing import Union

logger = logging.getLogger(__name__)

class StakingCalculator:
    """
    A calculator for staking rewards with support for APY calculations,
    compound interest, and lockup penalties.
    """

    def calculate_apy(
        self,
        stake_amount: Union[int, float, Decimal],
        duration_years: Union[int, float, Decimal],
        apy_rate: Union[float, Decimal]
    ) -> Decimal:
        """
        Calculate the annual percentage yield (APY) for staking.

        Args:
            stake_amount: The amount of tokens staked
            duration_years: The duration of staking in years
            apy_rate: The annual percentage yield rate

        Returns:
            Decimal: The calculated APY reward

        Raises:
            ValueError: If any input is invalid
        """
        # Validate inputs
        self.validate_input(stake_amount)
        self.validate_input(duration_years)
        self.validate_input(apy_rate)
        
        if apy_rate < 0:
            raise ValueError("APY rate cannot be negative")
            
        if duration_years < 0:
            raise ValueError("Duration cannot be negative")
            
        if stake_amount < 0:
            raise ValueError("Stake amount cannot be negative")

        # Convert to Decimal for precision
        try:
            principal = Decimal(str(stake_amount))
            rate = Decimal(str(apy_rate))
            time = Decimal(str(duration_years))
        except (InvalidOperation, TypeError) as e:
            raise ValueError("Invalid input values") from e

        # APY calculation: reward = principal * (1 + rate/100)^time - principal
        if time == 0:
            return Decimal('0')
            
        # Using compound interest formula for APY: A = P * (1 + r)^t - P
        amount = principal * ((1 + rate/100) ** time)
        reward = amount - principal
        return reward.quantize(Decimal('0.0000000001')).normalize()

    def calculate_compound_interest(
        self,
        principal: Union[int, float, Decimal],
        rate: Union[float, Decimal],
        time: Union[int, float, Decimal],
        compound_frequency: int = 1
    ) -> Decimal:
        """
        Calculate compound interest.

        Args:
            principal: The initial amount
            rate: The annual interest rate (in percentage)
            time: The time in years
            compound_frequency: How many times interest is compounded per year

        Returns:
            Decimal: The final amount after compound interest
        """
        # Validate inputs
        self.validate_input(principal)
        self.validate_input(rate)
        self.validate_input(time)
        self.validate_input(compound_frequency)
        
        if compound_frequency <= 0:
            raise ValueError("Compound frequency must be positive")
            
        if time < 0:
            raise ValueError("Time cannot be negative")
            
        if principal < 0:
            raise ValueError("Principal cannot be negative")

        # Convert to Decimal for precision
        try:
            p = Decimal(str(principal))
            r = Decimal(str(rate))
            t = Decimal(str(time))
            n = Decimal(str(compound_frequency))
        except (InvalidOperation, TypeError) as e:
            raise ValueError("Invalid input values") from e

        # Compound interest formula: A = P(1 + r/100/n)^(n*t)
        if t == 0:
            return p
            
        base = 1 + (r / 100) / n
        if base <= 0:
            raise ValueError("Invalid calculation parameters")
            
        # Using the compound interest formula
        # A = P(1 + r/100/n)^(n*t)
        amount = p * (base ** (n * t))
        return amount.quantize(Decimal('0.0000000001')).normalize()

    def apply_lockup_penalty(
        self,
        reward: Union[int, float, Decimal],
        penalty_rate: Union[float, Decimal]
    ) -> Decimal:
        """
        Apply a lockup penalty to a reward amount.

        Args:
            reward: The reward amount to which penalty is applied
            penalty_rate: The penalty rate (in percentage)

        Returns:
            Decimal: The reward amount after applying penalty
        """
        self.validate_input(reward)
        self.validate_input(penalty_rate)
        
        if penalty_rate < 0 or penalty_rate > 100:
            raise ValueError("Penalty rate must be between 0 and 100")

        try:
            reward_amount = Decimal(str(reward))
            penalty = Decimal(str(penalty_rate))
        except (InvalidOperation, TypeError) as e:
            raise ValueError("Invalid input values") from e

        if reward_amount < 0:
            raise ValueError("Reward amount cannot be negative")

        # Calculate penalty: penalty_amount = reward * (penalty_rate / 100)
        penalty_amount = reward_amount * (penalty / 100)
        remaining = reward_amount - penalty_amount
        return remaining.quantize(Decimal('0.0000000001')).normalize()

    def validate_input(self, value) -> bool:
        """
        Validate input values for calculator methods.

        Args:
            value: The value to validate

        Returns:
            bool: True if valid

        Raises:
            ValueError: If the input is invalid
        """
        if value is None:
            raise ValueError("Value cannot be None")
            
        if isinstance(value, str):
            try:
                float(value)
            except ValueError:
                raise ValueError(f"Invalid input: {value}")
        elif not isinstance(value, (int, float, Decimal)):
            raise ValueError(f"Invalid input type: {type(value)}")
        else:
            try:
                Decimal(str(value))
            except (InvalidOperation, TypeError):
                raise ValueError(f"Invalid input value: {value}")
            
        return True