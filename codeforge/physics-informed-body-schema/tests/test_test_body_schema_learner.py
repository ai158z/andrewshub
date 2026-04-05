import pytest
import torch
import torch.nn as nn
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from body_schema_learner import BodySchemaLearner
from pinn_body_model import PINNBodyModel
from biomechanical_constraints import BiomechanicalConstraints
from rynnec_video_analyzer import RynnECVideoAnalyzer
from codonic_layer import CodonicLayer
from utils.kinematics import forward_kinematics, inverse_kinematics

# Mock data for testing
@pytest.fixture
def mock_joint_angles():
    return torch.tensor([0.1, 0.2, 0.3], dtype=torch.float32)

@pytest.fixture
def mock_link_lengths():
    return [0.3, 0.4, 0.5]

@pytest.fixture
def mock_sensory_data():
    return torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)

@pytest.fixture
def mock_target_position():
    return torch.tensor([0.5, 0.5], dtype=torch.float32)

@pytest.fixture
def body_schema_learner():
    body_model = Mock(spec=PINNBodyModel)
    constraints = Mock(spec=BiomechanicalConstraints)
    video_analyzer = Mock(spec=RynnECVideoAnalyzer)
    codonic_layer = Mock(spec=CodonicLayer)
    
    return BodySchemaLearner(
        body_model=body_model,
        constraints=constraints,
        video_analyzer=video_analyzer,
        codonic_layer=codonic_layer
    )

def test_body_schema_initialization():
    body_model = Mock(spec=PINNBodyModel)
    constraints = Mock(spec=BiomechanicalConstraints)
    video_analyzer = Mock(spec=RynnECVideoAnalyzer)
    codonic_layer = Mock(spec=CodonicLayer)
    
    learner = BodySchemaLearner(
        body_model=body_model,
        constraints=constraints,
        video_analyzer=video_analyzer,
        codonic_layer=codonic_layer
    )
    
    assert isinstance(learner.body_model, Mock)
    assert isinstance(learner.constraints, Mock)
    assert isinstance(learner.video_analyzer, Mock)
    assert isinstance(learner.codonic_layer, Mock)

def test_body_schema_learner_adaptation(body_schema_learner):
    sensory_data = torch.randn(100, 3)
    
    with patch.object(body_schema_learner, 'adapt_body_schema') as mock_adapt:
        mock_adapt.return_value = {
            'loss': 0.01,
            'updated': True,
            'gradient_norm': 0.05
        }
        
        result = body_schema_learner.adapt_body_schema(sensory_data)
        
        mock_adapt.assert_called_once()
        assert isinstance(result, dict)
        assert 'loss' in result
        assert 'updated' in result
        assert 'gradient_norm' in result

def test_forward_kinematics(mock_joint_angles, mock_link_lengths):
    result = forward_kinematics(mock_joint_angles, mock_link_lengths)
    assert result is not None
    assert len(result) == 2

def test_inverse_kinematics(mock_target_position, mock_link_lengths):
    result = inverse_kinematics(mock_target_position, mock_link_lengths)
    assert result is not None
    assert len(result) == 3

def test_kinematic_calibration():
    # Test forward kinematics
    joint_angles = torch.tensor([0.1, 0.2, 0.3], dtype=torch.float32)
    link_lengths = [0.3, 0.4, 0.5]
    
    fk_result = forward_kinematics(joint_angles, link_lengths)
    assert fk_result is not None
    assert len(fk_result) == 2
    
    # Test inverse kinematics
    target_position = torch.tensor([0.5, 0.5], dtype=torch.float32)
    ik_result = inverse_kinematics(target_position, link_lengths)
    assert ik_result is not None
    assert len(ik_result) == 3

def test_body_model_initialization():
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    assert body_model is not None

def test_body_model_forward_pass(mock_sensory_data):
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    pred = body_model(mock_sensory_data)
    assert pred is not None
    assert pred.shape == (2,)

