import argparse
import sys
from typing import List
from decimal import Decimal, InvalidOperation

from src.staking_calculator import (
    calculate_apy,
    calculate_compound_interest,
    calculate_lockup_penalty,
    validate_inputs
)

def main():
    parser = argparse.ArgumentParser(
        description="Staking Reward Calculator - Calculate staking rewards and APY"
    )
    
    parser.add_argument(
        '--principal',
        type=Decimal,
        default=Decimal('1000'),
        help='Initial staked amount (default: 1000)'
    )
    
    parser.add_argument(
        '--rate',
        type=Decimal,
        default=Decimal('0.05'),
        help='Annual interest rate (default: 0.05)'
    )
    
    parser.add_argument(
        '--days', 
        type=int,
        default=365,
        help='Number of staking days (default: 365)'
    )
    
    parser.add_argument(
        '--compound-frequency',
        type=int,
        default=1,
        help='Compound frequency per year (default: 1)'
    )
    
    parser.add_argument(
        '--penalty-rate',
        type=Decimal,
        default=Decimal('0.02'),
        help='Lockup penalty rate (default: 0.02)'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['simple', 'detailed'],
        default='detailed',
        help='Output format (default: detailed)'
    )
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        # If no arguments provided, show help
        parser.print_help()
        return
    
    try:
        validate_inputs(args.principal, args.rate, args.days, args.compound_frequency, args.penalty_rate)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)
    
    # Calculate simple interest as well for comparison
    simple_interest = args.principal * args.rate * args.days / 365
    
    # Calculate APY
    apy = calculate_apy(args.rate, args.days)
    
    # Calculate final amount with compound interest
    final_amount = calculate_compound_interest(
        args.principal, 
        args.rate, 
        args.days, 
        args.compound_frequency
    )
    
    # Calculate penalty amount
    penalty_amount = calculate_lockup_penalty(args.principal, args.penalty_rate)
    
    # Display results
    if args.output_format == 'detailed':
        print(f"Principal Amount: {args.principal}")
        print(f"Interest Rate: {args.rate * 100}%")
        print(f"Staking Period: {args.days} days")
        print(f"Compound Frequency: {args.compound_frequency} times per year")
        print(f"APY: {apy:.2%}")
        print(f"Final Amount: {final_amount}")
        print(f"Penalty Amount: {penalty_amount}")
    else:
        print(f"Estimated return: {final_amount} {args.principal} after {args.days} days")
        print(f"APY: {apy:.2f}%")
    
    return {
        'principal': args.principal,
        'rate': args.rate,
        'days': args.days,
        'compound_frequency': args.compound_frequency,
        'penalty_rate': args.penalty_rate,
        'final_amount': final_amount,
        'penalty_amount': penalty_amount,
        'apy': apy
    }