import pytest
from unittest.mock import patch, MagicMock, ANY
import os
from backend.src.utils.github_webhook import verify_signature, handle_push_event
import hashlib
import hmac

@pytest.fixture
def valid_payload():
    return b'{"ref":"refs/heads/main","repository":{"id":123456,"name":"test-repo","html_url":"https://github.com/test/test-repo","owner":{"login":"test-owner"}}}'

@pytest.fixture
def invalid_payload():
    return b'{"repository":{}}'

def test_verify_signature_valid():
    secret = "test-secret"
    payload = b"test payload"
    expected_signature = "sha256=" + hmac.new(
        key=secret.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    with patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": secret}):
        assert verify_signature(payload, expected_signature) is True

def test_verify_signature_invalid():
    secret = "test-secret"
    payload = b"test payload"
    invalid_signature = "sha256=invalid"
    
    with patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": secret}):
        assert verify_signature(payload, invalid_signature) is False

def test_verify_signature_missing_secret():
    with patch.dict(os.environ, {}, clear=True):
        assert verify_signature(b"test", "sha256=test") is False

def test_verify_signature_exception_handling():
    with patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": "test"}):
        with patch("hmac.new", side_effect=Exception("test error")):
            result = verify_signature(b"test", "sha256=test")
            assert result is False

def test_handle_push_event_valid(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id')
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_sync_repo = mocker.patch('backend.src.api.routes.repositories.sync_repository')
    mock_run_analysis = mocker.patch('backend.src.services.code_analyzer.run_analysis')
    
    mock_get_repo.return_value = MagicMock()
    mock_add_repo.return_value = MagicMock()
    
    handle_push_event(valid_payload)
    
    mock_sync_repo.assert_called_once()
    mock_run_analysis.assert_called_once()

def test_handle_push_event_repository_not_found(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id')
    mock_get_repo.return_value = None
    
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_sync_repo = mocker.patch('backend.src.api.routes.repositories.sync_repository')
    mock_run_analysis = mocker.patch('backend.src.services.code_analyzer.run_analysis')
    
    mock_repo = MagicMock()
    mock_add_repo.return_value = mock_repo
    
    handle_push_event(valid_payload)
    
    mock_add_repo.assert_called_once()
    mock_sync_repo.assert_called_once()
    mock_run_analysis.assert_called_once()

def test_handle_push_event_invalid_payload(mocker, invalid_payload):
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event(invalid_payload)
    mock_logger.warning.assert_called_with("Invalid repository data in push event")

def test_handle_push_event_exception_handling(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id', side_effect=Exception("Database error"))
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    
    with pytest.raises(Exception):
        handle_push_event(valid_payload)
    
    mock_logger.error.assert_called()

def test_handle_push_event_missing_repository_data(mocker):
    payload = b'{"ref":"refs/heads/main"}'
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event(payload)
    mock_logger.warning.assert_called_with("Invalid repository data in push event")

def test_handle_push_event_empty_payload(mocker):
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event({})
    mock_logger.warning.assert_called_with("Invalid repository data in push event")

def test_handle_push_event_repository_add_fails(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id')
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_add_repo.return_value = None
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    
    mock_get_repo.return_value = None
    handle_push_event(valid_payload)
    
    mock_logger.error.assert_called()

def test_handle_push_event_sync_fails(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by1111111111111111id')
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_sync_repo = mocker.patch('backend.src.api.routes.repositories.sync_repository', side_effect=Exception("Sync failed"))
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    
    mock_repo = MagicMock()
    mock_add_repo.return_value = mock_repo
    mock_get_repo.return_value = mock_repo
    
    with pytest.raises(Exception):
        handle_push_event(valid_payload)
        
    assert "Error handling push event" in str(mock_logger.error.call_args[0][0])

def test_verify_signature_empty_payload():
    secret = "test-secret"
    with patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": secret}):
        signature = "sha256=" + hmac.new(
            key=secret.encode('utf-8'),
            msg=b"",
            digestmod=hashlib.sha256
        ).hexdigest()
        assert verify_signature(b"", signature) is True

def test_verify_signature_unicode_payload():
    secret = "test-secret-unicode"
    payload = "测试数据".encode('utf-8')
    with patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": secret}):
        signature = "sha256=" + hmac.new(
            key=secret.encode('utf-8'),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        assert verify_signature(payload, signature) is True

def test_handle_push_event_with_full_repo_data(mocker):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id')
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_sync_repo = mocker.patch('backend.src.api.routes.repositories.sync_repository')
    mock_run_analysis = mocker.patch('backend.src.services.code_analyzer.run_analysis')
    
    mock_get_repo.return_value = None
    mock_repo = MagicMock()
    mock_add_repo.return_value = mock_repo
    
    payload = {
        "repository": {
            "id": "123",
            "name": "test",
            "html_url": "http://test.com",
            "owner": {"login": "test"}
        }
    }
    
    handle_push_event(payload)
    mock_add_repo.assert_called_once()
    mock_sync_repo.assert_called_once_with("123")
    mock_run_analysis.assert_called_once()

def test_handle_push_event_no_repository(mocker):
    payload = {"ref": "refs/heads/main"}
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event(payload)
    mock_logger.warning.assert_called_with("Invalid repository data in push event")

def test_handle_push_event_exception_in_run_analysis(mocker, valid_payload):
    mock_get_repo = mocker.patch('backend.src.utils.github_webhook.get_repository_by_id')
    mock_add_repo = mocker.patch('backend.src.api.routes.repositories.add_repository')
    mock_sync_repo = mocker.patch('backend.src.api.routes.repositories.sync_repository')
    mock_run_analysis = mocker.patch('backend.src.services.code_analyzer.run_analysis', 
                                 side_effect=Exception("Analysis error"))
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    
    mock_get_repo.return_value = MagicMock()
    
    with pytest.raises(Exception):
        handle_push_event(valid_payload)

def test_handle_push_event_with_no_repository_id(mocker):
    payload = {
        "ref": "refs/heads/main",
        "repository": {
            "name": "test"
        }
    }
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event(payload)
    mock_logger.warning.assert_called_with("Invalid repository data in push event")

def test_handle_push_event_with_no_repository_name(mocker):
    payload = {
        "ref": "refs/heads/main",
        "repository": {
            "id": "123",
            "owner": {"login": "test"}
        }
    }
    mock_logger = mocker.patch('backend.src.utils.github_webhook.logger')
    handle_push_event(payload)
    mock_logger.warning.assert_called_with("Invalid repository data in push event")