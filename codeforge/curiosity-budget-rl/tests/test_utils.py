import logging
import os
from unittest.mock import patch, MagicMock, mock_open
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

class TestLogger:
    def test_log_info_level(self, caplog):
        from curiosity_budget.utils import log
        with caplog.at_level(logging.INFO):
            log("Test message")
        assert "Test message" in caplog.text
        assert "INFO" in caplog.text

    def test_log_error_level(self, caplog):
        from curiosity_budget.utils import log
        with caplog.at_level(logging.ERROR):
            log("Error message", logging.ERROR)
        assert "Error message" in caplog.text
        assert "ERROR" in caplog.text

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(1, 1)
    
    def forward(self, x):
        return self.layer(x)

class TestSaveModel:
    @patch('torch.save')
    @patch('curiosity_budget.utils.Path')
    @patch('curiosity_budget.utils.log')
    def test_save_model_success(self, mock_log, mock_path, mock_torch_save):
        from curiosity_budget.utils import save_model
        model = DummyModel()
        path = "/tmp/model.pth"
        save_model(model, path)
        mock_torch_save.assert_called_once()
        mock_log.assert_called()

    @patch('torch.save', side_effect=Exception("Save error"))
    @patch('curiosity_budget.utils.log')
    def test_save_model_failure(self, mock_log, mock_torch_save):
        from curiosity_budget.utils import save_model
        model = DummyModel()
        path = "/tmp/model.pth"
        try:
            save_model(model, path)
        except Exception:
            pass
        mock_log.assert_called_with(
            f"Failed to save model to {path}: Save error",
            logging.ERROR
        )

class TestPlot:
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.close')
    @patch('curiosity_budget.utils.log')
    def test_plot_simple_data(self, mock_log, mock_close, mock_show, mock_plot):
        from curiosity_budget.utils import plot
        data = {"test": [1, 2, 3]}
        plot(data)
        mock_plot.assert_called()
        mock_show.assert_called_once()
        mock_close.assert_called_once()
        mock_log.assert_not_called()

    @patch('matplotlib.pyplot.savefig')
    @patch('curiosity_budget.utils.log')
    def test_plot_with_save_path(self, mock_log, mock_savefig):
        from curiosity_budget.utils import plot
        data = {"test": [1, 2, 3]}
        plot(data, save_path="/tmp/plot.png")
        mock_savefig.assert_called_with("/tmp/plot.png")
        mock_log.assert_not_called()

    @patch('matplotlib.pyplot.plot', side_effect=Exception("Plot error"))
    @patch('curiosity_budget.utils.log')
    def test_plot_failure(self, mock_log, mock_plot):
        from curiosity_budget.utils import plot
        data = {"test": [1, 2, 3]}
        try:
            plot(data)
        except Exception:
            pass
        mock_log.assert_called_with("Failed to plot data: Plot error", logging.ERROR)

class TestLoadModel:
    @patch('os.path.exists', return_value=True)
    @patch('torch.load')
    @patch('curiosity_budget.utils.log')
    def test_load_model_success(self, mock_log, mock_torch_load, mock_exists):
        from curiosity_budget.utils import load_model
        model = DummyModel()
        path = "/tmp/model.pth"
        mock_torch_load.return_value = {'layer.weight': torch.tensor([1.0])}
        result = load_model(model, path)
        assert isinstance(result, DummyModel)
        mock_log.assert_called()

    @patch('os.path.exists', return_value=False)
    @patch('curiosity_budget.utils.log')
    def test_load_model_file_not_found(self, mock_log, mock_exists):
        from curiosity_budget.utils import load_model
        model = DummyModel()
        path = "/tmp/model.pth"
        result = load_model(model, path)
        assert result == model
        mock_log.assert_called()

    @patch('os.path.exists', return_value=True)
    @patch('torch.load', side_effect=Exception("Load error"))
    @patch('curiosity_budget.utils.log')
    def test_load_model_failure(self, mock_log, mock_torch_load, mock_exists):
        from curiosity_budget.utils import load_model
        model = DummyModel()
        path = "/tmp/model.pth"
        try:
            load_model(model, path)
        except Exception:
            pass
        mock_log.assert_called_with(
            f"Failed to load model from {path}: Load error",
            logging.ERROR
        )