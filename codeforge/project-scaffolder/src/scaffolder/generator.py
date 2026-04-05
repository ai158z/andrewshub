import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger(__name__)

class FileGenerator:
    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = template_dir
        self.jinja_env = None
        if template_dir:
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def create_directory(self, path: str) -> bool:
        """
        Create a directory at the specified path.
        
        Args:
            path: Path where directory should be created
            
        Returns:
            bool: True if directory was created, False if it already existed
            
        Raises:
            PermissionError: If user doesn't have permission to create directory
            OSError: If directory creation fails
        """
        try:
            path_obj = Path(path)
            if path_obj.exists():
                if path_obj.is_dir():
                    logger.info(f"Directory already exists: {path}")
                    return False
                else:
                    raise FileExistsError(f"Path exists but is not a directory: {path}")
            
            path_obj.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {str(e)}")
            raise

    def write_file(self, path: str, content: str, overwrite: bool = False) -> bool:
        """
        Write content to a file at the specified path.
        
        Args:
            path: File path to write to
            content: Content to write
            overwrite: Whether to overwrite existing file
            
        Returns:
            bool: True if file was written, False if it already existed and overwrite=False
            
        Raises:
            PermissionError: If user doesn't have permission to write file
            OSError: If file writing fails
        """
        try:
            path_obj = Path(path)
            
            if path_obj.exists() and not overwrite:
                logger.info(f"File already exists and overwrite disabled: {path}")
                return False
            
            # Create parent directories if they don't exist
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path_obj, 'w') as f:
                f.write(content)
            
            logger.info(f"Written file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write file {path}: {str(e)}")
            raise

    def copy_template(self, template_name: str, output_path: str, context: Dict[str, Any]) -> None:
        """
        Copy and render a template to the output directory with provided context.
        
        Args:
            template_name: Name of the template to render
            output_path: Path where rendered template should be written
            context: Context variables for template rendering
        """
        if not self.jinja_env:
            raise ValueError("Template directory not configured")
            
        try:
            template = self.jinja_env.get_template(template_name)
            output = template.render(context)
            
            # Create output directory
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write rendered template
            with open(output_file, 'w') as f:
                f.write(output)
                
            logger.info(f"Rendered template {template_name} to {output_path}")
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {str(e)}")
            raise

    def generate_project_structure(self, base_path: str, structure: Dict[str, Any], context: Dict[str, Any] = None) -> None:
        """
        Generate project structure from a dictionary definition.
        
        Args:
            base_path: Base directory for the project
            structure: Dictionary defining the project structure
            context: Context for template rendering (optional)
        """
        base_path_obj = Path(base_path)
        
        for item, content in structure.items():
            item_path = base_path_obj / item
            
            if isinstance(content, dict):
                # It's a directory with contents
                self.create_directory(str(item_path))
                # Recursively generate contents
                self.generate_project_structure(str(item_path), content, context)
            elif isinstance(content, str):
                # It's a file
                if self.jinja_env and context:
                    # Render template file
                    try:
                        template = self.jinja_env.from_string(content)
                        rendered_content = template.render(context)
                        self.write_file(str(item_path), rendered_content)
                    except Exception as e:
                        logger.error(f"Error rendering template for {item}: {str(e)}")
                        # Write the raw content if rendering fails
                        self.write_file(str(item_path), content)
                else:
                    # Write raw content
                    self.write_file(str(item_path), content)
            else:
                logger.warning(f"Invalid content type for {item}: {type(content)}")