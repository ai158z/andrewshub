# Rust project template
def get_rust_template():
    return {
        "Cargo.toml": """[package]
name = "my_rust_project"
version = "0.1.0"
edition = "2021"

[dependencies]
""",
        "src/main.rs": """fn main() {
    println!("Hello, world!");
}
""",
        "src/lib.rs": """pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }
}
""",
        "tests/integration_test.rs": """#[cfg(test)]
mod tests {
    use my_rust_project::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
"""
    }