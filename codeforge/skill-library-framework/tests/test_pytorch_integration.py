import pytest
import torch
import numpy as np
from unittest.mock import patch, MagicMock, mock_open
import json
from pathlib import Path

from src.skill_library.integrations.pytorch_integration import PyTorchIntegration

def test_init_with_cpu_fallback():
    with patch('torch.cuda.is_available', return_value=False):
        integration = PyTorchIntegration()
        assert integration.device.type == 'cpu'

def test_init_with_cuda_when_available():
    with patch('torch.cuda.is_available', return_value=True):
        integration = PyTorchIntegration()
        assert integration.device.type == 'cuda'

def test_load_model_from_pt_file(tmp_path):
    model_path = tmp_path / "model.pt"
    model_path.write_text("dummy")
    
    with patch('torch.load') as mock_load:
        integration = PyTorchIntegration(str(model_path))
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        
        integration.load_model()
        mock_load.assert_called_once()
        assert integration._model_loaded is True

def test_load_model_from_directory_structure(tmp_path):
    model_dir = tmp_path / "model"
    model_dir.mkdir()
    model_file = model_dir / "model.pth"
    model_file.write_text("model_data")
    
    config = {"model_class": "PyTorchModel", "input_dim": 10, "output_dim": 5}
    config_file = model_dir / "config.json"
    config_file.write_text(json.dumps(config))
    
    with patch('torch.load') as mock_load, \
         patch('torch.nn.Linear') as mock_linear:
        mock_linear.return_value = MagicMock()
        mock_load.return_value = MagicMock()
        
        integration = PyTorchIntegration(str(model_dir))
        integration.load_model()
        
        assert mock_load.call_count == 1
        assert integration._model_loaded is True

def test_load_model_from_config():
    config = {
        "model_class": "PyTorchModel",
        "input_dim": 10,
        "output_dim": 5,
        "model_path": "/fake/path/model.pth"
    }
    
    with patch('os.path.exists', return_value=True), \
         patch('torch.load'), \
         patch('torch.nn.Linear') as mock_linear:
        mock_model = MagicMock()
        mock_linear.return_value = mock_model
        mock_model.load_state_dict = MagicMock()
        
        integration = PyTorchIntegration()
        with patch.object(integration, '_model_loaded', True):
            integration.load_model(config)
            mock_linear.assert_called_once()

def test_load_model_missing_both_args():
    integration = PyTorchIntegration()
    with pytest.raises(ValueError, match="Either model_path or model_config must be provided"):
        integration.load_model()

def test_load_model_unsupported_model_class():
    config = {"model_class": "UnsupportedModel"}
    integration = PyTorchIntegration()
    
    with pytest.raises(ValueError, match="Unsupported model class"):
        integration.load_model(config)

def test_predict_without_loading_model():
    integration = PyTorchIntegration()
    with pytest.raises(RuntimeError, match="Model not loaded"):
        integration.predict([1.0, 2.0, 3.0])

def test_predict_with_list_input():
    model = MagicMock()
    model.return_value = torch.tensor([0.5])
    
    integration = PyTorchIntegration()
    integration._model_loaded = True
    with patch.object(integration, 'model', model):
        result = integration.predict([1.0, 2.0, 3.0])
        assert isinstance(result, np.ndarray)

def test_predict_with_numpy_input():
    model = MagicMock()
    model.return_value = torch.tensor([0.5])
    
    integration = PyTorchIntegration()
    integration._model_loaded = True
    with patch.object(integration, 'model', model):
        input_data = np.array([1.0, 2.0, 3.0])
        result = integration.predict(input_data)
        assert isinstance(result, np.ndarray)

def test_predict_with_torch_tensor_input():
    model = MagicMock()
    model.return_value = torch.tensor([0.5])
    
    integration = PyTorchIntegration()
    integration._model_loaded = True
    with patch.object(integration, 'model', model):
        input_data = torch.tensor([1.0, 2.0, 3.0])
        result = integration.predict(input_data)
        assert isinstance(result, np.ndarray)

def test_predict_model_not_loaded():
    integration = PyTorchIntegration()
    integration._model_loaded = False
    with pytest.raises(RuntimeError, match="Model not loaded"):
        integration.predict([1.0, 2.0, 3.0])

def test_prepare_input_valid_dict():
    integration = PyTorchIntegration()
    data = {"b": 2.0, "a": 1.0, "c": 3.0}
    result = integration._prepare_input(data)
    assert isinstance(result, torch.Tensor)
    assert result.tolist() == [1.0, 2.0, 3.0]

def test_prepare_input_invalid_type():
    integration = PyTorchIntegration()
    with pytest.raises(ValueError, match="Input data must be a dictionary"):
        integration._prepare_input([1, 2, 3])

def test_load_model_file_not_found():
    integration = PyTorchIntegration("/nonexistent/model.pt")
    with pytest.raises(FileNotFoundError):
        integration.load_model()

def test_load_model_with_invalid_config():
    config = {"model_class": "PyTorchModel"}
    integration = PyTorchIntegration()
    
    with pytest.raises(KeyError):
        # Missing required fields
        integration.load_model(config)

@patch('os.path.exists', return_value=True)
@patch('torch.load', side_effect=Exception("Load error"))
def test_load_model_error_handling(mock_load, mock_exists):
    integration = PyTorchIntegration("/fake/path/model.pt")
    with pytest.raises(Exception, match="Load error"):
        integration.load_model()

def test_predict_device_placement():
    model = MagicMock()
    model.return_value = torch.tensor([0.5])
    
    integration = PyTorchIntegration()
    integration._model_loaded = True
    
    with patch.object(integration, 'model', model), \
         patch('torch.cuda.is_available', return_value=False):
        integration.device = torch.device('cpu')
        result = integration.predict([1.0, 2.0])
        # Should not raise any error about device placement

def test_predict_returns_tensor():
    model = MagicMock()
    mock_output = MagicMock()
    mock_output.cpu().numpy.return_value = np.array([1.0, 2.0])
    model.return_value = mock_output
    
    integration = PyTorchIntegration()
    integration._model_loaded = True
    with patch.object(integration, 'model', model):
        result = integration.predict([1.0])
        assert isinstance(result, np.ndarray)

def test_predict_model_none_after_loading():
    integration = PyTorchIntegration()
    integration._model_loaded = True
    integration.model = None
    
    with pytest.raises(RuntimeError, match="Model is not loaded"):
        integration.predict([1.0, 2.0])