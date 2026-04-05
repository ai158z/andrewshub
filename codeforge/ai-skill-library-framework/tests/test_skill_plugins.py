import pytest
from unittest.mock import Mock, patch, MagicMock
from src.skill_plugins import SkillPlugin, BaseSkillPlugin, PluginManager, create_plugin
from src.models.skill import Skill


def test_skill_plugin_abstract_base():
    """Test that SkillPlugin is abstract and cannot be instantiated directly"""
    with pytest.raises(TypeError):
        SkillPlugin("test")


def test_base_skill_plugin_initialization():
    """Test BaseSkillPlugin can be instantiated and initialized properly"""
    plugin = BaseSkillPlugin("test_plugin")
    assert plugin.name == "test_plugin"
    assert plugin.version == "1.0"
    assert not plugin._is_loaded


def test_base_skill_plugin_load_unload():
    """Test BaseSkillPlugin load and unload methods"""
    plugin = BaseSkillPlugin("test_plugin")
    
    # Mock the skill loading
    with patch.object(plugin, '_load_skills') as mock_load:
        plugin.load_plugin()
        mock_load.assert_called_once()
        assert plugin._is_loaded
    
    plugin.unload_plugin()
    assert not plugin._is_loaded


def test_plugin_manager_initialization():
    """Test PluginManager initializes with correct default paths"""
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        manager = PluginManager()
        assert len(manager._plugin_paths) >= 3
        assert len(manager.plugins) == 0


def test_plugin_manager_discover_plugins():
    """Test plugin discovery from filesystem"""
    with patch('os.listdir') as mock_listdir, \
         patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        mock_listdir.return_value = ['test_plugin.py', 'another_plugin.py', 'not_a_plugin.txt']
        
        manager = PluginManager()
        plugins = manager.discover_plugins()
        assert isinstance(plugins, list)


def test_plugin_manager_load_plugin_success():
    """Test successful plugin loading"""
    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_plugin_class = Mock()
        mock_plugin_class.return_value = Mock()
        mock_import.return_value = Mock()
        mock_import.return_value.TestPlugin = mock_plugin_class
        
        manager = PluginManager()
        plugin = manager.load_plugin("test")
        assert plugin is not None


def test_plugin_manager_load_plugin_import_error():
    """Test plugin loading with import error"""
    with patch('importlib.import_module', side_effect=ImportError("Not found")):
        manager = PluginManager()
        plugin = manager.load_plugin("nonexistent")
        assert plugin is None


def test_plugin_manager_unload_plugin_not_found():
    """Test unloading a plugin that doesn't exist"""
    manager = PluginManager()
    result = manager.unload_plugin("nonexistent")
    assert not result


def test_plugin_manager_register_plugin():
    """Test plugin registration"""
    manager = PluginManager()
    plugin = BaseSkillPlugin("test")
    
    with patch.object(plugin, 'register') as mock_register:
        mock_register.return_value = None
        result = manager.register_plugin(plugin)
        assert result


def test_plugin_manager_get_plugin():
    """Test getting plugin by name"""
    manager = PluginManager()
    plugin = BaseSkillPlugin("test")
    
    with patch.object(manager.plugins, 'get', return_value=plugin):
        result = manager.get_plugin("test")
        assert result == plugin


def test_create_plugin_factory():
    """Test plugin factory creates correct plugin types"""
    plugin = create_plugin("base", "test")
    assert isinstance(plugin, BaseSkillPlugin)
    
    with pytest.raises(ValueError):
        create_plugin("invalid", "test")


def test_base_skill_plugin_add_remove_skill():
    """Test adding and removing skills from plugin"""
    plugin = BaseSkillPlugin("test")
    skill = Skill(id="test_skill", name="Test Skill", description="A test skill")
    
    # Test add skill
    plugin.add_skill(skill)
    assert len(plugin._skills) == 1
    
    # Test remove skill
    result = plugin.remove_skill("test_skill")
    assert result
    assert len(plugin._skills) == 0


def test_base_skill_plugin_register():
    """Test plugin registration with skill manager"""
    plugin = BaseSkillPlugin("test")
    skill = Skill(id="test_skill", name="Test Skill", description="A test skill")
    
    with patch('src.skill_manager.SkillManager.register_skill') as mock_register:
        plugin.add_skill(skill)
        plugin.register()
        mock_register.assert_called_once()


def test_base_skill_plugin_unload():
    """Test plugin unregistration"""
    plugin = BaseSkillPlugin("test")
    skill = Skill(id="test_skill", name="Test Skill", description="A test skill")
    plugin.add_skill(skill)
    
    with patch('src.skill_manager.SkillManager.unregister_skill') as mock_unregister:
        plugin.unload_plugin()
        mock_unregister.assert_called_with("test_skill")


def test_plugin_manager_list_plugins():
    """Test listing loaded plugins"""
    manager = PluginManager()
    plugin = BaseSkillPlugin("test")
    
    with patch.object(manager.plugins, 'get', return_value=plugin):
        manager.plugins["test"] = plugin
        plugins = manager.list_plugins()
        assert "test" in plugins


def test_plugin_manager_load_already_loaded():
    """Test loading already loaded plugin"""
    manager = PluginManager()
    plugin = BaseSkillPlugin("test")
    
    with patch.object(manager.plugins, '__contains__', return_value=True), \
         patch.object(manager.plugins, '__getitem__', return_value=plugin):
        result = manager.load_plugin("test")
        assert result == plugin


def test_base_skill_plugin_remove_nonexistent_skill():
    """Test removing a skill that doesn't exist"""
    plugin = BaseSkillPlugin("test")
    result = plugin.remove_skill("nonexistent")
    assert not result


def test_plugin_manager_discover_plugins_os_error():
    """Test plugin discovery with OS error"""
    with patch('os.listdir', side_effect=OSError("Permission denied")):
        manager = PluginManager()
        plugins = manager.discover_plugins()
        assert isinstance(plugins, list)
        assert len(plugins) == 0


def test_plugin_manager_register_plugin_failure():
    """Test plugin registration failure"""
    manager = PluginManager()
    plugin = BaseSkillPlugin("test")
    
    with patch.object(plugin, 'register', side_effect=Exception("Registration failed")):
        result = manager.register_plugin(plugin)
        assert not result

class TestSkillPlugin(SkillPlugin):
    def register(self):
        pass
    
    def load_plugin(self):
        pass
    
    def unload_plugin(self):
        pass

def test_skill_plugin_instantiation():
    """Test that concrete SkillPlugin implementation can be instantiated"""
    plugin = TestSkillPlugin("test")
    assert plugin.name == "test"