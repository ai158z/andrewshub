#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::path::Path;
    use tempfile::TempDir;

    #[test]
    fn test_create_project_success() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("test_project");
        
        let result = create_project("test_project", project_path.to_str().unwrap());
        
        assert!(result.is_ok());
        assert!(project_path.exists());
        assert!(project_path.join("Cargo.toml").exists());
        assert!(project_path.join("src").exists());
        assert!(project_path.join("src").join("main.rs").exists());
    }

    #[test]
    fn test_create_project_with_existing_directory() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("existing_project");
        fs::create_dir_all(&project_path).unwrap();
        
        let result = create_project("existing_project", project_path.to_str().unwrap());
        
        assert!(result.is_ok());
    }

    #[test]
    fn test_create_project_with_invalid_path() {
        let result = create_project("test", "/invalid/path/that/does/not/exist");
        assert!(result.is_err());
    }

    #[test]
    fn test_add_dependency_success() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("dep_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let cargo_toml = project_path.join("Cargo.toml");
        std::fs::write(&cargo_toml, "[package]\nname = \"test\"\nversion = \"0.1.0\"\nedition = \"2021\"\n").unwrap();
        
        let result = add_dependency(project_path.to_str().unwrap(), "serde", "1.0");
        
        assert!(result.is_ok());
        let content = fs::read_to_string(&cargo_toml).unwrap();
        assert!(content.contains("serde = \"1.0\""));
    }

    #[test]
    fn test_add_dependency_to_nonexistent_project() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("nonexistent");
        
        let result = add_dependency(project_path.to_str().unwrap(), "serde", "1.0");
        
        assert!(result.is_err());
    }

    #[test]
    fn test_add_dependency_invalid_toml() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("invalid_toml_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let cargo_toml = project_path.join("Cargo.toml");
        std::fs::write(&cargo_toml, "invalid toml content").unwrap();
        
        let result = add_dependency(project_path.to_str().unwrap(), "serde", "1.0");
        
        assert!(result.is_err());
    }

    #[test]
    fn test_generate_module_success() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("module_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let src_dir = project_path.join("src");
        fs::create_dir_all(&src_dir).unwrap();
        
        let result = generate_module(project_path.to_str().unwrap(), "mymodule");
        
        assert!(result.is_ok());
        assert!(src_dir.join("mymodule.rs").exists());
    }

    #[test]
    fn test_generate_module_creates_file() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("file_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let _ = generate_module(project_path.to_str().unwrap(), "testmod");
        
        let expected_file = project_path.join("src").join("testmod.rs");
        assert!(expected_file.exists());
    }

    #[test]
    fn test_generate_module_with_existing_src() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("existing_src");
        let src_dir = project_path.join("src");
        fs::create_dir_all(&src_dir).unwrap();
        
        std::fs::write(src_dir.join("lib.rs"), "pub mod testmod;").unwrap();
        
        let result = generate_module(project_path.to_str().unwrap(), "testmod");
        
        assert!(result.is_ok());
    }

    #[test]
    fn test_setup_workspace_success() {
        let temp_dir = TempDir::new().unwrap();
        let workspace_path = temp_dir.path().join("workspace_test");
        fs::create_dir_all(&workspace_path).unwrap();
        
        let result = setup_workspace(workspace_path.to_str().unwrap());
        
        assert!(result.is_ok());
        let workspace_cargo = workspace_path.join("Cargo.toml");
        assert!(workspace_cargo.exists());
        let content = fs::read_to_string(&workspace_cargo).unwrap();
        assert!(content.contains("[workspace]"));
    }

    #[test]
    fn test_setup_workspace_with_existing_files() {
        let temp_dir = TempDir::new().unwrap();
        let workspace_path = temp_dir.path().join("existing_workspace");
        fs::create_dir_all(&workspace_path).unwrap();
        
        let cargo_content = "[package]\nname = \"workspace_test\"\nversion = \"0.1.0\"\nedition = \"2021\"\n";
        fs::write(workspace_path.join("Cargo.toml"), cargo_content).unwrap();
        
        let result = setup_workspace(workspace_path.to_str().unwrap());
        
        assert!(result.is_ok());
    }

    #[test]
    fn test_setup_workspace_invalid_path() {
        let result = setup_workspace("/invalid/path");
        assert!(result.is_err());
    }

    #[test]
    fn test_add_workspace_member_success() {
        let temp_dir = TempDir::new().unwrap();
        let workspace_path = temp_dir.path().join("member_test");
        fs::create_dir_all(&workspace_path).unwrap();
        
        let cargo_content = "[workspace]\nmembers = []\n";
        fs::write(workspace_path.join("Cargo.toml"), cargo_content).unwrap();
        
        let result = add_workspace_member(workspace_path.to_str().unwrap(), "new_member");
        
        assert!(result.is_ok());
        let content = fs::read_to_string(workspace_path.join("Cargo.toml")).unwrap();
        assert!(content.contains("new_member"));
    }

    #[test]
    fn test_add_workspace_member_creates_missing_cargo_toml() {
        let temp_dir = TempDir::new().unwrap();
        let workspace_path = temp_dir.path().join("new_member_test");
        fs::create_dir_all(&workspace_path).unwrap();
        
        let result = add_workspace_member(workspace_path.to_str().unwrap(), "another_member");
        
        assert!(result.is_ok());
        assert!(workspace_path.join("Cargo.toml").exists());
    }

    #[test]
    fn test_add_binary_success() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("binary_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let src_dir = project_path.join("src");
        fs::create_dir_all(&src_dir).unwrap();
        
        let result = add_binary(project_path.to_str().unwrap(), "mybin");
        
        assert!(result.is_ok());
        assert!(src_dir.join("bin").exists());
        assert!(src_dir.join("bin").join("mybin.rs").exists());
    }

    #[test]
    fn test_add_binary_creates_src_directory() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("bin_src_test");
        
        let result = add_binary(project_path.to_str().unwrap(), "testbin");
        
        assert!(result.is_ok());
        assert!(project_path.join("src").exists());
    }

    #[test]
    fn test_create_project_with_special_characters() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("special-Project_123");
        
        let result = create_project("special-Project_123", project_path.to_str().unwrap());
        
        assert!(result.is_ok());
        assert!(project_path.exists());
    }

    #[test]
    fn test_add_dependency_empty_version() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("empty_version_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let cargo_toml = project_path.join("Cargo.toml");
        std::fs::write(&cargo_toml, "[package]\nname = \"test\"\nversion = \"0.1.0\"\nedition = \"2021\"\n").unwrap();
        
        let result = add_dependency(project_path.to_str().unwrap(), "serde", "");
        
        assert!(result.is_ok());
        let content = fs::read_to_string(&cargo_toml).unwrap();
        assert!(content.contains("serde = \"\""));
    }

    #[test]
    fn test_generate_module_with_module_name_clash() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("clash_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let src_dir = project_path.join("src");
        fs::create_dir_all(&src_dir).unwrap();
        std::fs::write(src_dir.join("existing.rs"), "").unwrap();
        
        let result = generate_module(project_path.to_str().unwrap(), "existing");
        
        assert!(result.is_ok());
    }

    #[test]
    fn test_add_binary_with_existing_bin_directory() {
        let temp_dir = TempDir::new().unwrap();
        let project_path = temp_dir.path().join("existing_bin_test");
        fs::create_dir_all(&project_path).unwrap();
        
        let bin_dir = project_path.join("src").join("bin");
        fs::create_dir_all(&bin_dir).unwrap();
        
        let result = add_binary(project_path.to_str().unwrap(), "newbin");
        
        assert!(result.is_ok());
        assert!(bin_dir.join("newbin.rs").exists());
    }
}