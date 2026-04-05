import click
from src.cli import generate_project

@click.command()
@click.option('--name', prompt='Project name', help='Name of the project')
@click.option('--type', type=click.Choice(['python', 'javascript', 'rust']), prompt='Project type', help='Type of project to generate')
@click.option('--framework', default=None, help='Framework to use (optional)')
@click.version_option()
def main(name: str, type: str, framework: str = None) -> None:
    """Main entry point for the CLI application."""
    try:
        generate_project(name, type, framework)
        click.echo(f"Project '{name}' of type '{type}' generated successfully!")
    except Exception as e:
        click.echo(f"Error generating project: {e}")
        return 1

if __name__ == '__main__':
    main()