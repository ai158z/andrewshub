import pytest
from unittest.mock import patch, MagicMock
from src.qkd.protocol import (
    QKDProtocol, BB84Protocol, SARG04Protocol, 
    DecoyStateProtocol, get_qkd_protocol
)

class TestQKDProtocol:
    
    def test_get_qkd_protocol_bb84(self):
        protocol = get_qkd_protocol('BB84')
        assert isinstance(protocol, BB84Protocol)
        
    def test_get_qkd_protocol_sarg04(self):
        protocol = get_qkd_protocol('SARG04')
        assert isinstance(protocol, SARG04Protocol)
        
    def test_get_qkd_protocol_decoy(self):
        protocol = get_qkd_protocol('decoy')
        assert isinstance(protocol, DecoyStateProtocol)
        
    def test_get_qkd_protocol_invalid_type(self):
        with pytest.raises(ValueError):
            get_qkd_protocol('invalid')
            
    def test_bb84_generate_keys_success(self):
        protocol = BB84Protocol()
        key = protocol.generate_keys(32)
        assert len(key) > 0
        
    def test_bb84_generate_keys_with_fallback(self, monkeypatch):
        protocol = BB84Protocol()
        # Mock low fidelity to trigger fallback
        with patch.object(protocol.quantum_channel, 'measure_fidelity', return_value=0.5):
            with patch('src.qkd.key_distribution.generate_random_bytes') as mock_gen:
                mock_gen.return_value = b'fallback_key'
                key = protocol.generate_keys(32)
                assert len(key) > 0
                
    def test_bb84_validate_protocol_success(self):
        protocol = BB84Protocol()
        with patch.object(protocol.quantum_channel, 'measure_fidelity', return_value=0.9):
            with patch.object(protocol.key_distributor, 'verify_key_integrity', return_value=True):
                with patch.object(protocol.edge_auth, 'authenticate_node', return_value=True):
                    assert protocol.validate_protocol() is True
                    
    def test_bb84_validate_protocol_low_fidelity(self):
        protocol = BB84Protocol()
        with patch.object(protocol.quantum_channel, 'measure_fidelity', return_value=0.5):
            result = protocol.validate_protocol()
            assert result is False
            
    def test_sarg04_generate_keys(self):
        protocol = SARG04Protocol()
        key = protocol.generate_keys(32)
        assert len(key) > 0
        
    def test_decoy_generate_keys(self):
        protocol = DecoyStateProtocol()
        key = protocol.generate_keys(32)
        assert len(key) > 0
        
    def test_decoy_validate_protocol(self):
        protocol = DecoyStateProtocol()
        assert protocol.validate_protocol() is True
        
    def test_create_bb84_protocol(self):
        protocol = BB84Protocol()
        assert protocol is not None
        
    def test_create_sarg04_protocol(self):
        protocol = SARG04Protocol()
        assert protocol is not None
        
    def test_create_decoy_protocol(self):
        protocol = DecoyStateProtocol()
        assert protocol is not None

if __name__ == '__main__':
    pytest.main()