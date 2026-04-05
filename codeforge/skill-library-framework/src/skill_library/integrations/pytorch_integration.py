import os
import logging
from typing import Any, Dict, List, Optional, Union
import torch
import torch.nn as nn
from pathlib import Path
import json
import numpy as np

logger = logging.getLogger(__name__)

class PyTorchIntegration:
    def __init__(self, model_path: Optional[str] = None):
        self.model: Optional[nn.Module] = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path
        self._model_loaded = False
        logger.info(f"PyTorchIntegration initialized with device: {self.device}")

    def load_model(self, model_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Load a PyTorch model from the specified path or configuration.
        
        Args:
            model_config: Optional dictionary containing model configuration
        """
        try:
            if self.model_path and os.path.exists(self.model_path):
                # Load model from file
                if self.model_path.endswith('.pt') or self.model_path.endswith('.pth'):
                    self.model = torch.load(self.model_path, map_location=self.device)
                    if self.model is not None:
                        self.model.eval()
                        self._model_loaded = True
                    logger.info("Model loaded successfully")
                else:
                    # Assume it's a directory with model files
                    config_path = Path(self.model_path) / "config.json"
                    if config_path.exists():
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                        # Load model based on config
                        model_class = config.get("model_class", "PyTorchModel")
                        if model_class == "PyTorchModel":
                            self.model = PyTorchModel(config["input_dim"], config["output_dim"])
                            model_path = str(Path(self.model_path) / "model.pth")
                            if os.path.exists(model_path):
                                state_dict = torch.load(model_path, map_location=self.device)
                                self.model.load_state_dict(state_dict)
                                self.model.eval()
                                self._model_loaded = True
                            else:
                                raise FileNotFoundError(f"Model file not found at {model_path}")
                        else:
                            raise ValueError(f"Unsupported model class: {model_class}")
                    else:
                        raise FileNotFoundError(f"Config file not found at {config_path}")
                
                if self.model is not None:
                    self.model.eval()
                    self._model_loaded = True
            elif model_config:
                # Load from configuration
                model_class = model_config.get("model_class", "PyTorchModel")
                if model_class == "PyTorchModel":
                    input_dim = model_config["input_dim"]
                    output_dim = model_config["output_dim"]
                    self.model = PyTorchModel(input_dim, output_dim)
                    model_path = model_config.get("model_path")
                    if model_path and os.path.exists(model_path):
                        state_dict = torch.load(model_path, map_location=self.device)
                        if self.model is not None:
                            self.model.load_state_dict(state_dict)
                        self.model.eval()
                        self._model_loaded = True
                        logger.info("Model loaded from config successfully")
                    else:
                        raise FileNotFoundError(f"Model file not found at {model_path}")
                else:
                    raise ValueError(f"Unsupported model class: {model_class}")
            else:
                raise ValueError("Either model_path or model_config must be provided")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, input_data: Union[np.ndarray, List[float], torch.Tensor]) -> np.ndarray:
        """
        Make a prediction using the loaded model.
        
        Args:
            input_data: Input data for prediction
            
        Returns:
            np.ndarray: Prediction results
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
            
        try:
            # Convert input to tensor if needed
            if isinstance(input_data, list):
                input_tensor = torch.tensor(input_data, dtype=torch.float32)
            elif isinstance(input_data, np.ndarray):
                input_tensor = torch.from_numpy(input_data).float()
            else:
                input_tensor = input_data
                
            # Move to the same device as model
            input_tensor = input_tensor.to(self.device)
            
            with torch.no_grad():
                if self.model is None:
                    raise RuntimeError("Model is not loaded")
                output = self.model(input_tensor)
                if isinstance(output, torch.Tensor):
                    return output.cpu().numpy()
                else:
                    return np.array(output)
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise

    def _prepare_input(self, data: Dict[str, Any]) -> torch.Tensor:
        """Prepare input data for the model."""
        # Convert dict to tensor
        if isinstance(data, dict):
            # Sort keys to ensure consistent ordering
            sorted_data = [data[key] for key in sorted(data.keys())]
            return torch.tensor(sorted_data, dtype=torch.float32)
        else:
            raise ValueError("Input data must be a dictionary with numerical values")

# Additional model classes that might be used with this integration
class PyTorchModel(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super(PyTorchModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)
        
    def forward(self, x):
        return self.linear(x)