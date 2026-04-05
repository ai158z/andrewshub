import pytest
from unittest.mock import patch, MagicMock
from src.risk_analyzer import analyze_network_risks, get_network_risk_data

@pytest.fixture
def mock_network_data():
    return {
        "cosmos": {
            "slashing_risk": 0.05,
            "governance_risk": 0.03,
            "market_risk": 0.02,
            "security_risk": 0.01
        }
    }

@pytest.fixture
def mock_network_apy():
    return 12.5

@pytest.fixture
def mock_network_commission():
    return 5.0

def test_get_network_risk_data_known_network():
    result = get_network_risk_data("cosmos")
    assert "slashing_risk" in result
    assert "governance_risk" in result
    assert "market_risk" in result
    assert "security_risk" in result

def test_get_network_risk_data_unknown_network():
    result = get_network_risk_data("unknown")
    assert result["slashing_risk"] == 0.05
    assert result["governance_risk"] == 0.05
    assert result["market_risk"] == 0.05
    assert result["security_risk"] == 0.03

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_high_risk(mock_commission, mock_apy):
    mock_apy.return_value = 15.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.8,
            "governance_risk": 0.7,
            "market_risk": 0.6,
            "security_risk": 0.5
        }
    }):
        result = analyze_network_risks("testnet")
        assert result["risk_level"] == "HIGH"

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_medium_risk(mock_commission, mock_apy):
    mock_apy.return_value = 10.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.5,
            "governance_risk": 0.4,
            "market_risk": 0.3,
            "security_risk": 0.2
        }
    }):
        result = analyze_network_risks("testnet")
        assert result["risk_level"] == "MEDIUM"

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_low_risk(mock_commission, mock_apy):
    mock_apy.return_value = 8.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.2,
            "governance_risk": 0.15,
            "market_risk": 0.1,
            "security_risk": 0.05
        }
    }):
        result = analyze_network_risk("testnet")
        assert result["risk_level"] == "LOW"

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_very_low_risk(mock_commission, mock_apy):
    mock_apy.return_value = 10.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.05,
            "governance_risk": 0.05,
            "market_risk": 0.05,
            "security_risk": 0.03
        }
    }):
        result = analyze_network_risks("testnet")
        assert result["risk_level"] == "VERY_LOW"

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_cosmos(mock_commission, mock_apy):
    mock_apy.return_value = 12.5
    mock_commission.return_value = 5.0
    
    result = analyze_network_risks("cosmos")
    assert result["network"] == "cosmos"
    assert "risk_level" in result
    assert "total_risk_score" in result

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_ethereum(mock_commission, mock_apy):
    mock_apy.return_value = 8.0
    mock_commission.return_value = 5.0
    
    result = analyze_network_risks("ethereum")
    assert result["network"] == "ethereum"
    assert result["risk_level"] in ["HIGH", "MEDIUM", "LOW", "VERY_LOW", "UNKNOWN"]

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_analyze_network_risks_polkadot(mock_commission, mock_apy):
    mock_apy.return_value = 14.0
    mock_commission.return_value = 5.0
    
    result = analyze_network_risks("polkadot")
    assert result["network"] == "polkadot"
    assert "risk_adjusted_apy" in result

def test_analyze_network_risks_unknown_network():
    result = analyze_network_risks("unknown")
    assert result["network"] == "unknown"
    assert result["risk_level"] == "UNKNOWN"

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_risk_adjusted_apy_calculation(mock_commission, mock_apy):
    mock_apy.return_value = 10.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.1,
            "governance_risk": 0.1,
            "market_risk": 0.1,
            "security_risk": 0.1
        }
    }):
        result = analyze_network_risks("testnet")
        expected_risk_score = (0.1 * 0.4) + (0.1 * 0.3) + (0.1 * 0.2) + (0.1 * 0.1)
        assert result["total_risk_score"] == expected_risk_score
        assert result["risk_adjusted_apy"] == 10.0 * (1 - expected_risk_score)

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_network_apy_exception_handling(mock_commission, mock_apy):
    mock_apy.side_effect = Exception("Network error")
    mock_commission.return_value = 5.0
    
    result = analyze_network_risks("testnet")
    assert "error" in result
    assert result["base_apy"] == 0.0

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_network_commission_exception_handling(mock_commission, mock_apy):
    mock_apy.return_value = 10.0
    mock_commission.side_effect = Exception("Commission error")
    
    result = analyze_network_risks("testnet")
    assert result["commission_rate"] == 0.0

