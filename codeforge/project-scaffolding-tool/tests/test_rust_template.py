import pytest
from src.templates.rust_template import (
    get_rust_structure, 
    get_rust_files, 
    get_rust_cargo_toml, 
    get_rust_main_rs_template, 
    get_rust_lib_template, 
    get_rust_cargo_config
)

class TestRustTemplate:
    def test_get_rust_structure_returns_dict(self):
        result = get_rust_structure()
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_rust_files_returns_dict(self):
        result = get_rust_files()
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_rust_cargo_toml_returns_dict(self):
        result = get_rust_cargo_toml()
        assert isinstance(result, dict)
        assert "Cargo.toml" in result

    def test_get_rust_main_rs_template_returns_dict(self):
        result = get_rust_main_rs_template()
        assert isinstance(result, dict)
        assert "src/main.rs" in result

    def test_get_rust_lib_template_returns_dict(self):
        result = get_rust_lib_template()
        assert isinstance(result, dict)
        assert "src/lib.rs" in result

    def test_get_rust_cargo_config_returns_dict(self):
        result = get_rust_cargo_config()
        assert isinstance(result, dict)
        assert "Cargo.toml" in result

    def test_get_rust_structure_has_required_directories(self):
        result = get_rust_structure()
        required_dirs = ["src", "tests", "benches", "examples", "target"]
        for dir_name in required_dirs:
            assert dir_name in result

    def test_get_rust_files_contains_all_expected_files(self):
        result = get_rust_files()
        expected_files = [
            "src/main.rs", "src/lib.rs", "Cargo.toml", 
            "tests/integration_test.rs", "benches/benchmark.rs", 
            "examples/example.rs", "src/bin/main.rs"
        ]
        for file in expected_files:
            assert file in result

    def test_get_rust_files_cargo_toml_content(self):
        result = get_rust_cargo_toml()
        assert "Cargo.toml" in result
        content = result["Cargo.toml"]
        assert "[package]" in content
        assert "name = \"project\"" in content
        assert "version = \"0.1.0\"" in content
        assert "edition = \"2021\"" in content

    def test_get_rust_main_rs_template_content(self):
        result = get_rust_main_rs_template()
        assert "src/main.rs" in result
        content = result["src/main.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content

    def test_get_rust_lib_template_content(self):
        result = get_rust_lib_template()
        assert "src/lib.rs" in result
        content = result["src/lib.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content

    def test_get_rust_cargo_config_content(self):
        result = get_rust_cargo_config()
        assert "Cargo.toml" in result
        content = result["Cargo.toml"]
        assert "[package]" in content
        assert "name = \"project\"" in content
        assert "version = \"0.1.0\"" in content
        assert "edition = \"2021\"" in content

    def test_get_rust_structure_keys_match_values(self):
        result = get_rust_structure()
        for key, value in result.items():
            assert key == value

    def test_get_rust_files_integration_test_content(self):
        result = get_rust_files()
        content = result["tests/integration_test.rs"]
        assert "#[cfg(test)]" in content
        assert "mod tests {" in content
        assert "#[test]" in content
        assert "assert_eq!(2 + 2, 4)" in content

    def test_get_rust_files_benchmark_content(self):
        result = get_rust_files()
        content = result["benches/benchmark.rs"]
        assert "#[cfg(test)]" in content
        assert "mod tests {" in content
        assert "#[test]" in content
        assert "assert_eq!(2 + 2, 4)" in content

    def test_get_rust_files_example_content(self):
        result = get_rust_files()
        content = result["examples/example.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content

    def test_get_rust_files_bin_main_content(self):
        result = get_rust_files()
        content = result["src/bin/main.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content

    def test_get_rust_files_main_rs_content(self):
        result = get_rust_files()
        content = result["src/main.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content

    def test_get_rust_files_lib_rs_content(self):
        result = get_rust_files()
        content = result["src/lib.rs"]
        assert "fn main() {" in content
        assert "println!(\"Hello, world!\");" in content