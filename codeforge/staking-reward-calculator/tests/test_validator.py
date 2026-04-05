import pytest
from src.validator import validate_stake_amount

class TestValidateStakeAmount:
    def test_valid_positive_amount(self):
        assert validate_stake_amount(1000.0) == True

    def test_zero_amount_fails(self):
        assert validate_stake_amount(0) == False

    def test_negative_amount_fails(self):
        assert validate_stake_amount(-100) == False

    def test_amount_exceeding_max_fails(self):
        assert validate_stake_amount(1000001) == False

    def test_amount_at_max_succeeds(self):
        assert validate_stake_amount(1000000) == True

    def test_amount_just_below_max_succeeds(self):
        assert validate_stake_amount(999999) == True

    def test_string_amount_fails(self):
        assert validate_stake_amount("1000") == False

    def test_string_amount_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount("invalid")
        assert "Stake amount must be a number" in caplog.messages
        assert result == False

    def test_none_amount_fails(self):
        assert validate_stake_amount(None) == False

    def test_boolean_amount_fails(self):
        assert validate_stake_amount(True) == False

    def test_float_amount_succeeds(self):
        assert validate_stake_amount(1500.5) == True

    def test_integer_amount_succeeds(self):
        assert validate_stake_amount(50000) == True

    def test_exact_zero_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(0)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_negative_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(-10)
        assert "Stake amount must be positive" in caplog.messages
        assert result == False

    def test_exceeding_max_logs_error(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1000001)
        assert "Stake amount exceeds maximum allowed value" in caplog.messages
        assert result == False

    def test_valid_amount_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(5000)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_float_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(1500.5)
        assert len(caplog.messages) == 0
        assert result == True

    def test_valid_integer_no_log_output(self, caplog):
        with caplog.at_level("ERROR"):
            result = validate_stake_amount(50000)
        assert len(caplog.messages) == 0
        assert result == True