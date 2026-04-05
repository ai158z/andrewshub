import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.rynnec_video_analyzer import RynnECVideoAnalyzer

class TestRynnECVideoAnalyzer:
    @pytest.fixture
    def analyzer(self):
        model_config = {"test": "config"}
        return RynnECVideoAnalyzer(model_config)

    @patch('src.rynnec_video_analyzer.PINNBodyModel')
    @patch('src.rynnec_video_analyzer.BodySchemaLearner')
    @patch('src.rynnec_video_analyzer.BiomechanicalConstraints')
    @patch('src.rynnec_video_analyzer.CodonicNetwork')
    @patch('src.rynnec_video_analyzer.CodonicLayerModule')
    @patch('src.rynnec_video_analyzer.PhysicsConstraints')
    def test_init(self, mock_physics, mock_codonic_layer, mock_codonic_net, mock_constraints, mock_body_schema, mock_pinn, analyzer):
        # Test that initialization works with default config
        assert analyzer.model_config == {"test": "config"}
        assert hasattr(analyzer, 'body_schema_learner')
        assert hasattr(analyzer, 'pinn_model')
        assert hasattr(analyzer, 'biomechanical_constraints')
        assert hasattr(analyzer, 'codonic_layer')
        assert hasattr(analyzer, 'physics_constraints')
        assert hasattr(analyzer, 'pinn_body_model')
        assert hasattr(analyzer, 'codonic_network')

    def test_extract_regions_returns_list(self, analyzer):
        frame = np.array([[[1, 2, 3]]], dtype=np.uint8)
        result = analyzer.extract_regions(frame)
        assert isinstance(result, list)

    def test_analyze_motion_dynamics_with_empty_input(self, analyzer):
        result = analyzer.analyze_motion_dynamics([])
        assert result == {'displacement': [], 'velocity': [], 'acceleration': []}

    def test_analyze_motion_dynamics_with_regions(self, analyzer):
        regions = [
            {
                'motion_vectors': [(10, 20)],
                'displacement': (50, 60),
                'velocity_vectors': [(1, 1)]
            }
        ]
        result = analyzer.analyze_motion_dynamics(regions)
        assert 'displacement' in result
        assert 'velocity' in result
        assert 'acceleration' in result

    def test_predict_sensory_state(self, analyzer):
        time_series_data = [
            {"displacement": (1, 2), "velocity": (3, 4), "acceleration": (5, 6)}
        ]
        result = analyzer.predict_sensory_state(time_series_data)
        assert 'sensory_state' in result

    @patch('src.rynnec_video_analyzer.PINNBodyModel')
    @patch('src.rynnec_video_analyzer.PINNBodyModel.to')
    def test_device_assignment_cuda(self, mock_to, mock_pinn_model, analyzer):
        # Mock CUDA availability
        with patch('torch.cuda.is_available', return_value=True):
            mock_device = Mock()
            mock_device.type = 'cuda'
            with patch('torch.device', return_value=mock_device):
                analyzer = RynnECVideoAnalyzer({})
                mock_to.assert_called()

    def test_extract_regions_returns_empty_list_for_empty_frame(self, analyzer):
        frame = np.array([])
        result = analyzer.extract_regions(frame)
        assert result == []

    def test_analyze_motion_dynamics_returns_expected_keys(self, analyzer):
        regions = [{'motion_vectors': [], 'displacement': (0, 0), 'velocity_vectors': []}]
        result = analyzer.analyze_motion_dynamics(regions)
        expected_keys = {'displacement', 'velocity', 'acceleration'}
        assert set(result.keys()) == expected_keys

    def test_predict_sensory_state_returns_dict(self, analyzer):
        result = analyzer.predict_sensory_state([])
        assert isinstance(result, dict)
        assert 'sensory_state' in result

    def test_analyze_motion_dynamics_accumulates_correctly(self, analyzer):
        regions = [
            {'motion_vectors': [(10, 20), (30, 40)], 'displacement': (100, 200), 'velocity_vectors': [(1, 1), (2, 2)]},
            {'motion_vectors': [(50, 60)], 'displacement': (300, 400), 'velocity_vectors': [(3, 3)]}
        ]
        result = analyzer.analyze_motion_dynamics(regions)
        assert result['displacement'] == [(100, 200), (300, 400)]
        assert result['velocity'] == [[(1, 1), (2, 2)], [(3, 3)]]

    def test_extract_regions_basic_functionality(self, analyzer):
        dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = analyzer.extract_regions(dummy_frame)
        assert isinstance(result, list)

    def test_analyze_motion_dynamics_empty_region_skipped(self, analyzer):
        regions = [{}]
        result = analyzer.analyze_motion_dynamics(regions)
        assert result == {'displacement': [], 'velocity': [], 'acceleration': []}

    def test_analyze_motion_dynamics_mixed_regions(self, analyzer):
        regions = [
            {'displacement': (10, 20), 'velocity_vectors': [(1, 1)]},
            {'other_data': 'test'},
            {'motion_vectors': [(5, 5)], 'displacement': (30, 40)}
        ]
        result = analyzer.analyze_motion_dynamics(regions)
        assert len(result['displacement']) == 2
        assert len(result['velocity']) == 1

    def test_predict_sensory_state_with_data(self, analyzer):
        time_series = [{"data": "test"}]
        result = analyzer.predict_sensory_state(time_series)
        assert isinstance(result, dict)

    def test_analyzer_initialization_device_cpu_fallback(self, analyzer):
        assert hasattr(analyzer, 'device')

    def test_extract_regions_no_mutate_input(self, analyzer):
        frame = np.array([[[1, 2, 3]]], dtype=np.uint8)
        original_frame = frame.copy()
        analyzer.extract_regions(frame)
        np.testing.assert_array_equal(frame, original_frame)

    def test_analyze_motion_dynamics_no_side_effects(self, analyzer):
        original_regions = [{'motion_vectors': [(1, 2)], 'displacement': (5, 6), 'velocity_vectors': [(7, 8)]}]
        regions = original_regions.copy()
        analyzer.analyze_motion_dynamics(regions)
        assert regions == original_regions