import json
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import dataclasses
from pathlib import Path


@dataclass
class Thresholds:
    """Configuration for analysis thresholds."""
    high: int = 10
    medium: int = 5
    low: int = 1


@dataclass
class Rule:
    """Configuration for a single rule."""
    id: str
    name: str
    description: str
    enabled: bool = True
    severity: str = "medium"
    category: str = "general"


@dataclass
class Config:
    """Main configuration class."""
    thresholds: Thresholds = field(default_factory=Thresholds)
    rules: List[Rule] = field(default_factory=list)
    
    def __post_init__(self):
        if not isinstance(self.thresholds, Thresholds):
            self.thresholds = Thresholds(**self.thresholds) if isinstance(self.thresholds, dict) else Thresholds()
        if not self.rules:
            self.rules = []
        elif isinstance(self.rules, list) and len(self.rules) > 0 and isinstance(self.rules[0], dict):
            self.rules = [Rule(**rule) for rule in self.rules]


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from a file.
    
    Args:
        config_path: Path to the configuration file. If None, returns default config.
        
    Returns:
        Config object with loaded settings.
        
    Raises:
        FileNotFoundError: If config file doesn't exist.
        ValueError: If config file format is invalid.
    """
    if not config_path:
        return Config()
    
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(path, 'r') as f:
            if path.suffix in ['.yml', '.yaml']:
                data = yaml.safe_load(f)
            elif path.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {path.suffix}")
    except Exception as e:
        raise ValueError(f"Error loading configuration file: {str(e)}")
    
    # Handle case where data is None
    if data is None:
        data = {}
    
    # Extract thresholds and rules from data
    thresholds_data = data.get('thresholds', {})
    rules_data = data.get('rules', [])
    
    # Create Config object
    config = Config(
        thresholds=Thresholds(**thresholds_data) if thresholds_data else Thresholds(),
        rules=[Rule(**rule) for rule in rules_data] if rules_data else []
    )
    
    return config


def create_default_config() -> Config:
    """Create a default configuration with standard rules."""
    return Config(
        thresholds=Thresholds(
            high=10,
            medium=5,
            low=1
        ),
        rules=[
            Rule(
                id="security-checks",
                name="Security Checks",
                description="Check for common security vulnerabilities",
                enabled=True,
                severity="high",
                category="security"
            ),
            Rule(
                id="style-checks",
                name="Style Checks",
                description="Check for code style violations",
                enabled=True,
                severity="medium",
                category="style"
            ),
            Rule(
                id="static-analysis",
                name="Static Analysis",
                description="Run static code analysis",
                enabled=True,
                severity="medium",
                category="static"
            )
        ]
    )