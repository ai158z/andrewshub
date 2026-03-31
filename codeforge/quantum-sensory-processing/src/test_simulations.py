import torch
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class AmbiguityDetector:
    """Detects whether sensory input is ambiguous (high entropy / low confidence).

    An input is considered ambiguous when its normalized entropy exceeds a
    configurable threshold, meaning the signal carries roughly equal energy
    across many dimensions — the system can't tell what it's "looking at".
    """

    def __init__(self, entropy_threshold: float = 0.85, confidence_floor: float = 0.3):
        self.entropy_threshold = entropy_threshold
        self.confidence_floor = confidence_floor

    def analyze(self, tensor: torch.Tensor) -> Tuple[bool, float, float]:
        """Return (is_ambiguous, normalized_entropy, confidence)."""
        with torch.no_grad():
            flat = tensor.detach().float().flatten()
            probs = torch.softmax(flat, dim=0).clamp(min=1e-12)
            entropy = float(-(probs * probs.log()).sum())
            max_entropy = float(np.log(flat.numel())) if flat.numel() > 1 else 1.0
            normalized = entropy / max_entropy if max_entropy > 0 else 0.0
            confidence = float(probs.max())

        is_ambiguous = normalized > self.entropy_threshold and confidence < self.confidence_floor
        return is_ambiguous, normalized, confidence


def check_ambiguous_input(
    tensor: torch.Tensor,
    entropy_threshold: float = 0.85,
    confidence_floor: float = 0.3,
) -> bool:
    """Quick check: is this input ambiguous?"""
    detector = AmbiguityDetector(entropy_threshold, confidence_floor)
    is_ambiguous, _, _ = detector.analyze(tensor)
    return is_ambiguous

# Alias for backward compatibility
test_ambiguous_input = check_ambiguous_input


def generate_ambiguous_scenarios(
    dim: int = 10,
    n_samples: int = 5,
) -> torch.Tensor:
    """Generate synthetic ambiguous inputs (near-uniform distributions)."""
    base = torch.ones(n_samples, dim) / dim
    noise = torch.randn(n_samples, dim) * 0.01
    return base + noise
