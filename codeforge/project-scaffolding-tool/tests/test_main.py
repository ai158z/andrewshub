from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner
from src.main import main

def test_main_with_valid_inputs():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'python' generated successfully!" in result.output

def test_main_with_invalid_project_type():
    runner = CliRunner()
    result = runner.invoke(main, ['--name', 'invalid', '--type', 'invalid'])
    assert result.exit_code == 2

def test_main_with_no_name():
    runner = CliRunner()
    result = runner.invoke(main, ['--type', 'python'])
    assert result.exit_code == 2

def test_main_with_valid_framework():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python', '--framework', 'django'])
        assert result.exit_code == 0

def test_main_with_no_framework():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'python' generated successfully!" in result.output

def test_main_with_exception():
    runner = CliRunner()
    with patch('src.main.generate_project', side_effect=Exception("Generation failed")):
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python'])
        assert result.exit_code == 1
        assert "Error generating project: Generation failed" in result.output

def test_main_with_valid_inputs_javascript():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'javascript'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'javascript' generated successfully!" in result.output

def test_main_with_valid_inputs_rust():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'rust'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'rust' generated successfully!" in result.output

def test_main_with_framework_and_python():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python', '--framework', 'django'])
        assert result.exit_code == 0

def test_main_with_framework_and_javascript():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'javascript', '--framework', 'react'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'javascript' generated successfully!" in result.output

def test_main_with_framework_and_rust():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'rust', '--framework', 'actix'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'rust' generated successfully!" in result.output

def test_main_missing_required_options():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 2

def test_main_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert '--name' in result.output
    assert '--type' in result.output

def test_main_invalid_option():
    runner = CliRunner()
    result = runner.invoke(main, ['--invalid', 'option'])
    assert result.exit_code == 2

def test_main_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0

def test_main_with_valid_type_no_framework():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, ['--name', 'test_project', '--type', 'python'])
        assert result.exit_code == 0
        assert "Project 'test_project' of type 'python' generated successfully!" in result.output

def test_main_with_prompt_inputs():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, input='test_project\npython\n')
        assert result.exit_code == 0

def test_main_with_prompt_inputs_and_framework():
    runner = CliRunner()
    with patch('src.main.generate_project') as mock_generate:
        result = runner.invoke(main, input='test_project\npython\n')
        assert result.exit_code == 0