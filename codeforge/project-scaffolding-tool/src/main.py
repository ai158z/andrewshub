import os
import sys
import click
from src.scaffolding.config import get_project_config
from src.scaffolding.cli import main as cli_main
from src.scaffolding.generator import generate_project_structure, write_file
from src.scaffolding.templates.python import generate_python_template
from src.scaffolding.templates.javascript import generate_javascript_template
from src.scaffolding.templates.web import generate_web_template
from src.scaffolding.templates.library import generate_library_template

def scaffolding_tool():
    """Main entry point for the scaffolding tool"""
    try:
        # Load configuration
        config = get_project_config()
        project_structure = {}
        
        # Generate templates based on project type
        if config.get("type") == "python":
            project_structure = generate_python_template()
        elif config.get("type") == "javascript":
            project_structure = generate_javascript_template()
        elif config.get("type") == "web":
            project_structure = generate_web_template()
        elif config.get("type") == "library":
            project_structure = generate_library_template()
        else:
            # Default to library template if unknown type
            project_structure = generate_library_template()
            
        # Generate the project structure
        write_file(project_structure)
        
        # Run the CLI
        cli_main()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    scaffolding_tool()