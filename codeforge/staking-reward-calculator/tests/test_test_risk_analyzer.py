import pytest
from unittest.mock import patch, MagicMock
from src.risk_analyzer import analyze_network_risk

@pytest.fixture
def mock_network_risks():
    return {
        'solana': {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        },
        'ethereum': {
            'security_score': 9.2,
            'decentralization_score': 8.8,
            'reliability_score': 8.5
        },
        'cardano': {
            'security_score': 8.8,
            'decentralization_score': 9.5,
            'reliability_score': 8.2
        }
    }

def test_analyze_network_risk_valid_network():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        expected_data = {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        }
        mock_get_network_data.return_value = expected_data
        result = analyze_network_risk('solana')
        assert result == expected_data

def test_analyze_network_risk_invalid_network():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = None
        result = analyze_network_risk('nonexistent')
        assert result is None

def test_analyze_network_risk_empty_string():
    result = analyze_network_risk('')
    assert result is None

def test_analyze_network_risk_none_input():
    result = analyze_network_risk(None)
    assert result is None

def test_analyze_network_risk_consistency():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        expected_data = {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        }
        mock_get_network_data.return_value = expected_data
        
        result1 = analyze_network_risk('solana')
        result2 = analyze_network_risk('solana')
        
        assert result1 == expected_data
        assert result2 == expected_data
        assert result1 == result2

def test_risk_score_ranges():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        test_data = {
            'security_score': 10.0,
            'decentralization_score': 5.0,
            'reliability_score': 7.5
        }
        mock_get_network_data.return_value = test_data
        result = analyze_network_risk('test_network')
        
        assert 0 <= result['security_score'] <= 10
        assert 0 <= result['decentralization_score'] <= 10
        assert 0 <= result['reliability_score'] <= 10

def test_network_risk_comparison():
    with patch('src.risk_analyzer.get_network_data') as mock_get_data:
        mock_get_data.return_value = {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        }
        solana_risks = analyze_network_risk('solana')
        
        mock_get_data.return_value = {
            'security_score': 9.2,
            'decentralization_score': 8.8,
            'reliability_score': 8.5
        }
        eth_risks = analyze_network_risk('ethereum')
        
        assert solana_risks is not None
        assert eth_risks is not None

def test_analyze_network_risk_various_networks():
    test_networks = ['solana', 'ethereum', 'cardano', 'unknown_network']
    
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        for network in test_networks:
            if network == 'unknown_network':
                mock_get_network_data.return_value = None
                result = analyze_network_risk(network)
                assert result is None
            else:
                expected_data = {
                    'solana': {
                        'security_score': 8.5,
                        'decentralization_score': 7.2,
                        'reliability_score': 9.1
                    },
                    'ethereum': {
                        'security_score': 9.2,
                        'decentralization_score': 8.8,
                        'reliability_score': 8.5
                    },
                    'cardano': {
                        'security_score': 8.8,
                        'decentralization_score': 9.5,
                        'reliability_score': 8.2
                    }
                }.get(network, {
                    'security_score': 7.0,
                    'decentralization_score': 7.0,
                    'reliability_score': 7.0
                })
                mock_get_network_data.return_value = expected_data
                result = analyze_network_risk(network)
                assert result == expected_data

def test_analyze_network_risks_with_data():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        }
        result = analyze_network_risk('solana')
        assert result is not None

def test_analyze_network_risks_with_no_data():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = None
        result = analyze_network_risk('unknown')
        assert result is None

def test_analyze_network_risk_edge_case_scores():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        # Test with edge case scores
        test_data = {
            'security_score': 0.0,
            'decentralization_score': 10.0,
            'reliability_score': 5.0
        }
        mock_get_network_data.return_value = test_data
        result = analyze_network_risk('test')
        
        assert result['security_score'] == 0.0
        assert result['decentralization_score'] == 10.0
        assert result['reliability_score'] == 5.0

def test_analyze_network_risk_multiple_calls():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        expected_data = {
            'security_score': 9.0,
            'decentralization_score': 8.0,
            'reliability_score': 7.0
        }
        mock_get_network_data.return_value = expected_data
        
        result1 = analyze_network_risk('network1')
        result2 = analyze_network_risk('network1')
        
        assert result1 == result2
        assert result1 == expected_data

def test_analyze_network_risk_different_networks():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = {
            'security_score': 8.0,
            'decentralization_score': 7.0,
            'reliability_score': 9.0
        }
        
        result_a = analyze_network_risk('network_a')
        mock_get_network_data.return_value = {
            'security_score': 7.5,
            'decentralization_score': 8.5,
            'reliability_score': 8.0
        }
        result_b = analyze_network_risk('network_b')
        
        assert result_a != result_b

def test_analyze_network_risk_score_validation():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        test_data = {
            'security_score': 11.0,  # Invalid score > 10
            'decentralization_score': 5.0,
            'reliability_score': -1.0  # Invalid score < 0
        }
        mock_get_network_data.return_value = test_data
        result = analyze_network_risk('test')
        
        # Should still return the data even if scores are out of range
        assert result == test_data

def test_analyze_network_risk_networks():
    networks = ['solana', 'ethereum', 'cardano']
    expected_risks = {
        'solana': {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        },
        'ethereum': {
            'security_score': 9.2,
            'decentralization_score': 8.8,
            'reliability_score': 8.5
        },
        'cardano': {
            'security_score': 8.8,
            'decentralization_score': 9.5,
            'reliability_score': 8.2
        }
    }
    
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        for network, expected in expected_risks.items():
            mock_get_network_data.return_value = expected
            result = analyze_network_risk(network)
            assert result == expected

def test_analyze_network_risk_none_return():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = None
        result = analyze_network_risk('unknown')
        assert result is None

def test_analyze_network_risk_with_none_network_data():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = None
        result = analyze_network_risk('test')
        assert result is None

def test_analyze_network_risk_with_valid_network():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        expected_data = {
            'security_score': 8.5,
            'decentralization_score': 7.2,
            'reliability_score': 9.1
        }
        mock_get_network_data.return_value = expected_data
        result = analyze_network_risk('valid_network')
        assert result == expected_data

def test_analyze_network_risk_with_invalid_scores():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        test_data = {
            'security_score': 15.0,  # Above max
            'decentralization_score': -5.0,  # Below min
            'reliability_score': 7.5
        }
        mock_get_network_data.return_value = test_data
        result = analyze_network_risk('test')
        assert result == test_data  # Should return as-is, no validation in function

def test_analyze_network_risk_network_data_none():
    with patch('src.risk_analyzer.get_network_data') as mock_get_network_data:
        mock_get_network_data.return_value = None
        result = analyze_network_risk('any_network')
        assert result is None