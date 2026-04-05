import os
import logging
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
import shutil

from src.scaffolding.config import get_project_config, save_config
from src.scaffolding.templates.python import generate_python_template
from src.scaffolding.templates.javascript import generate_javascript_template
from src.scaffolding.templates.web import generate_web_template
from src.scaffolding.templates.library import generate_library_template
import os
import logging
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
import shutil

from src.scaffolding.config import get_project_config, save_config
from src.scaffolding.templates.python import generate_python_template
from src.scaffolding.templates.javascript import generate_javascript_template
from src.scaffolding.templates.web import generate_web_template
from src.scaffolding.templates.library import generate_library_template

def generate_project_structure(project_name: str, project_path: str) -> Dict[str, str]:
    config = get_project_config()
    project_type = config.get('project_type', 'python')
    
    if project_type == 'python':
        template_content = generate_python_template()
    elif project_type == 'javascript':
        template_content = generate_javascript_template()
    elif project_type == 'web':
        template_content = generate_web_template()
    elif project_type == 'library':
        template_content = generate_library_template()
    else:
        template_content = ""

    return {
        "project_name': 'python', 'javascript', 'web', 'library'
    }
    return {template_content}

def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)

# Read all files in a directory and subdirectories.
def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}")
        return []

def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}")
        return []

def generate_project_structure(project_name: str, project_path: str) -> Dict[str, str]:
    config = get_project_config()
    project_type = config.get('project_type', 'python')
    
    if project_type == 'python':
        template_content = generate_python_template()
    elif project_type == 'javascript':
        template_content = generate_javascript_template()
    elif project_type == 'web':
        template_content = generate_web_template()
    elif project_type == 'library':
        template_content = generate_library_template()
    else:
        template_content = ""

    return {template_content}

def write_file(file_path: str, content: str) -> None:
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)

# Read all files in a directory and subdirectories.
def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}")
        return []

# Read all files in a directory and subdirectories.
def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}"))
        return []

# Read all files in a directory and subdirectories.
def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}")
        return []

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files

def read_directory(directory_path: str) -> List[str]:
    try:
        files = []
        for root, dirs, file_list in os.walk(directory_path):
            for file in file_list:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files
    except Exception as e:
        logger.error(f"Error reading directory: {e}")
        return []

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files

def read_directory(directory_path: str) -> List[str]:
    files = []
    for root, dirs, file_list in os.walk(directory_path):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)
    return files