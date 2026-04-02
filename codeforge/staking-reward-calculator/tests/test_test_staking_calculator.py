import pytest
from src.staking_calculator import StakingCalculator


class TestStakingCalculator:
    def test_calculate_apy_valid_input(self):
        """Test APY calculation with valid inputs"""
        calc = StakingCalculator()
        result = calc.calculate_apy(1000, 1, 0.05)
        assert result == 50.0

    def test_calculate_apy_with_zero_amount(self):
        """Test APY calculation with zero principal"""
        calc = StakingCalculator()
        result = calc.calculate_apy(0, 1, 0.05)
        assert result == 0.0

    def test_calculate_apy_negative_amount(self):
        """Test APY calculation with negative amount should raise ValueError"""
        calc = StakingCalculator()
        with pytest.raises(ValueError):
            calc.calculate_apy(-1000, 1, 0.05)

    def test_calculate_compound_interest_valid(self):
        """Test compound interest calculation with valid inputs"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(1000, 0.05, 2, 1)
        assert round(result, 2) == 102.5  # 1000 * (1 + 0.05)^2 - 1000 = 102.5

    def test_calculate_compound_interest_zero_principal(self):
        """Test compound interest with zero principal"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(0, 0.05, 1, 1)
        assert result == 0.0

    def test_apply_lockup_penalty_valid(self):
        """Test lockup penalty calculation with valid inputs"""
        calc = StakingCalculator()
        result = calc.apply_lockup_penalty(100, 0.1)
        assert result == 90.0

    def test_apply_lockup_penalty_zero_reward(self):
        """Test lockup penalty with zero reward"""
        calc = StakingCalculator()
        result = calc.apply_lockup_penalty(0, 0.1)
        assert result == 0.0

    def test_validate_input_valid(self):
        """Test input validation with valid inputs"""
        calc = StakingCalculator()
        assert calc.validate_input(100) == 100

    def test_validate_input_negative(self):
        """Test input validation with negative input should raise ValueError"""
        calc = StakingCalculator()
        with pytest.raises(ValueError):
            calc.validate_input(-100)

    def test_calculate_apy_zero_time(self):
        """Test APY calculation with zero time period"""
        calc = StakingCalculator()
        result = calc.calculate_apy(1000, 0, 0.05)
        assert result == 0.0

    def test_calculate_compound_interest_zero_rate(self):
        """Test compound interest with zero rate"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(1000, 0, 1, 1)
        assert result == 0.0

    def test_apply_lockup_penalty_no_penalty(self):
        """Test lockup penalty calculation with zero penalty rate"""
        calc = StakingCalculator()
        result = calc.apply_lockup_penalty(100, 0)
        assert result == 100.0

    def test_apply_lockup_penalty_full_penalty(self):
        """Test lockup penalty calculation with 100% penalty"""
        calc = StakingCalculator()
        result = calc.apply_lockup_penalty(100, 1)
        assert result == 0.0

    def test_validate_input_zero(self):
        """Test input validation with zero input"""
        calc = StakingCalculator()
        assert calc.validate_input(0) == 0
        assert calc.validate_input(0.0) == 0.0

    def test_calculate_apy_fractional_inputs(self):
        """Test APY calculation with fractional inputs"""
        calc = StakingCalculator()
        result = calc.calculate_apy(500.5, 1.5, 0.07)
        expected = 500.5 * 1.5 * 0.07
        assert result == expected

    def test_calculate_compound_interest_quarterly(self):
        """Test compound interest with quarterly compounding"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(1500, 0.04, 3, 4)
        assert round(result, 2) == 193.94

    def test_apply_lockup_penalty_half_penalty(self):
        """Test lockup penalty calculation with 50% penalty"""
        calc = StakingCalculator()
        result = calc.apply_lockup_penalty(100, 0.5)
        assert result == 50.0

    def test_validate_input_fractional(self):
        """Test input validation with fractional input"""
        calc = StakingCalculator()
        assert calc.validate_input(1000.5) == 1000.5

    def test_calculate_apy_boundary_conditions(self):
        """Test APY calculation with boundary conditions"""
        calc = StakingCalculator()
        result = calc.calculate_apy(1000, 0, 0.05)
        assert result == 0.0

    def test_calculate_compound_interest_zero_time(self):
        """Test compound interest with zero time period"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(1000, 0.05, 0, 1)
        assert result == 0.0

    def test_compound_interest_zero_compounding(self):
        """Test compound interest with zero compounding frequency"""
        calc = StakingCalculator()
        result = calc.calculate_compound_interest(1000, 0.05, 1, 0)
        assert result == 0.0

    def test_validate_input_edge_cases(self):
        """Test input validation with edge cases"""
        calc = StakingCalculator()
        assert calc.validate_input(0) == 0
        assert calc.validate_input(0.0) == 0.0
        with pytest.raises(ValueError):
            calc.validate_input(-0.1)