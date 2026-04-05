import pytest
from unittest.mock import mock_open, patch
from src.scaffolder.templates.rust import RustTemplate

def test_rust_template_generation():
    """Test that Rust template generates correct file structure"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    assert "src/main.rs" in files
    assert "src/lib.rs" in files
    assert "Cargo.toml" in files
    assert "README.md" in files

def test_rust_template_lib_content():
    """Test that lib.rs template contains expected content"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    expected_content = '''pub fn test_project_function() -> String {
    "Hello, world!".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_test_project_function() {
        let result = test_project_function();
        assert_eq!(result, "Hello, world!");
    }
}'''
    
    assert files["src/lib.rs"] == expected_content

def test_rust_template_cargo_toml_content():
    """Test that Cargo.toml has correct project configuration"""
    template = RustTemplate("my_crate")
    files = template.generate()
    
    expected_content = '''[package]
name = "my_crate"
version = "0.1.0"
edition = "2021"

[dependencies]
'''
    
    assert files["Cargo.toml"] == expected_content

def test_rust_template_readme_content():
    """Test that README.md has correct project name"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    expected_header = "# test_project"
    assert files["README.md"].startswith(expected_header)

def test_rust_template_main_content():
    """Test that main.rs has correct hello world function"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    expected_content = '''fn main() {
    println!("Hello, world!");
}'''
    
    assert files["src/main.rs"] == expected_content

def test_rust_template_invalid_project_name():
    """Test that invalid project names raise appropriate errors"""
    with pytest.raises(ValueError):
        RustTemplate("")  # Empty name
        
    with pytest.raises(ValueError):
        RustTemplate("123invalid")  # Starts with number
        
    with pytest.raises(ValueError):
        RustTemplate("invalid-name")  # Contains hyphen

def test_rust_template_valid_project_name():
    """Test that valid project names work correctly"""
    valid_names = ["hello", "my_crate", "test123", "snake_case"]
    
    for name in valid_names:
        template = RustTemplate(name)
        files = template.generate()
        assert f"fn {name}_function()" in files["src/lib.rs"]

def test_rust_template_project_name_sanitization():
    """Test that project names are properly sanitized"""
    # Test special characters are handled
    template = RustTemplate("test-project.name")
    files = template.generate()
    
    # Should generate valid Rust function names
    assert "test_project_name_function" in files["src/lib.rs"]

def test_rust_template_file_structure():
    """Test that all required Rust files are generated"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    required_files = ["Cargo.toml", "src/main.rs", "src/lib.rs", "README.md"]
    for file in required_files:
        assert file in files

def test_rust_template_cargo_toml_validation():
    """Test that Cargo.toml contains all required fields"""
    template = RustTemplate("test_crate")
    files = template.generate()
    
    cargo_content = files["Cargo.toml"]
    assert "[package]" in cargo_content
    assert "name = \"test_crate\"" in cargo_content
    assert "edition = \"2021\"" in cargo_content

def test_rust_template_function_naming():
    """Test that function names use correct project name"""
    template = RustTemplate("my_awesome_project")
    files = template.generate()
    
    lib_content = files["src/lib.rs"]
    assert "pub fn my_awesome_project_function()" in lib_content

def test_rust_template_test_module():
    """Test that test modules are generated correctly"""
    template = RustTemplate("test_project")
    files = template.generate()
    
    lib_content = files["src/lib.rs"]
    assert "#[cfg(test)]" in lib_content
    assert 'fn test_test_project_function()' in lib_content

def test_rust_template_main_function():
    """Test that main function is generated correctly"""
    template = RustTemplate("hello_world")
    files = template.generate()
    
    main_content = files["src/main.rs"]
    assert 'fn main() {' in main_content
    assert 'println!("Hello, world!");' in main_content

def test_rust_template_multiple_instances():
    """Test that multiple template instances don't interfere"""
    template1 = RustTemplate("project1")
    template2 = RustTemplate("project2")
    
    files1 = template1.generate()
    files2 = template2.generate()
    
    # Each should have their own distinct content
    assert "project1_function" in files1["src/lib.rs"]
    assert "project2_function" in files2["src/lib.rs"]
    
    assert "project1_function" not in files2["src/lib.rs"]
    assert "project2_function" not in files1["src/lib.rs"]