import os
import logging
from typing import Dict, Optional, Any, List
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel, field_validator
from src.scaffolder.generator import FileGenerator
from src.scaffolder.utils import sanitize_path, validate_project_name

# Import template functions
from src.scaffolder.templates.python import python_cli_template, python_web_template, python_lib_template
from src.scaffolder.templates.javascript import js_cli_template, js_web_template
from src.scaffolder.templates.rust import rust_cli_template, rust_web_template, rust_lib_template

logger = logging.getLogger(__name__)

class ProjectConfig(BaseModel):
    name: str
    template: str
    path: str
    version: str = "0.1.0"
    author: str = "Unknown"
    description: str = "A new project"

    @field_validator('name')
    def validate_name(cls, v):
        if not validate_project_name(v):
            raise ValueError('Invalid project name')
        return v

class TemplateManager:
    def __init__(self):
        self.templates = {
            'python': {
                'cli': python_cli_template,
                'web': python_web_template,
                'lib': python_lib_template
            },
            'javascript': {
                'cli': js_cli_template,
                'web': js_web_template
            },
            'rust': {
                'cli': rust_cli_template,
                'web': rust_web_template,
                'lib': rust_lib_template
            }
        }

    def get_template(self, template_type: str, template_category: str) -> Dict[str, Any]:
        if template_type not in self.templates:
            raise ValueError(f"Unsupported template type: {template_type}")
        if template_category not in self.templates[template_type]:
            raise ValueError(f"Template category '{template_category}' not found in {template_type} templates")
        return self.templates[template_type][template_category]

    def create_project(self, project_name: str, template_type: str = 'python', template_category: str = 'cli') -> Optional[Dict[str, Any]]:
        if not validate_project_name(project_name):
            return None
        template = self.get_template(template_category, template_type)
        if not template:
            return None
        template['name'] = project_name
        template['template_type'] = template_type
        template['template_category'] = template_category
        return template

class ProjectManager:
    def __init__(self, project_name: str, template: str = 'python'):
        if not validate_project_name(project_name):
            raise ValueError('Invalid project name')
        self.project_name = project_name
        self.template = template
        self.validate()
        
    def validate(self):
        # Validation is done via validate_project_name in __init__
        pass
        
    def get_template(self, template_type: str = 'python', template_category: str = 'cli') -> Dict[str, str]:
        # This is a simplified implementation - in reality would use the template manager
        template = {}
        template["template_type"] = template_type
        template["template_category"] = template_category
        return template