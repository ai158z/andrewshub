from unittest.mock import patch, MagicMock
import pytest
from typer.testing import CliRunner
from src.scaffolder.cli import app

runner = CliRunner()

def test_scaffold_valid_project_name():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(app, ["scaffold", "test-project", "--template", "python-cli"])
        assert result.exit_code == 0
        mock_tm.return_value.create_project.assert_called_once()

def test_scaffold_invalid_project_name():
    with patch('src.scaffolder.cli.validate_project_name', return_value=False):
        result = runner.invoke(app, ["scaffold", "invalid/name", "--template", "python-cli"])
        assert result.exit_code == 1
        assert "Invalid project name" in result.stdout

def test_scaffold_dry_run():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True):
        result = runner.invoke(app, ["scaffold", "test-project", "--dry-run"])
        assert result.exit_code == 0
        assert "Dry run: Would create project 'test-project'" in result.stdout

def test_scaffold_with_custom_template():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(app, ["scaffold", "test-project", "--template", "custom-template"])
        assert result.exit_code == 0
        mock_tm.assert_called_once()

def test_list_templates():
    result = runner.invoke(app, ["list-templates"])
    assert result.exit_code == 0
    assert "Available templates:" in result.stdout
    assert "python-cli" in result.stdout
    assert "rust-web" in result.stdout

def test_scaffold_exception_handling():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager', side_effect=Exception("Template error")):
        result = runner.invoke(app, ["scaffold", "test-project"])
        assert result.exit_code == 1
        assert "Error creating project" in result.stdout

def test_scaffold_missing_name():
    result = runner.invoke(app, ["scaffold"])
    assert result.exit_code != 0

def test_main_entry_point():
    with patch('src.scaffolder.cli.app') as mock_app:
        from src.scaffolder.cli import main
        with patch('sys.argv', ['cli.py', 'scaffold', 'test-project']):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.type is SystemExit
            assert e.value.code == 0

def test_scaffold_valid_name_with_pathlike_output_dir():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(app, ["scaffold", "test-project", "--output-dir", "./projects"])
        assert result.exit_code == 0
        mock_tm.return_value.create_project.assert_called_once()

def test_scaffold_valid_name_with_dry_run_and_custom_dir():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True):
        result = runner.invoke(
            app, 
            ["scaffold", "test-project", "--dry-run", "--output-dir", "./test"]
        )
        assert result.exit_code == 0
        assert "Dry run" in result.stdout

def test_scaffold_valid_name_with_all_options():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(
            app, 
            ["scaffold", "test-project", "--template", "python-web", "--output-dir", "./web-projects"]
        )
        assert result.exit_code == 0
        mock_tm.assert_called_once()

def test_scaffold_project_name_with_spaces():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager'):
        result = runner.invoke(app, ["scaffold", "test project"])
        assert result.exit_code == 0

def test_scaffold_empty_project_name():
    with patch('src.scaffolder.cli.validate_project_name', return_value=False):
        result = runner.invoke(app, ["scaffold", ""])
        assert result.exit_code == 1
        assert "Invalid project name" in result.stdout

def test_list_templates_command():
    result = runner.invoke(app, ["list-templates"])
    assert "python-cli: Python CLI application template" in result.stdout
    assert "rust-web: Rust web application template" in result.stdout

def test_scaffold_valid_name_with_invalid_template():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager'):
        result = runner.invoke(app, ["scaffold", "test", "--template", "invalid-template"])
        assert result.exit_code == 0

def test_scaffold_valid_name_with_no_template_specified():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(app, ["scaffold", "test-project"])
        assert result.exit_code == 0
        mock_tm.assert_called_once()

def test_scaffold_project_creation_fails():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        mock_tm.return_value.create_project.side_effect = Exception("Creation failed")
        result = runner.invoke(app, ["scaffold", "test-project"])
        assert result.exit_code == 1

def test_scaffold_valid_name_with_valid_output_dir():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True), \
         patch('src.scaffolder.cli.TemplateManager') as mock_tm:
        result = runner.invoke(app, ["scaffold", "test-project", "--output-dir", "/tmp/projects"])
        assert result.exit_code == 0
        mock_tm.return_value.create_project.assert_called_once()

def test_scaffold_project_with_valid_template_and_dry_run():
    with patch('src.scaffolder.cli.validate_project_name', return_value=True):
        result = runner.invoke(
            app, 
            ["scaffold", "test-project", "--template", "python-cli", "--dry-run"]
        )
        assert result.exit_code == 0
        assert "Dry run: Would create project 'test-project'" in result.stdout

def test_main_function_with_no_args():
    with patch('src.scaffolder.cli.app') as mock_app:
        result = runner.invoke(app, [])
        assert result.exit_code != 0