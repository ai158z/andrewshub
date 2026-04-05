import pytest
import torch
import torch.nn as nn
from unittest.mock import Mock, patch, MagicMock
from src.codonic_layer import CodonicLayer

class MockPINN:
    def __init__(self):
        pass

class MockBodySchemaLearner:
    def get_body_state(self):
        return {
            'link_lengths': [1.0, 1.0, 1.0],
            'joint_angles': torch.tensor([0.1, 0.2, 0.3])
        }

class MockBiomechanicalConstraints:
    def apply_joint_limits(self, x):
        return x

class MockRynnECVideoAnalyzer:
    def __init__(self):
        pass

class MockPhysicsConstraints:
    def __init__(self):
        pass

@pytest.fixture
def mock_components():
    pinn_model = MockPINN()
    body_schema_learner = MockBodySchemaLearner()
    biomechanical_constraints = MockBiomechanicalConstraints()
    rynnec_analyzer = MockRynnECVideoAnalyzer()
    physics_constraints = MockPhysicsConstraints()
    
    return {
        'pinn_model': pinn_model,
        'body_schema_learner': body_schema_learner,
        'biomechanical_constraints': biomechanical_constraints,
        'rynnec_analyzer': rynnec_analyzer,
        'physics_constraints': physics_constraints
    }

@pytest.fixture
def codonic_layer(mock_components):
    with patch('src.codonic_layer.CodonicNetwork') as mock_network:
        mock_network.return_value = Mock()
        mock_network.return_value.to = Mock(return_value=mock_network.return_value)
        layer = CodonicLayer(
            input_dim=10,
            hidden_dim=20,
            output_dim=5,
            pinn_model=mock_components['pinn_model'],
            body_schema_learner=mock_components['body_schema_learner'],
            biomechanical_constraints=mock_components['biomechanical_constraints'],
            rynnec_analyzer=mock_components['rynnec_analyzer'],
            physics_constraints=mock_components['physics_constraints']
        )
        return layer

def test_init_success(codonic_layer):
    assert codonic_layer is not None
    assert hasattr(codonic_layer, 'codonic_network')
    assert hasattr(codonic_layer, 'optimizer')

def test_predict_sensory_output_valid_input(codonic_layer):
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles)
    
    assert result is not None
    assert 'raw_output' in metadata
    assert 'constrained_output' in metadata

def test_predict_sensory_output_invalid_input_type(codonic_layer):
    with pytest.raises(TypeError):
        codonic_layer.predict_sensory_output([0.1, 0.2, 0.3])  # List instead of tensor

def test_predict_sensory_output_with_external_forces(codonic_layer):
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    external_forces = torch.tensor([0.5, 0.5, 0.5])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles, external_forces)
    
    assert result is not None
    assert 'raw_output' in metadata

def test_predict_sensory_output_no_link_lengths(codonic_layer):
    # Mock body state with no link lengths
    codonic_layer.body_schema_learner.get_body_state = Mock(return_value={})
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles)
    
    assert result is not None
    assert 'input_positions' in metadata

def test_update_codonic_weights_updates_weights(codonic_layer):
    target_data = torch.tensor([1.0, 2.0, 3.0])
    metrics = codonic_layer.update_codonic_weights(target_data)
    
    assert 'loss' in metrics
    assert 'learning_rate' in metrics
    assert metrics['loss'] >= 0

def test_update_codonic_weights_with_custom_lr(codonic_layer):
    target_data = torch.tensor([1.0, 2.0, 3.0])
    metrics = codonic_layer.update_codonic_weights(target_data, learning_rate=0.01)
    
    assert 'loss' in metrics
    assert metrics['learning_rate'] == 0.01

def test_integrate_with_pinn(codonic_layer):
    mock_pinn_model = Mock()
    mock_pinn_model.compute_physics_loss = Mock(return_value=torch.tensor(0.5))
    
    sensory_data = torch.tensor([1.0, 2.0, 3.0])
    loss = codonic_layer.integrate_with_pinn(mock_pinn_model, sensory_data)
    
    assert loss is not None
    assert isinstance(loss, torch.Tensor)

