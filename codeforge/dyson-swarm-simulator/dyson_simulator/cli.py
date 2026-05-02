import click
import logging
from typing import Optional
from dyson_simulator.main import run_simulation
from dyson_simulator.models import SimulationParameters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Dyson Sphere Simulator CLI"""
    pass

@click.command()
@click.option('--target-capture', type=float, required=True, help='Target solar energy capture percentage (0-100)')
@click.option('--launch-mass-rate', type=float, required=True, help='Launch mass rate (kg/year)')
@click.option('--output-file', type=click.Path(), help='Output file path for results')
def simulate(target_capture: float, launch_mass_rate: float, output_file: Optional[str]):
    """Run a Dyson swarm simulation with specified parameters"""
    try:
        # Validate inputs
        if not 0 <= target_capture <= 100:
            raise click.BadParameter("Target capture must be between 0 and 100 percent")
            
        if launch_mass_rate <= 0:
            raise click.BadParameter("Launch mass rate must be positive")
        
        # Create simulation parameters
        params = SimulationParameters(
            target_capture_percent=target_capture,
            launch_mass_rate=launch_mass_rate
        )
        
        # Run simulation
        results = run_simulation(params)
        
        # Output results
        output_lines = []
        output_lines.append(f"Simulation Results for {target_capture}% capture target:")
        output_lines.append(f"  Timeline: {results.timeline_years} years")
        output_lines.append(f"  Required Mass: {results.total_mass_required} kg")
        output_lines.append(f"  Collector Area: {results.collector_area_m2} m²")
        
        # Format output
        formatted_output = "\n".join(output_lines)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(formatted_output)
            logger.info(f"Results saved to {output_file}")
        else:
            click.echo(formatted_output)
            
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        raise click.ClickException(f"Simulation failed: {str(e)}")

cli.add_command(simulate)

if __name__ == '__main__':
    cli()