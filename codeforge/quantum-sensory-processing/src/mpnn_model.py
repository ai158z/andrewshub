import torch
import torch.nn as nn
import torch.nn.functional as F
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MessagePassingLayer(nn.Module):
    """Single message-passing layer: aggregate neighbor messages then update node states."""

    def __init__(self, node_dim: int, edge_dim: int, hidden_dim: int):
        super().__init__()
        self.message_fn = nn.Sequential(
            nn.Linear(2 * node_dim + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.update_fn = nn.GRUCell(hidden_dim, node_dim)

    def forward(
        self,
        node_features: torch.Tensor,
        edge_index: torch.Tensor,
        edge_features: torch.Tensor,
    ) -> torch.Tensor:
        src, dst = edge_index
        src_feat = node_features[src]
        dst_feat = node_features[dst]
        messages = self.message_fn(torch.cat([src_feat, dst_feat, edge_features], dim=-1))

        agg = torch.zeros(node_features.size(0), messages.size(-1), device=node_features.device)
        agg.index_add_(0, dst, messages)

        return self.update_fn(agg, node_features)


class MPNNModel(nn.Module):
    """Message-Passing Neural Network for sensorimotor alignment.

    Nodes represent sensor/actuator channels; edges encode spatial or
    functional relationships between them.  When called without graph
    structure it falls back to a simple feed-forward path.
    """

    def __init__(
        self,
        input_dim: int = 10,
        edge_dim: int = 4,
        hidden_dim: int = 32,
        output_dim: int = 10,
        num_layers: int = 3,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.node_encoder = nn.Linear(input_dim, hidden_dim)
        self.layers = nn.ModuleList(
            [MessagePassingLayer(hidden_dim, edge_dim, hidden_dim) for _ in range(num_layers)]
        )
        self.readout = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(
        self,
        node_features: torch.Tensor,
        edge_index: Optional[torch.Tensor] = None,
        edge_features: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Forward pass.  Without graph structure treats input as independent vectors."""
        if edge_index is None:
            h = F.relu(self.node_encoder(node_features))
            return self.readout(h)

        h = self.node_encoder(node_features)
        for layer in self.layers:
            h = layer(h, edge_index, edge_features)
        return self.readout(h)
