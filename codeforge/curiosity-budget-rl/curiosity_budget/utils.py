import logging
import os
import json
import pickle
from typing import Any, Dict, Optional
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def log(message: str, level: int = logging.INFO) -> None:
    """Log a message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.log(level, f"[{timestamp}] {message}")

def save_model(model: nn.Module, path: str) -> None:
    """Save a PyTorch model to a file"""
    try:
        # Create directory if it doesn't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save model state dict
        torch.save(model.state_dict(), path)
        log(f"Model saved to {path}")
    except Exception as e:
        log(f"Failed to save model to {path}: {str(e)}", logging.ERROR)
        raise

def load_model(model: nn.Module, path: str) -> nn.Module:
    """Load a PyTorch model from a file"""
    try:
        if os.path.exists(path):
            state_dict = torch.load(path, map_location=torch.device('cpu'))
            model.load_state_dict(state_dict, strict=False)
            model.eval()  # Set model to evaluation mode
            log(f"Model loaded from {path}")
        else:
            log(f"Model file {path} not found", logging.WARNING)
        return model
    except Exception as e:
        log(f"Failed to load model from {path}: {str(e)}", logging.ERROR)
        raise

def plot(
    data: Dict[str, Any], 
    title: str = "Training Progress",
    xlabel: str = "Steps",
    ylabel: str = "Value",
    save_path: Optional[str] = None
) -> None:
    """Plot training metrics or other data"""
    try:
        plt.figure(figsize=(10, 6))
        
        for label, values in data.items():
            if isinstance(values, dict) and "x" in values and "y" in values:
                plt.plot(values["x"], values["y"], label=label)
            else:
                plt.plot(values, label=label)
        
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
            
        plt.close()
    except Exception as e:
        log(f"Failed to plot data: {str(e)}", logging.ERROR)
        raise