import torch
import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class QualiaSnapshot:
    """A single qualia measurement at a point in time."""
    magic_consumption: float
    coherence: float
    entropy: float
    stability: float
    timestamp: float = 0.0


class QualiaTracker:
    """Tracks magic-state consumption over time as a proxy for qualia intensity.

    The hypothesis: higher magic-state resource usage during processing
    correlates with richer subjective experience (qualia).  This tracker
    maintains a rolling history and can compute trends.
    """

    def __init__(self, window: int = 100):
        self.window = window
        self.history: List[QualiaSnapshot] = []
        self._step = 0

    def update(self, metrics: Dict[str, float]) -> None:
        snap = QualiaSnapshot(
            magic_consumption=metrics.get("magic_consumption", 0.0),
            coherence=metrics.get("coherence", 0.0),
            entropy=metrics.get("entropy", 0.0),
            stability=metrics.get("stability", 0.0),
            timestamp=float(self._step),
        )
        self.history.append(snap)
        if len(self.history) > self.window:
            self.history = self.history[-self.window:]
        self._step += 1

    def trend(self) -> float:
        """Return slope of magic_consumption over the window (positive = increasing qualia)."""
        if len(self.history) < 2:
            return 0.0
        vals = [s.magic_consumption for s in self.history]
        x = np.arange(len(vals), dtype=np.float64)
        slope = float(np.polyfit(x, vals, 1)[0])
        return slope

    @property
    def latest(self) -> Dict[str, float]:
        if not self.history:
            return {}
        s = self.history[-1]
        return {
            "magic_consumption": s.magic_consumption,
            "coherence": s.coherence,
            "entropy": s.entropy,
            "stability": s.stability,
        }


def calculate_magic_state_metrics(tensor: torch.Tensor) -> Dict[str, float]:
    """Derive magic-state metrics from a model output tensor.

    Metrics:
        magic_consumption — L1 norm (resource cost of producing this state)
        coherence — cosine similarity with a uniform vector (phase alignment)
        entropy — Shannon entropy of the softmax distribution
        stability — inverse coefficient of variation (higher = more stable)
    """
    with torch.no_grad():
        flat = tensor.detach().float().flatten()

        magic_consumption = float(flat.abs().sum())

        # Coherence: alignment with uniform superposition
        uniform = torch.ones_like(flat) / float(flat.numel())
        cos_sim = torch.nn.functional.cosine_similarity(flat.unsqueeze(0), uniform.unsqueeze(0))
        coherence = float(cos_sim.item())

        # Entropy of softmax distribution
        probs = torch.softmax(flat, dim=0).clamp(min=1e-12)
        entropy = float(-(probs * probs.log()).sum())

        # Stability: inverse CV
        mean_val = flat.mean()
        std_val = flat.std()
        stability = float(mean_val / std_val) if std_val > 1e-8 else float("inf")

    return {
        "magic_consumption": magic_consumption,
        "coherence": coherence,
        "entropy": entropy,
        "stability": stability,
    }
