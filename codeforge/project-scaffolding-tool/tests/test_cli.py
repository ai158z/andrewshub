import pytest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
from click.testing import CliRunner
from src.scaffolding.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_all_options(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'test', '--template', 'python'])
    assert result.exit_code == 0
    assert "Project test created successfully" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_prompts_for_missing_project_name(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--template', 'python'])
    assert result.exit_code == 0
    assert "created successfully" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_prompts_for_missing_template(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'test'])
    assert result.exit_code == 0
    assert "created successfully" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_uses_config_when_no_cli_args(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {
        'project_name': 'config_project',
        'template': 'python'
    }
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "config_project" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_config_file(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    with runner.isolated_filesystem():
        with open('test_config.json', 'w') as f:
            json.dump({'project_name': 'config_test', 'template': 'python'}, f)
        
        result = runner.invoke(main, ['--config', 'test_config.json'])
        assert result.exit_code == 0
        assert "config_test" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_invalid_template_fails(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'test', '--template', 'invalid'])
    assert result.exit_code == 2
    assert "Error: Invalid value" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_javascript_template(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'js_test', '--template', 'javascript'])
    assert result.exit_code == 0
    assert "js_test" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_web_template(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'web_test', '--template', 'web'])
    assert result.exit_code == 0
    assert "web_test" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_library_template(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'lib_test', '--template', 'library'])
    assert result.exit_code == 0
    assert "lib_test" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_saves_config_after_run(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'config_save_test', '--template', 'python'])
    assert result.exit_code == 0
    mock_save_config.assert_called_once()


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_creates_project_directory(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, ['--project-name', 'dir_test', '--template', 'python'])
    assert result.exit_code == 0
    mock_makedirs.assert_called()


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_handles_exception_gracefully(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    mock_makedirs.side_effect = Exception("Test error")
    
    result = runner.invoke(main, ['--project-name', 'error_test', '--template', 'python'])
    assert result.exit_code == 1
    assert "Error creating project" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_help_option(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_no_args_prompts_for_input(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Enter project name" in result.output


@patch('src.scaffolding.cli.os.makedirs')
@patch('src.scaffolding.cli.write_file')
@patch('src.scaffolding.cli.get_project_config')
@patch('src.scaffolding.cli.save_config')
def test_main_with_valid_config_file(mock_save_config, mock_get_config, mock_write_file, mock_makedirs, runner):
    mock_get_config.return_value = {}
    with runner.isolated_filesystem():
        config_data = {'project_name': 'config_file_test', 'template': 'python'}
        
        with open('temp_config.json', 'w') as f:
            json.dump(config_data, f)
            
        result = runner.invoke(main, ['--config', 'temp_config.json'])
        assert result.exit_code == 0
        assert "config_file_test" in result.output