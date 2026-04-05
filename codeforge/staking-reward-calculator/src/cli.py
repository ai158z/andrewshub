import click
import logging
from typing import Dict, Any
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_inputs(stake_amount: float, duration: int, network: str, currency: str) -> None:
    """Validate CLI inputs"""
    if stake_amount <= 0:
        raise ValueError("Stake amount must be positive")
    
    if duration <= 0:
        raise ValueError("Duration must be positive")
        
    if not network:
        raise ValueError("Network cannot be empty")
        
    if not currency:
        raise ValueError("Currency cannot be empty")

def format_rewards_output(rewards_data: Dict[str, Any]) -> str:
    """Format rewards data for display"""
    output = []
    output.append("Staking Rewards Summary:")
    output.append(f"  Initial Stake: {rewards_data['initial_stake']} tokens")
    output.append(f"  Final Value: {rewards_data['final_value']:.6f} tokens")
    output.append(f"  Total Rewards: {rewards_data['total_rewards']:.6f} tokens")
    output.append(f"  ROI: {rewards_data['roi']:.2f}%")
    return "\n".join(output)

@click.command()
@click.option('--stake-amount', '-s', type=float, required=True, help='Amount to stake')
@click.option('--duration', '-d', type=int, required=True, help='Staking duration in days')
@click.option('--network', '-n', type=str, required=True, help='Blockchain network name')
@click.option('--currency', '-c', type=str, default='USD', help='Currency for value conversion')
def main(stake_amount: float, duration: int, network: str, currency: str) -> None:
    """Main CLI entry point for staking reward calculation"""
    try:
        # Validate inputs
        validate_inputs(stake_amount, duration, network, currency)
        
        # Get network parameters
        apy = get_network_apy(network)
        commission = get_network_commission(network)
        
        # Calculate rewards
        rewards_data = calculate_rewards(stake_amount, duration, apy, commission)
        
        # Convert to fiat
        initial_fiat_value = convert_to_fiat(stake_amount, network, currency)
        final_fiat_value = convert_to_fiat(rewards_data['final_value'], network, currency)
        
        # Add fiat values to rewards data
        rewards_data['initial_fiat'] = initial_fiat_value
        rewards_data['final_fiat'] = final_fiat_value
        
        # Display results
        click.echo(format_rewards_output(rewards_data))
        
        # Risk analysis
        risks = analyze_network_risks(network)
        click.echo(f"\nNetwork Risk Analysis:")
        for risk, level in risks.items():
            click.echo(f"  {risk}: {level}")
            
        # Plotting
        fig = plot_rewards_over_time(rewards_data)
        if fig:
            click.echo(f"\nPlot generated successfully")
            
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        click.echo(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        click.echo(f"Error: {e}")
        sys.exit(1)

# Import statements for functions used in the module
from src.calculator import calculate_rewards
from src.visualizer import plot_rewards_over_time
from src.risk_analyzer import analyze_network_risks
from src.network_data import get_network_apy, get_network_commission
from src.currency_converter import convert_to_fiat

if __name__ == '__main__':
    main()