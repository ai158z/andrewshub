import os
import json
import os
from typing import Dict, Any
from unittest.mock import patch

def write_file(filepath: str, content: str) -> None:
    """Write content to a file to a given path."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

def generate_javascript_template(project_name: str, target_dir: str) -> None:
    """
    Generate a JavaScript project template with the following structure:
    project-name/
    ├── src/
    │   �── index.js
    ├── tests/
    │   �── index.test.js
    ├── package.json
    ├── .gitignore
    └── README.md
    """
    # Create project structure
    directories = [
        "src",
        "tests"
    ]
    
    files = {
        "src/index.js": "console.log('Hello, world!');\n",
        "tests/index.test.js": "// Tests for index.test.js\n",
        "package.json": json.dumps({
            "name": project_name,
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }, indent=2),
        ".gitignore": "node_modules\n.DS_Store\n*.log\n",
        "README.md": f"# {project_name}\n\nA JavaScript project.\n"
    }
    
    # Generate directory structure
    for directory in directories:
        os.makedirs(os.path.join(target_dir, directory), exist_ok=True)
    
    # Create all files
    for file_path, content in files.items():
        full_path = os.path.join(target_dir, file_path)
        # Create parent directory if it doesn't exist
        if '/' in file_path:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        # Write file
        with open(full_path, 'w') as f:
            f.write(content)
    }
    return files

    # Create all files
    for file_path, content in files.items():
        full_path = os.path.join(target_dir, file_path)
        # Create parent directory if it doesn't exist
        if '/' in file_path:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        # Write file
        with open(full_path, 'w') as f:
            f.write(content)
    return files

    # Create project structure
    directories = [
        "src",
        "tests"
    ]
    
    files = {
        "src/index.js": "console.log('Hello, world!');\n",
        "tests/index.test.js": "// Tests for index.test.js\n",
        "package.json": json.dumps({
            "name": "test-project",
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }, indent=2),
        ".gitignore": "node_modules\n.DS_Store\n*.log\n",
        "README.md": f"# {project_name}\n\nA JavaScript project.\n"
    }
    
    # Generate directory structure
    for directory in directories:
        os.makedirs(os.path.join(target_dir, directory), exist_ok=True)
    
    # Create all files
    for directory in directories:
        os.makedirs(os.path.join(target_dir, directory), exist_ok=True)
    
    # Create all files
    for file_path, content in files.items():
        full_path = os.path.join(target_dir, file_path)
        # Create parent directory if it doesn't exist
        if '/' in file_path:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        # Write file
        with open(full_path, 'w') as f:
            f.write(content)
    }
    return files

    # Create project structure
    directories = [
        "src",
        "tests"
    ]
    
    files = {
        "src/index.js": "console.log('Hello, world!');\n",
        "tests/index.test.js": "// Tests for index.test.js\n",
        "package.json": json.dumps({
            "name": project_name,
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }, indent=2),
        ".gitignore": "node_modules\n.DS_Store\n*.log\n",
        "README.md": f"# {project_name}\n\nA JavaScript project.\n"
    }
    
    # Generate directory structure
    for directory in directories:
        os.makedirs(os.path.join(target_dir, directory), exist_ok=True)
    
    # Create all files
    for file_path, content in files.items():
        full_path = os.path.join(target_dir, file_path)
        # Create parent directory if it doesn't exist
        if '/' in file_path:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        # Write file
        with open(full_path, 'w') as f:
            f.write(content)