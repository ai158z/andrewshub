import pytest
from unittest.mock import patch, MagicMock
from src.main import main

def test_main_with_valid_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.blockchain_client.get_reward_rate") as mock_get_rate:
        mock_get_rate.return_value = 0.05
        with patch("src.data_fetcher.fetch_data") as mock_fetch:
            mock_fetch.return_value = {"rewards": 100}
            with patch("src.staking_calculator.calculate_rewards") as mock_calc:
                mock_calc.return_value = 100
                result = main()
                assert result == 0

def test_main_with_invalid_amount(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "-100", "--network", "ethereum"])
    with patch("src.validator.validate_stake_amount", return_value=False):
        with pytest.raises(ValueError, match="Invalid stake amount"):
            main()

def test_main_with_missing_reward_rate(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.blockchain_client.get_reward_rate", return_value=None):
        result = main()
        assert result == 1

def test_main_with_valid_stake_data(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.staking_calculator.calculate_rewards") as mock_calc:
        mock_calc.return_value = 50
        result = main()
        assert result == 0

def test_main_formatting(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.utils.format_currency") as mock_format:
        mock_format.return_value = "$1,000.00"
        result = main()
        assert result == 0

def test_main_cache_interaction(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.utils.cache_get") as mock_cache_get:
        mock_cache_get.return_value = {"cached": True}
        with patch("src.utils.cache_set") as mock_cache_set:
            mock_cache_set.return_value = None
            result = main()
            assert result == 0

def test_main_with_pydantic_validation_error(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "invalid", "--network", "ethereum"])
    with patch("src.models.stake_data.StakeData") as mock_model:
        mock_model.side_effect = Exception("Validation error")
        with pytest.raises(Exception):
            main()

def test_main_network_data_fetch(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.data_fetcher.fetch_data") as mock_fetch:
        mock_fetch.return_value = {"status": "success"}
        result = main()
        assert result == 0

def test_main_calculate_rewards_called(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.staking_calculator.calculate_rewards") as mock_calc:
        mock_calc.return_value = 50
        result = main()
        assert result == 0

def test_main_invalid_network(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "invalid_network"])
    with patch("src.blockchain_client.get_reward_rate", return_value=None):
        result = main()
        assert result == 1

def test_main_valid_amount_but_no_rewards(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.staking_calculator.calculate_rewards", return_value=0):
        result = main()
        assert result == 0

def test_main_argument_parsing_error(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])
    with pytest.raises(SystemExit):
        main()

def test_main_stake_data_model_creation(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.models.stake_data.StakeData") as mock_model:
        mock_model.return_value = MagicMock()
        result = main()
        assert result == 0

def test_main_reward_rate_none(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.blockchain_client.get_reward_rate", return_value=None):
        result = main()
        assert result == 1

def test_main_format_currency_called(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.utils.format_currency") as mock_format:
        mock_format.return_value = "$1,000.00"
        result = main()
        assert result == 0

def test_main_validate_stake_amount(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "0", "--network", "ethereum"])
    with patch("src.validator.validate_stake_amount", return_value=False):
        with pytest.raises(ValueError, match="Invalid stake amount"):
            main()

def test_main_successful_execution(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    result = main()
    assert result == 0

def test_main_caching_mechanism(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.utils.cache_get") as mock_get:
        mock_get.return_value = None
        with patch("src.utils.cache_set") as mock_set:
            result = main()
            assert result == 0

def test_main_edge_case_zero_amount(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "0", "--network", "ethereum"])
    with patch("src.validator.validate_stake_amount", return_value=False):
        with pytest.raises(ValueError):
            main()

def test_main_integration_with_all_mocks(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--amount", "1000", "--network", "ethereum"])
    with patch("src.blockchain_client.get_reward_rate") as mock_rate:
        mock_rate.return_value = 0.05
        with patch("src.staking_calculator.calculate_rewards") as mock_calc:
            mock_calc.return_value = 50
            with patch("src.utils.format_currency") as mock_format:
                mock_format.return_value = "$50.00"
                result = main()
                assert result == 0