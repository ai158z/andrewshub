import os
import logging
from typing import Dict, Any
from jinja2 import Environment, BaseLoader

def create_directory(path: str) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Path to the directory to create
        
    Raises:
        OSError: If directory creation fails
    """
    try:
        if path == '':
            # Handle empty string path - don't create directory with makedirs
            return
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logging.debug(f"Created directory: {path}")
    except OSError as e:
        logging.error(f"Failed to create directory {path}: {e}")
        raise

def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file.
    
    Args:
        file_path: Path where the file should be written
        content: Content to write to the file
        
    Raises:
        IOError: If file writing fails
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory:
            create_directory(directory)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content if content is not None else '')
        logging.debug(f"Written file: {file_path}")
    except Exception as e:
        logging.error(f"Failed to write file {file_path}: {e}")
        raise

def render_template(template_str: str, context: Dict[str, Any]) -> str:
    """
    Render a template string with provided context.
    
    Args:
        template_str: Template string with Jinja2 syntax
        context: Dictionary with template variables
        
    Returns:
        Rendered template string
    """
    try:
        env = Environment(loader=BaseLoader())
        template = env.from_string(template_str)
        if context is None:
            context = {}
        return template.render(context)
    except Exception as e:
        logging.error(f"Failed to render template: {e}")
        raise