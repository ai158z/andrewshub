import pytest
import sys
from src.cli_parser import parse_args, display_menu
from unittest.mock import patch, MagicMock

def test_parse_args_default_values():
    """Test that parse_args returns expected default values when no arguments provided."""
    sys.argv = ['']
    args = parse_args()
    assert args.config == "config.yaml"
    assert args.db_path == "data.db"
    assert not args.add_feed
    assert not args.list_feeds
    assert not args.moonpay_alerts
    assert not args.test_mode

def test_parse_args_with_config():
    """Test parsing with custom config file."""
    sys.argv = ['--config', 'custom_config.yaml']
    args = parse_args()
    assert args.config == "custom_config.yaml"

def test_parse_args_with_db_path():
    """Test parsing with custom database path."""
    sys.argv = ['--db-path', 'custom.db']
    args = parse_args()
    assert args.db_path == "custom.db"

def test_parse_args_add_feed():
    """Test the add-feed argument."""
    sys.argv = ['--add-feed', 'http://example.com/feed']
    args = parse_args()
    assert args.add_feed == "http://example.com/feed"

def test_parse_args_list_feeds():
    """Test the list-feeds argument."""
    sys.argv = ['--list-feeds']
    args = parse_args()
    assert args.list_feeds

def test_parse_args_test_mode():
    """Test the test-mode argument."""
    sys.argv = ['--test-mode']
    args = parse_args()
    assert args.test_mode

def test_parse_args_moonpay_alerts():
    """Test the moonpay-alerts argument."""
    sys.argv = ['--moonpay-alerts']
    args = parse_args()
    assert args.moonpay_alerts

def test_parse_args_all_flags():
    """Test all flags can be parsed."""
    sys.argv = ['--add-feed', 'http://example.com/feed', '--list-feeds', '--test-mode', '--moonpay-alerts']
    args = parse_args()
    assert args.add_feed == "http://example.com/feed"
    assert args.list_feeds
    assert args.test_mode
    assert args.moonpay_alerts

def test_display_menu_valid_selection():
    """Test that display_menu returns a valid selection."""
    options = ["Option 1", "Option 2", "Option 3"]
    choice = display_menu(options)
    assert choice == "Option 2"

def test_parse_args_invalid_url():
    """Test with an invalid URL argument."""
    sys.argv = ['--add-feed', 'invalid_url']
    with pytest.raises(SystemExit):
        args = parse_args()

def test_parse_args_help():
    """Test help message."""
    sys.argv = ['--help']
    with pytest.raises(SystemExit):
        parse_args()

def test_parse_args_version():
    """Test version argument."""
    sys.argv = ['--version']
    with pytest.raises(SystemExit):
        args = parse_args()

def test_display_menu_empty_options():
    """Test display_menu with empty options."""
    with pytest.raises(ValueError, match="Menu options cannot be empty"):
        display_menu([])

def test_display_menu_user_input(mocker):
    """Test user input handling in display_menu."""
    # Mock the input to simulate user typing "2"
    with patch('builtins.input', return_value='2') as mock_input:
        options = ["Option 1", "Option 2", "Option 3"]
        selected = display_menu(options)
        assert selected == "Option 2"

def test_display_menu_valid_range():
    """Test valid range for display_menu selection."""
    options = ["Option 1", "Option 2", "Option 3"]
    # Simulate user selection
    with patch('builtins.input', return_value='2'):
        selected = display_menu(options)
        assert selected == "Option 2"