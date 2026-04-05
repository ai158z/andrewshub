import os
import logging
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)

def get_rust_structure() -> Dict[str, Any]:
    """
    Returns the directory structure for a Rust project.
    """
    return {
        "src": {
            "bin": {},
            "lib": {}
        },
        "tests": {},
        "benches": {},
        "examples": {},
        "target": {}
    }

def get_rust_files() -> Dict[str, str]:
    """
    Returns the file templates for a Rust project.
    """
    return {
        "src/main.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "src/lib.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "Cargo.toml": """[package]
name = "project"
version = "0.1.0"
edition = "2021"

[dependencies]
""",
        "tests/integration_test.rs": """#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
""",
        "benches/benchmark.rs": """#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
""",
        "examples/example.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "src/bin/main.rs": """fn main() {
    println!("Hello, world!");
}
"""
    }

def get_rust_cargo_toml() -> Dict[str, str]:
    """
    Returns the Cargo.toml template for a Rust project.
    """
    return {
        "Cargo.toml": """[package]
name = "project"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    }

def get_rust_main_rs_template() -> Dict[str, str]:
    """
    Template for main.rs file.
    """
    return {
        "src/main.rs": """fn main() {
    println!("Hello, world!");
}
"""
    }

def get_rust_lib_template() -> Dict[str, str]:
    """
    Template for lib.rs file.
    """
    return {
        "src/lib.rs": """fn main() {
    println!("Hello, world!");
}
"""
    }

def get_rust_cargo_config() -> Dict[str, str]:
    """
    Returns the Cargo configuration for a Rust project.
    """
    return {
        "Cargo.toml": """[package]
name = "project"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    }

def get_rust_structure() -> Dict[str, str]:
    """
    Returns the directory structure for a Rust project.
    """
    return {
        "src": "src",
        "tests": "tests",
        "benches": "benches",
        "examples": "examples",
        "target": "target"
    }

def get_rust_files() -> Dict[str, str]:
    """
    Returns the file templates for a Rust project.
    """
    return {
        "src/main.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "src/lib.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "Cargo.toml": """[package]
name = "project"
version = "0.1.0"
edition = "2021"

[dependencies]
""",
        "tests/integration_test.rs": """#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
""",
        "benches/benchmark.rs": """#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
""",
        "examples/example.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "src/bin/main.rs": """fn main() {
    println!("Hello, world!");
}
"""
    }