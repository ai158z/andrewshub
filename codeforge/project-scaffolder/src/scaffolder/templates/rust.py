import re
from typing import Dict, Any

class RustTemplate:
    def __init__(self, project_name: str):
        if not project_name:
            raise ValueError(f"Invalid project name: {project_name}")
        # Validate that the project name is a valid Rust crate name
        if not self._is_valid_crate_name(project_name):
            raise ValueError(f"Invalid project name: {project_name}")
        self.project_name = project_name

    def _is_valid_crate_name(self, name: str) -> bool:
        # Rust crate names must start with a letter or underscore and only contain 
        # alphanumeric characters and underscores
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return re.match(pattern, name) is not None

    def generate(self) -> Dict[str, str]:
        """Generate the complete file structure for a Rust project"""
        return {
            "src/lib.rs": self._generate_lib_rs(),
            "src/main.rs": self._generate_main_rs(),
            "Cargo.toml": self._generate_cargo_toml(),
            "README.md": self._generate_readme()
        }

    def _sanitize_name(self, name: str) -> str:
        """Convert project name to valid Rust identifier"""
        # Replace hyphens and dots with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Remove leading numbers
        if sanitized and sanitized[0].isdigit():
            sanitized = '_' + sanitized
        return sanitized

    def _generate_lib_rs(self) -> str:
        """Generate the content for lib.rs"""
        func_name = self._sanitize_name(self.project_name) + "_function"
        test_name = f"test_{self._sanitize_name(self.project_name)}_function"
        
        return f'''pub fn {func_name}() -> String {{
    "Hello, world!".to_string()
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn {test_name}() {{
        let result = {func_name}();
        assert_eq!(result, "Hello, world!");
    }}
}}'''

    def _generate_main_rs(self) -> str:
        """Generate the content for main.rs"""
        return '''fn main() {
    println!("Hello, world!");
}'''

    def _generate_cargo_toml(self) -> str:
        """Generate the content for Cargo.toml"""
        return f'''[package]
name = "{self._sanitize_name(self.project_name)}"
version = "0.1.0"
edition = "2021"

[dependencies]
'''

    def _generate_readme(self) -> str:
        """Generate the content for README.md"""
        return f'''# {self._sanitize_name(self.project_name)}

A Rust library crate.

## Usage

Add this to your `Cargo.toml`:
'''