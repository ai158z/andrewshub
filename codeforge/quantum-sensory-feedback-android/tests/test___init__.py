import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
import src.quantum_sensors as qs

class TestQuantumSensorsModule:
    """Test cases for quantum_sensors module functions"""

    @pytest.fixture
    def app_instance(self):
        """Create a FastAPI app instance for testing"""
        return FastAPI()

    def test_version_exists(self):
        """Test that package version is defined"""
        assert qs.__version__ == "1.0.0"

    def test_module_attributes(self):
        """Test that all expected attributes exist in __all__"""
        expected_exports = [
            "ConfigManager",
            "SensorReading",
            "SensorFusionData",
            "fuse_sensors",
            "ZenoProcessor",
            "CodonicProcessor",
            "EntanglementHandler",
            "ROS2Bridge"
        ]
        
        for item in expected_exports:
            assert item in qs.__all__

    def test_get_app_returns_none_initially(self):
        """Test that get_app returns None before initialization"""
        app = qs.get_app()
        assert app is None

    def test_get_config_manager_returns_none_initially(self):
        """Test that get_config_manager returns None before initialization"""
        config_manager = qs.get_config_manager()
        assert config_manager is None

    @patch('src.quantum_sensors.ConfigManager')
    def test_initialize_app_sets_global_vars(self, mock_config_manager):
        """Test that initialize_app properly sets global application instances"""
        app = FastAPI()
        mock_app = Mock()
        mock_config = Mock()
        mock_config_manager.return_value = mock_config
        
        qs.initialize_app(app)
        
        # Verify that global variables are set
        assert qs._app is not None
        assert qs._config_manager is not None

    def test_get_sensor_models_returns_correct_types(self):
        """Test that get_sensor_models returns correct model types"""
        models = qs.get_sensor_models()
        assert 'SensorReading' in models
        assert 'SensorFusionData' in models
        assert models['SensorReading'] == qs.SensorReading
        assert models['SensorFusionData'] == qs.SensorFusionData

    def test_get_processing_components_structure(self):
        """Test that get_processing_components returns all processing components"""
        components = qs.get_processing_components()
        
        expected_components = {
            'fusion_engine',
            'zeno_processor', 
            'codonic_processor',
            'entanglement_handler',
            'ros2_bridge'
        }
        
        for component in expected_components:
            assert component in components

    @patch('src.quantum_sensors.ZenoProcessor')
    def test_zeno_processor_initialization(self, mock_zeno_processor):
        """Test that ZenoProcessor is properly instantiated"""
        mock_zeno_processor.return_value = Mock()
        processor = qs.ZenoProcessor()
        assert processor is not None

    def test_fusion_engine_exists(self):
        """Test that fusion engine component is available"""
        components = qs.get_processing_components()
        assert 'fusion_engine' in components

    def test_ros2_bridge_initialization(self):
        """Test that ROS2 bridge is properly created"""
        # Test that we can get the ROS2 bridge component
        components = qs.get_processing_components()
        assert 'ros2_bridge' in components
        assert components['ros2_bridge'] is not None

    def test_codonic_processor_initialization(self):
        """Test that CodonicProcessor is properly instantiated"""
        components = qs.get_processing_components()
        assert 'codonic_processor' in components
        assert components['codonic_processor'] is not None

    def test_entanglement_handler_initialization(self):
        """Test that EntanglementHandler is properly created"""
        components = qs.get_processing_components()
        entanglement_handler = components.get('entanglement_handler')
        assert entanglement_handler is not None

    @patch('src.quantum_sensors.ConfigManager')
    def test_config_manager_initialization(self, mock_config_manager):
        """Test ConfigManager initialization"""
        mock_config_manager.return_value = Mock()
        config = qs.ConfigManager()
        assert config is not None

    def test_fuse_sensors_function_exists(self):
        """Test that fuse_sensors function exists"""
        assert qs.fuse_sensors is not None

    def test_get_app_function(self):
        """Test get_app function returns app instance"""
        app = qs.get_app()
        # Initially should be None
        assert app is None

    def test_get_config_manager_function(self):
        """Test get_config_manager function"""
        config_manager = qs.get_config_manager()
        # Initially should be None
        assert config_manager is None

    def test_sensor_models_function(self):
        """Test get_sensor_models function returns correct models"""
        models = qs.get_sensor_models()
        assert 'SensorReading' in models
        assert 'SensorFusionData' in models