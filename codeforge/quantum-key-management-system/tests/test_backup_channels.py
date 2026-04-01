import pytest
from unittest.mock import patch, MagicMock
from src.fallback.backup_channels import BackupChannel
import io
import json

def test_backup_channel_initialization():
    with patch("src.fallback.backup_channels.BackupChannel") as mock_backup:
        mock_backup.__init__ = MagicMock()

@pytest.mark.simple
def test_switch_to_classical(backup_channel):
    result = backup_channel.switch_to_classical()
    assert result['status'] == 'success'
    assert result['channel'] == 'classical'

def test_restore_quantum_channel(backup_channel):
    result = backup_channel.restore_quantum_channel()
    assert result['status'] == 'success'
    assert result['channel'] == 'quantum'

def test_switch_to_classical_returns_dict():
    result = backup_channel.switch_to_classical()
    assert isinstance(result, dict)

def test_restore_quantum_channel():
    result = backup_channel.restore_quantum_channel()
    assert isinstance(result, dict)

def test_restore_quantum_channel_success():
    result = backup_channel.restore_quantum_channel()
    assert result['status'] == 'success'
    assert result['channel'] == 'quantum'

def test_classical_fallback():
    # Test the classical fallback functionality
    result = backup_channel.classical_fallback()
    assert result['status'] == 'success'
    assert result['channel'] == 'classical'