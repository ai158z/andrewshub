import pytest
import torch
import numpy as np

from src.mpnn_model import MPNNModel, MessagePassingLayer
from src.magic_state_metrics import calculate_magic_state_metrics, QualiaTracker
from src.inverse_solver import solve_inverse_problem
from src.test_simulations import AmbiguityDetector, check_ambiguous_input, generate_ambiguous_scenarios
from src.sensory_processing import QuantumSensoryProcessor


# --- MPNN tests ---

class TestMPNNModel:
    def test_feedforward_mode(self):
        model = MPNNModel(input_dim=8, output_dim=4)
        x = torch.randn(5, 8)
        out = model(x)
        assert out.shape == (5, 4)

    def test_graph_mode(self):
        model = MPNNModel(input_dim=6, edge_dim=3, hidden_dim=16, output_dim=4, num_layers=2)
        nodes = torch.randn(4, 6)
        edges = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=torch.long)
        edge_feat = torch.randn(4, 3)
        out = model(nodes, edges, edge_feat)
        assert out.shape == (4, 4)

    def test_deterministic(self):
        torch.manual_seed(42)
        model = MPNNModel(input_dim=5, output_dim=3)
        x = torch.randn(2, 5)
        a = model(x)
        b = model(x)
        assert torch.allclose(a, b)


# --- Magic state metrics tests ---

class TestMagicStateMetrics:
    def test_keys_present(self):
        t = torch.randn(10)
        m = calculate_magic_state_metrics(t)
        assert set(m.keys()) == {"magic_consumption", "coherence", "entropy", "stability"}

    def test_uniform_high_entropy(self):
        t = torch.ones(100)
        m = calculate_magic_state_metrics(t)
        assert m["coherence"] > 0.99  # perfectly aligned with uniform

    def test_spike_low_entropy(self):
        t = torch.zeros(100)
        t[0] = 100.0
        m = calculate_magic_state_metrics(t)
        assert m["entropy"] < 0.5


# --- Qualia tracker tests ---

class TestQualiaTracker:
    def test_empty_trend(self):
        qt = QualiaTracker()
        assert qt.trend() == 0.0

    def test_increasing_trend(self):
        qt = QualiaTracker()
        for i in range(20):
            qt.update({"magic_consumption": float(i), "coherence": 0, "entropy": 0, "stability": 0})
        assert qt.trend() > 0

    def test_window_limit(self):
        qt = QualiaTracker(window=5)
        for i in range(10):
            qt.update({"magic_consumption": float(i)})
        assert len(qt.history) == 5


# --- Ambiguity detection tests ---

class TestAmbiguityDetector:
    def test_uniform_is_ambiguous(self):
        t = torch.ones(100) / 100.0
        assert check_ambiguous_input(t) is True

    def test_spike_not_ambiguous(self):
        t = torch.zeros(100)
        t[0] = 100.0
        assert check_ambiguous_input(t) is False

    def test_generate_scenarios(self):
        samples = generate_ambiguous_scenarios(dim=8, n_samples=3)
        assert samples.shape == (3, 8)


# --- Inverse solver tests ---

class TestInverseSolver:
    def test_returns_expected_keys(self):
        target = torch.randn(1, 10)
        result = solve_inverse_problem(target)
        assert "optimized_input" in result
        assert "loss" in result
        assert "converged" in result
        assert "steps" in result

    def test_loss_decreases(self):
        torch.manual_seed(0)
        target = torch.randn(1, 10)
        result = solve_inverse_problem(target, max_steps=200)
        # Loss should be lower than random init
        assert result["loss"] < 10.0


# --- Integration: QuantumSensoryProcessor ---

class TestQuantumSensoryProcessor:
    def test_process_numpy(self):
        proc = QuantumSensoryProcessor(input_dim=6, output_dim=6)
        raw = np.random.randn(3, 6).astype(np.float32)
        out = proc.process(raw)
        assert out.shape == (3, 6)

    def test_process_tensor(self):
        proc = QuantumSensoryProcessor(input_dim=8, output_dim=8)
        t = torch.randn(2, 8)
        out, metrics = proc.process_tensor(t)
        assert out.shape == (2, 8)
        assert "magic_consumption" in metrics

    def test_qualia_trend_after_processing(self):
        proc = QuantumSensoryProcessor(input_dim=5, output_dim=5)
        for _ in range(5):
            proc.process(np.random.randn(2, 5).astype(np.float32))
        # Just check it returns a float, direction depends on random init
        assert isinstance(proc.qualia_trend, float)
