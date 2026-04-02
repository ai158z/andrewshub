import argparse
import logging
from decimal import Decimal, InvalidOperation
from typing import Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_inputs(*args) -> bool:
    """
    Validate that all input arguments are positive numbers.
    
    Args:
        *args: Variable number of arguments to validate
        
    Returns:
        bool: True if all inputs are valid positive numbers
        
    Raises:
        ValueError: If any input is negative or not a number
        TypeError: If any input is not a number
    """
    for arg in args:
        # Check if the argument is a number (int, float, or Decimal)
        if not isinstance(arg, (int, float, Decimal)):
            logger.error(f"Invalid type: {type(arg)}. Expected number.")
            raise TypeError(f"All inputs must be numbers. Received {type(arg)}")
        
        # Convert to Decimal for consistent comparison
        try:
            value = Decimal(str(arg))
        except (InvalidOperation, TypeError) as e:
            logger.error(f"Cannot convert {arg} to decimal: {e}")
            raise TypeError(f"Invalid numeric value: {arg}")
        
        # Check if the value is negative
        if value < 0:
            logger.error(f"Negative value not allowed: {value}")
            raise ValueError(f"All inputs must be non-negative. Received: {value}")
            
    return True

def calculate_apy(rate: Union[float, Decimal], days: int) -> Decimal:
    """
    Calculate Annual Percentage Yield (APY) based on a daily rate and compounding period.
    
    Args:
        rate: Daily interest rate (as a decimal, e.g., 0.01 for 1%)
        days: Number of days for compounding period
        
    Returns:
        Decimal: The calculated APY as a decimal (e.g., 0.12 for 12%)
        
    Raises:
        ValueError: If rate or days are invalid
        TypeError: If inputs are not numeric
    """
    # Validate inputs
    if not isinstance(rate, (int, float, Decimal)):
        raise TypeError("Rate must be a number")
    
    if not isinstance(days, int) or days <= 0:
        raise ValueError("Days must be a positive integer")
    
    # Convert inputs to Decimal for precision
    rate_decimal = Decimal(str(rate))
    days_decimal = Decimal(str(days))
    
    # Calculate APY: (1 + rate)^days - 1
    try:
        apy = (Decimal('1') + rate_decimal) ** days_decimal - Decimal('1')
        return apy
    except Exception as e:
        logger.error(f"Error calculating APY: {e}")
        raise ValueError(f"Error calculating APY: {e}")

def calculate_compound_interest(
    principal: Union[float, Decimal], 
    rate: Union[float, Decimal], 
    time: Union[float, int], 
    n: int
) -> Decimal:
    """
    Calculate compound interest using the formula: A = P(1 + r/n)^(nt).
    
    Args:
        principal: Initial amount invested
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
        n: Number of times interest is compounded per year
        
    Returns:
        Decimal: The total amount after compound interest
        
    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs are not numeric
    """
    # Validate inputs
    if not all(isinstance(x, (int, float, Decimal)) for x in [principal, rate, time]):
        raise TypeError("All inputs must be numbers")
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Compounding frequency (n) must be a positive integer")
    
    # Convert inputs to Decimal
    principal_decimal = Decimal(str(principal))
    rate_decimal = Decimal(str(rate))
    time_decimal = Decimal(str(time)))
    n_decimal = Decimal(str(n))
    
    # Calculate compound interest: A = P(1 + r/n)^(nt)
    try:
        # Calculate (1 + r/n)
        base = Decimal('1') + (rate_decimal / n_decimal)
        # Calculate nt (total compoundings)
        exponent = n_decimal * time_decimal
        # Calculate final amount
        amount = principal_decimal * (base ** exponent)
        return amount
    except Exception as e:
        logger.error(f"Error calculating compound interest: {e}")
        raise ValueError(f"Error calculating compound interest: {e}")

def calculate_lockup_penalty(
    amount: Union[float, Decimal], 
    penalty_rate: Union[float, Decimal]
) -> Decimal:
    """
    Calculate the penalty amount for early withdrawal from a lockup period.
    
    Args:
        amount: The total staked amount
        penalty_rate: The penalty rate as a decimal (e.g., 0.05 for 5%)
        
    Returns:
        Decimal: The penalty amount to be deducted
        
    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs are not numeric
    """
    # Validate inputs
    if not all(isinstance(x, (int, float, Decimal)) for x in [amount, penalty_rate]):
        raise TypeError("Amount and penalty_rate must be numbers")
    
    # Convert inputs to Decimal
    amount_decimal = Decimal(str(amount))
    penalty_rate_decimal = Decimal(str(penalty_rate))
    
    # Calculate penalty
    try:
        penalty = amount_decimal * penalty_rate_decimal
        return penalty
    except Exception as e:
        logger.error(f"Error calculating penalty: {e}")
        raise ValueError(f"Error calculating penalty: {e}")

def main():
    """Main function to run the staking reward calculator CLI."""
    parser = argparse.ArgumentParser(description="Staking Reward Calculator")
    parser.add_argument('--principal', type=float, help='Principal amount')
    parser.add_argument('--rate', type=float, help='Annual interest rate (as decimal)')
    parser.add_argument('--time', type=float, help='Time period in years')
    parser.add_argument('--n', type=int, help='Compounding frequency per year')
    parser.add_argument('--days', type=int, help='Number of days for APY calculation')
    parser.add_argument('--penalty-rate', type=float, help='Penalty rate (as decimal)')
    parser.add_argument('--amount', type=float, help='Amount for penalty calculation')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    try:
        # Handle compound interest calculation
        if args.principal is not None and args.rate is not None and args.time is not None and args.n is not None:
            result = calculate_compound_interest(args.principal, args.rate, args.time, args.n)
            print(f"Compound interest result: {result}")
            return
            
        # Handle APY calculation
        if args.rate is not None and args.days is not None:
            result = calculate_apy(args.rate, args.days)
            print(f"APY result: {result}")
            return
            
        # Handle penalty calculation
        if args.amount is not None and args.penalty_rate is not None:
            result = calculate_lockup_penalty(args.amount, args.penalty_rate)
            print(f"Penalty amount: {result}")
            return
            
        print("Invalid combination of arguments. Please check your inputs.")
        
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()