def test_risk_score_calculation():
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.2,
            "governance_risk": 0.3,
            "market_risk": 0.1,
            "security_risk": 0.05
        }
    }):
        risk_data = get_network_risk_data("testnet")
        slashing = risk_data["slashing_risk"]
        governance = risk_data["governance_risk"]
        market = risk_data["market_risk"]
        security = risk_data["security_risk"]
        
        expected_score = (slashing * 0.4) + (governance * 0.3) + (market * 0.2) + (security * 0.1)
        result = analyze_network_risks("testnet")
        assert result["total_risk_score"] == expected_score

def test_risk_level_classification():
    test_cases = [
        (0.8, "HIGH"),
        (0.5, "MEDIUM"),
        (0.2, "LOW"),
        (0.05, "VERY_LOW")
    ]
    
    for score, expected_level in test_cases:
        with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
            "testnet": {
                "slashing_risk": score,
                "governance_risk": score,
                "market_risk": score,
                "security_risk": score
            }
        }):
            result = analyze_network_risks("testnet")
            assert result["risk_level"] == expected_level

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_potential_losses_calculation(mock_commission, mock_apy):
    mock_apy.return_value = 10.0
    mock_commission.return_value = 5.0
    
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.1,
            "governance_risk": 0.05,
            "market_risk": 0.03,
            "security_risk": 0.02
        }
    }):
        result = analyze_network_risks("testnet")
        assert "potential_losses" in result
        losses = result["potential_losses"]
        assert losses["annual_slashing"] == 10.0 * 0.1
        assert losses["annual_governance_loss"] == 10.0 * 0.05
        assert losses["annual_market_loss"] == 10.0 * 0.03
        assert losses["annual_security_loss"] == 10.0 * 0.02

def test_risk_report_structure():
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.1,
            "governance_risk": 0.05,
            "market_risk": 0.03,
            "security_risk": 0.02
        }
    }):
        result = analyze_network_risks("testnet")
        expected_keys = [
            "network", "risk_level", "total_risk_score", "base_apy",
            "risk_adjusted_apy", "commission_rate", "risk_breakdown",
            "potential_losses", "recommendations"
        ]
        for key in expected_keys:
            assert key in result

def test_risk_report_risk_breakdown():
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.1,
            "governance_risk": 0.05,
            "market_risk": 0.03,
            "security_risk": 0.02
        }
    }):
        result = analyze_network_risks("testnet")
        breakdown = result["risk_breakdown"]
        assert breakdown["slashing_risk"] == 0.1
        assert breakdown["governance_risk"] == 0.05
        assert breakdown["market_risk"] == 0.03
        assert breakdown["security_risk"] == 0.02

def test_risk_report_recommendations():
    with patch('src.risk_analyzer.NETWORK_RISK_DATA', {
        "testnet": {
            "slashing_risk": 0.8,
            "governance_risk": 0.7,
            "market_risk": 0.6,
            "security_risk": 0.5
        }
    }):
        result = analyze_network_risks("testnet")
        assert len(result["recommendations"]) > 0
        assert "Consider diversifying" in result["recommendations"][0]

@patch('src.risk_analyzer.get_network_apy')
@patch('src.risk_analyzer.get_network_commission')
def test_network_data_error_handling(mock_commission, mock_apy):
    mock_apy.side_effect = Exception("API error")
    mock_commission.return_value = 0.0
    
    result = analyze_network_risks("testnet")
    assert result["error"] is not None
    assert result["risk_level"] == "UNKNOWN"