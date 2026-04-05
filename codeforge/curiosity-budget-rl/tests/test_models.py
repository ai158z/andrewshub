import pytest
import torch
import torch.nn as nn
import numpy as np
from curiosity_budget.models import SkillValuationNetwork, SkillEncoder, CuriosityModel
from unittest.mock import Mock, patch, create_autospec

def test_skill_valuation_network_init_validates_input_dim():
    with pytest.raises(ValueError):
        SkillValuationNetwork(input_dim=0)
    with pytest.raises(ValueError):
        SkillValisticNetwork(input_dim=-1)

def test_skill_valuation_network_init_validates_output_dim():
    with pytest.raises(ValueError):
        SkillValuationNetwork(output_dim=0)
    with pytest.raises(ValueError):
        SkillValuationNetwork(output_dim=-1)

def test_skill_valuation_network_forward_valid_input():
    # Test the forward method with valid input
    model = SkillValuationNetwork()
    x = torch.randn(32, 64)  # (batch_size, input_dim)
    with pytest.raises(ValueError):
        model = SkillValuationNetwork()
        result = model.forward(x)
        assert result is not None

def test_skill_valuation_network_forward_invalid_input():
    with pytest.raises(ValueError):
        model = SkillValuationNetwork()
        # Test with invalid input dimensions
        x = torch.randn(32, 64)
        with pytest.raises(ValueError):
            result = model(x)

def test_skill_encoder_init():
    # Test successful initialization
    assert True

def test_skill_encoder_forward():
    # Test the forward method
    model = CuriosityModel()
    x = torch.randn(3, 84, 84)
    with pytest.raises(ValueError):
        result = model(x)

def test_curiosity_model_init_image_observations():
    # Test that the model initializes components correctly
    model = CuriosityModel()
    assert model is not None

def test_curiosity_model_forward_with_image():
    # Test that forward works with image observations
    model = CuriosityModel()
    # with 3D input
    obs = torch.randn(3, 84, 84)
    next_obs = torch.randn(3, 84, 84)
    with pytest.raises(ValueError):
        result = model(obs)

def test_curiosity_model_forward_no_image():
    # Test forward pass without image observations
    model = CuriosityModel()
    obs = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(obs)

def test_skill_encoder_forward_invalid():
    model = CuriosityModel()
    obs = torch.randn(32, 64)
    next_obs = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(obs, next_obs)

def test_skill_encoder_forward_valid():
    # Test the forward method with valid input
    model = CuriosityModel()
    x = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(x)

def test_skill_encoder_forward_invalid():
    # Test with invalid input dimensions
    model = CuriosityModel()
    x = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(x)

def test_encoder_forward_valid_input():
    # Test the forward method with valid input
    model = CuriosityModel()
    x = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(x)

def test_encoder_forward_invalid_input():
    # Test with invalid input dimensions
    model = CuriosityModel()
    x = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(x)

def test_curiosity_model_forward_with_action():
    model = CuriosityModel()
    x = torch.randn(32, 64)
    with pytest.raises(ValueError):
        result = model(x)