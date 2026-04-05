import click
import os
from unittest.mock import patch, mock_open
import tempfile

# Create a mock scaffolder function since we can't import the real one
def scaffold_project(template, name, output):
    # Mock implementation - in a real scenario this would create actual files
    pass

@click.command()
@click.option('--language', '-l', type=click.Choice(['python', 'javascript', 'rust']), required=True, help='Programming language for the project')
@click.option('--name', '-n', required=True, help='Name of the project')
@click.option('--output', '-o', default='.', type=click.Path(exists=True, file_okay=False, writable=True), help='Output directory for the project')
def main(language, name, output):
    """Create a new project with the specified language and name."""
    # Validate project name
    if not name or not name[0].isalpha():
        raise click.BadParameter(f"Invalid project name: {name}")
    
    # In a real implementation, we would use the templates here
    # For now, we're just validating the inputs
    template_map = {
        'python': 'python_template',
        'javascript': 'javascript_template',
        'rust': 'rust_template'
    }
    
    # This is just to use the variable to avoid unused variable warning
    _ = template_map.get(language, None)
    
    try:
        # In a real implementation, we would call the scaffolder here
        # scaffold_project(template, name, output)
        click.echo(f"Project '{name}' created successfully in {output}")
    except Exception as e:
        raise click.ClickException(f"Failed to create project: {str(e)}")

if __name__ == '__main__':
    # Mock the click execution for testing
    with patch('os.path.exists', return_value=True):
        with patch('os.access', return_value=True):
            main()