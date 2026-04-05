import os
from typing import Dict, Any
from src.utils import validate_project_name, create_directory, write_file
from src.templates import python_template, javascript_template, rust_template

TEMPLATE_MAP = {
    'python': python_template.PYTHON_TEMPLATE,
    'javascript': javascript_template.JAVASCRIPT_TEMPLATE,
    'rust': rust_template.RUST_TEMPLATE
}

def scaffold_project(template: str, project_name: str, output_dir: str) -> bool:
    """Scaffold a new project based on the provided template."""
    # Validate inputs
    if not template:
        raise ValueError("Template name must be provided")
    
    if template not in TEMPLATE_MAP:
        raise ValueError(f"Unsupported template: {template}")
        
    if not project_name:
        raise ValueError("Project name must be provided")
        
    if not validate_project_name(project_name):
        raise ValueError(f"Invalid project name: {project_name}")
    
    # Create project directory
    project_path = os.path.join(output_dir, project_name)
    create_directory(project_path)
    
    # Get template files
    template_files = TEMPLATE_MAP[template]
    
    # Create all directories first
    for file_path in template_files.get('directories', []):
        dir_path = os.path.join(project_path, file_path)
        create_directory(dir_path)
    
    # Create files from template
    for file_path, content in template_files.get('files', {}).items():
        full_path = os.path.join(project_path, file_path)
        # Ensure parent directory exists
        parent_dir = os.path.dirname(full_path)
        if parent_dir:
            create_directory(parent_dir)
        write_file(full_path, content)
    
    return True