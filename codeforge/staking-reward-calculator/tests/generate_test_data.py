import csv
import random
from typing import List, Dict, Any
from decimal import Decimal
import logging

def generate_test_scenarios(count: int = 100) -> List[Dict[str, Any]]:
    """
    Generate test data scenarios with varied parameters for staking calculations.
    
    Args:
        count: Number of scenarios to generate
        
    Returns:
        List of test scenarios with varied parameters
    """
    scenarios = []
    
    for i in range(count):
        # Generate varied test data
        stake_amount = round(random.uniform(100, 10000), 2)
        duration_days = random.randint(30, 1095)  # 30 days to 3 years
        annual_rate = round(random.uniform(0.05, 0.25), 4)  # 5% to 25%
        penalty_rate = round(random.uniform(0.01, 0.15), 4)  # 1% to 15%
        
        scenario = {
            'stake_amount': stake_amount,
            'duration_days': duration_days,
            'annual_rate': annual_rate,
            'penalty_rate': penalty_rate
        }
        scenarios.append(scenario)
    
    return scenarios

def save_to_csv(scenarios: List[Dict[str, Any]], filename: str) -> None:
    """
    Save generated scenarios to a CSV file.
    
    Args:
        scenarios: List of scenario dictionaries to save
        filename: Name of the file to save to
    """
    if not scenarios:
        raise ValueError("No scenarios provided to save")
    
    fieldnames = ['stake_amount', 'duration_days', 'annual_rate', 'penalty_rate']
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for scenario in scenarios:
                # Write each scenario as a row in the CSV
                writer.writerow(scenario)
    except Exception as e:
        raise IOError(f"Error writing to CSV file: {e}")

# Generate and save test scenarios to CSV
if __name__ == "__main__":
    # Generate 100 test scenarios
    test_scenarios = generate_test_scenarios(100)
    
    # Save to CSV file
    save_to_csv(test_scenarios, "test_data.csv")
    
    print(f"Generated and saved {len(test_scenarios)} test scenarios to test_data.csv")