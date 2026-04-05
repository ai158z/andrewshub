import click
import os
import sys
import logging
from typing import Optional
import json

# Fix the import issues by using relative imports
try:
    from scaffolding.config import get_project_config, save_config
    from scaffolding.generator import generate_project_structure, write_file, read_directory
    from scaffolding.templates.python import generate_python_template
    from scaffolding.templates.javascript import generate_javascript_template
    from scaffolding.templates.web import generate_web_template
    from scaffolding.templates.library import generate_library_template
except ImportError:
    # Fallback to absolute imports if relative don't work
    from scaffolding.config import get_project_config, save_config
    from scaffolding.generator import generate_project_structure, write_file, read_directory
    from scaffolding.templates.python import generate_python_template
    from scaffolding.templates.javascript import generate_javascript_template
    from scaffolding.templates.web import generate_web_template
    from scaffolding.templates.library import generate_library_template


@click.command()
@click.option('--project-name', '-n', help='Name of the project to scaffold')
@click.option('--template', '-t', type=click.Choice(['python', 'javascript', 'web', 'library']), 
              help='Template type to use')
@click.option('--output-dir', '-o', default='.', help='Output directory for the project')
@click.option('--config', '-c', help='Path to configuration file')
def main():
    """Main CLI entry point for the project scaffolding tool."""
    pass


if __name__ == '__main__':
    main()