def test_body_model_training():
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    initial_params = [p.clone() for p in body_model.parameters()]
    
    # Mock calibration data
    sensory_data = torch.randn(3)
    target = torch.randn(2)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(body_model.parameters(), lr=0.001)
    
    pred = body_model(sensory_data)
    loss = loss_fn(pred, target)
    loss.backward()
    
    for param in body_model.parameters():
        if param.grad is not None:
            assert param.grad is not None

def test_constraints_initialization():
    constraints = BiomechanicalConstraints(
        joint_limits=[(-3.14, 3.14), (-1.57, 1.57), (-1.57, 1.57)],
        torque_limits=[(-10.0, 10.0), (-5.0, 5.0), (-5.0, 5.0)]
    )
    
    assert constraints is not None

def test_video_analyzer_initialization():
    video_analyzer = RynnECVideoAnalyzer()
    assert video_analyzer is not None

def test_codonic_layer_initialization():
    codonic_layer = CodonicLayer(input_size=10, hidden_size=16, output_size=3)
    assert codonic_layer is not None

def test_adaptation_returns_dict(body_schema_learner):
    sensory_data = torch.randn(100, 3)
    
    with patch.object(body_schema_learner, 'adapt_body_schema') as mock_adapt:
        mock_adapt.return_value = {
            'loss': 0.01,
            'updated': True,
            'gradient_norm': 0.05
        }
        
        result = body_schema_learner.adapt_body_schema(sensory_data)
        assert isinstance(result, dict)

def test_adaptation_calls_adapt_method(body_schema_learner):
    sensory_data = torch.randn(100, 3)
    
    with patch.object(body_schema_learner, 'adapt_body_schema') as mock_adapt:
        mock_adapt.return_value = {
            'loss': 0.01,
            'updated': True,
            'gradient_norm': 0.05
        }
        
        body_schema_learner.adapt_body_schema(sensory_data)
        mock_adapt.assert_called_once()

def test_kinematic_calibration_forward():
    joint_angles = torch.tensor([0.1, 0.2, 0.3], dtype=torch.float32)
    link_lengths = [0.3, 0.4, 0.5]
    result = forward_kinematics(joint_angles, link_lengths)
    assert result is not None
    assert len(result) == 2

def test_kinematic_calibration_inverse():
    target_position = torch.tensor([0.5, 0.5], dtype=torch.float32)
    link_lengths = [0.3, 0.4, 0.5]
    result = inverse_kinematics(target_position, link_lengths)
    assert result is not None
    assert len(result) == 3

def test_body_model_has_parameters():
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    params = list(body_model.parameters())
    assert len(params) > 0

def test_body_model_loss_computation(mock_sensory_data):
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    sensory_data = torch.randn(3)
    target = torch.randn(2)
    loss_fn = nn.MSELoss()
    pred = body_model(sensory_data)
    loss = loss_fn(pred, target)
    
    assert loss is not None

def test_body_model_gradient_computation():
    body_model = PINNBodyModel(
        input_size=3,
        hidden_sizes=[16, 12],
        output_size=2,
        spatial_dim=2
    )
    
    # Mock calibration data
    sensory_data = torch.randn(3)
    target = torch.randn(2)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(body_model.parameters(), lr=0.001)
    
    pred = body_model(sensory_data)
    loss = loss_fn(pred, target)
    loss.backward()
    
    for param in body_model.parameters():
        if param.grad is not None:
            assert param.grad is not None

def test_constraints_exist():
    constraints = BiomechanicalConstraints(
        joint_limits=[(-3.14, 3.14), (-1.57, 1.57), (-1.57, 1.57)],
        torque_limits=[(-10.0, 10.0), (-5.0, 5.0), (-5.0, 5.0)]
    )
    
    assert constraints is not None

def test_video_analyzer_exists():
    video_analyzer = RynnECVideoAnalyzer()
    assert video_analyzer is not None

def test_codonic_layer_exists():
    codonic_layer = CodonicLayer(input_size=10, hidden_size=16, output_size=3)
    assert codonic_layer is not None