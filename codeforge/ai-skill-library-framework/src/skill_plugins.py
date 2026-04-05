import importlib
import logging
import os
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.models.skill import Skill


class SkillPlugin(ABC):
    """Abstract base class for all skill plugins"""
    
    def __init__(self, name: str):
        self.name = name
        self.version: str = "1.0"
        self._is_loaded: bool = False
        self._skills: List[Skill] = []
    
    @abstractmethod
    def register(self) -> None:
        """Register the plugin's skills with the system"""
        pass

    @abstractmethod
    def load_plugin(self) -> None:
        """Load the plugin"""
        self._is_loaded = True

    @abstractmethod
    def unload_plugin(self) -> None:
        """Unload the plugin"""
        self._is_loaded = False
        # Unregister all skills when unloading
        for skill in self._skills:
            try:
                from src.skill_manager import SkillManager
                SkillManager.unregister_skill(skill.id)
            except ImportError:
                pass  # SkillManager not available, skip unregistering
        self._skills = []

    def add_skill(self, skill: Skill) -> None:
        """Add a skill to this plugin"""
        self._skills.append(skill)

    def remove_skill(self, skill_id: str) -> bool:
        """Remove a skill from this plugin by ID"""
        for i, skill in enumerate(self._skills):
            if skill.id == skill_id:
                self._skills.pop(i)
                return True
        return False


class BaseSkillPlugin(SkillPlugin):
    """Base implementation of a skill plugin"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self._skills: List[Skill] = []

    def register(self) -> None:
        """Register all skills in this plugin"""
        try:
            from src.skill_manager import SkillManager
            for skill in self._skills:
                SkillManager.register_skill(skill)
        except ImportError:
            pass  # SkillManager not available, skip registration

    def load_plugin(self) -> None:
        """Load the plugin"""
        super().load_plugin()
        self._load_skills()

    def _load_skills(self) -> None:
        """Internal method to load skills - to be implemented by subclasses"""
        pass

    def unload_plugin(self) -> None:
        """Unload the plugin"""
        super().unload_plugin()


class PluginManager:
    """Manages discovery, loading, and unloading of plugins"""
    
    def __init__(self):
        self._plugin_paths: List[str] = [
            "src/plugins",
            "plugins",
            os.path.expanduser("~/.assistant/plugins")
        ]
        self.plugins: Dict[str, SkillPlugin] = {}
        
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin paths"""
        plugins = []
        for path in self._plugin_paths:
            if os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        if item.endswith("_plugin.py"):
                            plugins.append(item[:-3])  # Remove .py extension
                except OSError:
                    continue
        return list(set(plugins))  # Remove duplicates

    def load_plugin(self, plugin_name: str) -> Optional[SkillPlugin]:
        """Load a plugin by name"""
        if plugin_name in self.plugins:
            return self.plugins[plugin_name]
            
        try:
            # Try to import the plugin module
            module = importlib.import_module(f"src.plugins.{plugin_name}")
            plugin_class = getattr(module, f"{plugin_name.capitalize()}Plugin")
            plugin_instance = plugin_class(plugin_name)
            self.plugins[plugin_name] = plugin_instance
            return plugin_instance
        except ImportError:
            logging.error(f"Failed to load plugin {plugin_name}")
            return None

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin by name"""
        if plugin_name not in self.plugins:
            return False
            
        plugin = self.plugins[plugin_name]
        try:
            plugin.unload_plugin()
            del self.plugins[plugin_name]
            return True
        except Exception:
            return False

    def register_plugin(self, plugin: SkillPlugin) -> bool:
        """Register a plugin with the system"""
        try:
            plugin.register()
            return True
        except Exception as e:
            logging.error(f"Failed to register plugin {plugin.name}: {e}")
            return False

    def get_plugin(self, name: str) -> Optional[SkillPlugin]:
        """Get a plugin by name"""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all loaded plugin names"""
        return list(self.plugins.keys())


def create_plugin(plugin_type: str, name: str) -> SkillPlugin:
    """Factory function to create plugin instances"""
    if plugin_type == "base":
        return BaseSkillPlugin(name)
    else:
        raise ValueError(f"Unknown plugin type: {plugin_type}")