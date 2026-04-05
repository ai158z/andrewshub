import os
import logging
from typing import Dict, Any
from src.utils import create_directory, write_file, render_template


logger = logging.getLogger(__name__)

# Define the directory structures directly since we can't import get_structure
PYTHON_STRUCTURE = [
    "src",
    "src/main",
    "src/tests",
    "docs",
    "config"
]

JAVASCRIPT_STRUCTURE = [
    "src",
    "src/components",
    "src/utils",
    "tests",
    "docs"
]

RUST_STRUCTURE = [
    "src",
    "src/bin",
    "tests",
    "examples",
    "benches"
]

# Template files for different project types
PYTHON_FILES = [
    ("README.md", "# {{project_name}}\n\nPython project template"),
    ("requirements.txt", "# Project dependencies\n"),
    ("src/main/__init__.py", "# Python package\n"),
    ("src/main/app.py", "# Main application file\n\ndef main():\n    pass\n"),
    ("src/tests/__init__.py", "# Test package\n")
]

JAVASCRIPT_FILES = [
    ("README.md", "# {{project_name}}\n\nJavaScript project template"),
    ("src/index.js", "// Main JavaScript file\nconsole.log('Hello World');\n"),
    ("package.json", '{\n  "name": "{{project_name}}",\n  "version": "1.0.0"\n}'),
    ("src/utils/helpers.js", "// Utility functions\n")
]

RUST_FILES = [
    ("README.md", "# {{project_name}}\n\nRust project template"),
    ("Cargo.toml", '[package]\nname = "{{project_name}}"\nversion = "0.1.0"\n'),
    ("src/main.rs", 'fn main() {\n    println!("Hello, world!");\n}'),
    ("src/lib.rs", '// Library crate\n')
]


def create_project_structure(name: str, project_type: str, framework: str) -> str:
    """
    Create project directory structure based on project type.
    
    Args:
        name: Project name
        project_type: Type of project (python, javascript, rust)
        framework: Framework to use
        
    Returns:
        str: Path to created project directory
    """
    if not name or not isinstance(name, str):
        raise ValueError("Project name must be a non-empty string")
    
    if not project_type or not isinstance(project_type, str):
        raise ValueError("Project type must be a non-empty string")
        
    if not framework or not isinstance(framework, str):
        raise ValueError("Framework must be a non-empty string")
    
    project_path = os.path.join(os.getcwd(), name)
    
    # Create project root directory
    create_directory(project_path)
    
    # Get structure based on project type
    if project_type == "python":
        structure = PYTHON_STRUCTURE
    elif project_type == "javascript":
        structure = JAVASCRIPT_STRUCTURE
    elif project_type == "rust":
        structure = RUST_STRUCTURE
    else:
        raise ValueError(f"Unsupported project type: {project_type}")
    
    # Create directory structure
    for dir_path in structure:
        full_path = os.path.join(project_path, dir_path)
        create_directory(full_path)
        logger.info(f"Created directory: {full_path}")
    
    return project_path


def generate_files(project_path: str, template_data: Dict[str, Any]) -> None:
    """
    Generate files with template data.
    
    Args:
        project_path: Path to project directory
        template_data: Data to use in templates
    """
    if not project_path or not isinstance(project_path, str):
        raise ValueError("Project path must be a non-empty string")
        
    if not isinstance(template_data, dict):
        raise ValueError("Template data must be a dictionary")
    
    # Determine project type from path
    project_name = os.path.basename(project_path)
    
    # Generate project files based on project type
    project_type = None
    files_to_generate = []
    
    # Check for existing project markers
    if os.path.exists(os.path.join(project_path, "src")) and not os.path.exists(os.path.join(project_path, "Cargo.toml")):
        project_type = "python"
        files_to_generate = PYTHON_FILES
    elif os.path.exists(os.path.join(project_path, "src")) and os.path.exists(os.path.join(project_path, "Cargo.toml")):
        project_type = "rust"
        files_to_generate = RUST_FILES
    elif os.path.exists(os.path.join(project_path, "src")):
        # Check if it's a JavaScript project
        project_type = "javascript"
        files_to_generate = JAVASCRIPT_FILES
    else:
        # Try to determine from existing files
        if os.path.exists(os.path.join(project_path, "pyproject.toml")):
            project_type = "python"
            files_to_generate = PYTHON_FILES
        elif os.path.exists(os.path.join(project_path, "package.json")):
            project_type = "javascript"
            files_to_generate = JAVASCRIPT_FILES
        elif os.path.exists(os.path.join(project_path, "Cargo.toml")):
            project_type = "rust"
            files_to_generate = RUST_FILES
        else:
            raise ValueError(f"Could not determine project type for path: {project_path}")
    
    # Generate files
    for file_path, template_content in files_to_generate:
        full_path = os.path.join(project_path, file_path)
        rendered_content = render_template(template_content, template_data)
        write_file(full_path, rendered_content)
        logger.info(f"Generated file: {full_path}")


def copy_template_files(project_path: str, template_module) -> None:
    """
    Copy template files to project directory.
    
    Args:
        project_path: Path to project directory
        template_module: Module containing template functions
    """
    if not project_path or not isinstance(project_path, str):
        raise ValueError("Project path must be a non-empty string")
        
    if not template_module:
        raise ValueError("Template module cannot be None")
    
    # Generate template files based on project type
    project_type = None
    files_to_generate = []
    
    # Determine project type from the project path
    if os.path.exists(os.path.join(project_path, "pyproject.toml")):
        project_type = "python"
        files_to_generate = PYTHON_FILES
    elif os.path.exists(os.path.join(project_path, "package.json")):
        project_type = "javascript"
        files_to_generate = JAVASCRIPT_FILES
    elif os.path.exists(os.path.join(project_path, "Cargo.toml")):
        project_type = "rust"
        files_to_generate = RUST_FILES
    else:
        raise ValueError("Could not determine project type for path: {project_path}")
    
    # Generate files from templates
    for file_path, template_content in files_to_generate:
        full_path = os.path.join(project_path, file_path)
        context = {"project_name": os.path.basename(project_path)}
        rendered_content = render_template(template_content, context)
        write_file(full_path, rendered_content)
        logger.info(f"Created template file: {full_path}")