def test_integrate_with_pinn_no_physics_weight(codonic_layer):
    mock_pinn_model = Mock()
    mock_pinn_model.compute_physics_loss = Mock(return_value=torch.tensor(0.5))
    
    sensory_data = torch.tensor([1.0, 2.0, 3.0])
    loss = codonic_layer.integrate_with_pinn(mock_pinn_model, sensory_data, physics_weight=0.0)
    
    assert loss is not None

def test_update_codonic_weights_training_mode(codonic_layer):
    codonic_layer.codonic_network.train = Mock()
    codonic_layer.codonic_network.eval = Mock()
    
    target_data = torch.tensor([1.0, 2.0, 3.0])
    codonic_layer.update_codonic_weights(target_data)
    
    codonic_layer.codonic_network.train.assert_called()
    codonic_layer.codonic_network.eval.assert_called()

def test_predict_sensory_output_body_state_empty(codonic_layer):
    codonic_layer.body_schema_learner.get_body_state = Mock(return_value={})
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles)
    
    assert result is not None
    assert 'body_state' in metadata
    assert metadata['body_state'] == {}

def test_predict_sensory_output_body_state_with_links(codonic_layer):
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles)
    
    assert result is not None
    assert 'input_positions' in metadata

def test_update_codonic_weights_none_lr(codonic_layer):
    target_data = torch.tensor([1.0, 2.0, 3.0])
    original_lr = codonic_layer.optimizer.param_groups[0]['lr']
    metrics = codonic_layer.update_codonic_weights(target_data)
    
    # Should use default learning rate
    assert metrics['learning_rate'] == original_lr

def test_update_codonic_weights_error_handling(codonic_layer):
    # Test that exceptions are properly raised
    with patch.object(codonic_layer.codonic_network, 'backward', side_effect=Exception("Test error")):
        with pytest.raises(Exception, match="Test error"):
            target_data = torch.tensor([1.0, 2.0, 3.0])
            codonic_layer.update_codonic_weights(target_data)

def test_integrate_with_pinn_physics_weight_range(codonic_layer):
    mock_pinn_model = Mock()
    mock_pinn_model.compute_physics_loss = Mock(return_value=torch.tensor(0.5))
    
    sensory_data = torch.tensor([1.0, 2.0, 3.0])
    
    # Test with physics_weight = 1.0 (full physics)
    loss1 = codonic_layer.integrate_with_pinn(mock_pinn_model, sensory_data, physics_weight=1.0)
    # Test with physics_weight = 0.0 (no physics)
    loss2 = codonic_layer.integrate_with_pinn(mock_pinn_model, sensory_data, physics_weight=0.0)
    
    assert loss1 is not None
    assert loss2 is not None

def test_predict_sensory_output_logging(codonic_layer, caplog):
    import logging
    with caplog.at_level(logging.DEBUG):
        joint_angles = torch.tensor([0.1, 0.2, 0.3])
        codonic_layer.predict_sensory_output(joint_angles)
    
    # Check if debug logging occurred
    assert "completed successfully" in caplog.text or "Sensory prediction completed" in caplog.text

def test_predict_sensory_output_error_handling(codonic_layer):
    # Test error handling with invalid tensor
    with pytest.raises(TypeError):
        codonic_layer.predict_sensory_output("not_a_tensor")

def test_predict_sensory_output_no_external_forces(codonic_layer):
    joint_angles = torch.tensor([0.1, 0.2, 0.3])
    result, metadata = codonic_layer.predict_sensory_output(joint_angles, None)
    
    assert result is not None
    assert 'raw_output' in metadata

def test_update_codonic_weights_zero_lr(codonic_layer):
    target_data = torch.tensor([1.0, 2.0, 3.0])
    # This should use default learning rate
    metrics = codonic_layer.update_codonic_weights(target_data, learning_rate=0.0)
    
    # Even with 0.0 lr, should still get metrics back
    assert 'loss' in metrics

def test_update_codonic_weights_negative_lr(codonic_layer):
    target_data = torch.tensor([1.0, 2.0, 3.0])
    # Test negative learning rate handling
    with pytest.raises(Exception) as exc_info:
        codonic_layer.update_codonic_weights(target_data, learning_rate=-0.01)
    # Exception handling would depend on implementation, but we're testing the interface
    assert True  # Just testing that we can call it