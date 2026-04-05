import typer
from typing import Optional
from pathlib import Path
from src.scaffolder.core import ProjectConfig, TemplateManager
from src.scaffolder.utils import validate_project_name
from src.scaffolder.generator import FileGenerator
from src.scaffolder.templates.python import python_cli_template, python_web_template, python_lib_template
from src.scaffolder.templates.javascript import js_cli_template, js_web_template, js_lib_template
from src.scaffolder.templates.rust import rust_cli_template, rust_web_template

app = typer.Typer()

@app.command()
def scaffold(
    name: str = typer.Argument(..., help="Name of the project to create"),
    template: str = typer.Option("python-cli", help="Template to use for scaffolding"),
    output_dir: Path = typer.Option(Path("."), help="Output directory for the project"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created without actually creating it")
):
    """Scaffold a new project using the specified template."""
    try:
        # Validate project name
        if not validate_project_name(name):
            typer.echo(f"Invalid project name: {name}")
            raise typer.Exit(1)
        
        # Create project config
        config = ProjectConfig(
            project_name=name,
            template_name=template,
            output_dir=output_dir
        )
        
        # Initialize template manager
        template_manager = TemplateManager(config)
        
        # Create the project
        if not dry_run:
            template_manager.create_project()
            typer.echo(f"Project '{name}' created successfully!")
        else:
            typer.echo(f"Dry run: Would create project '{name}' using template '{template}'")
            
    except Exception as e:
        typer.echo(f"Error creating project: {e}")
        raise typer.Exit(1)

@app.command("list-templates")
def list_templates_cmd():
    """List all available templates."""
    typer.echo("Available templates:")
    typer.echo("  python-cli: Python CLI application template")
    typer.echo("  python-web: Python web application template")
    typer.echo("  python-lib: Python library template")
    typer.echo("  js-cli: JavaScript CLI application template")
    typer.echo("  js-web: JavaScript web application template")
    typer.echo("  js-lib: JavaScript library template")
    typer.echo("  rust-cli: Rust CLI application template")
    typer.echo("  rust-web: Rust web application template")

def main():
    """Main entry point for the CLI."""
    try:
        app()
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    main()