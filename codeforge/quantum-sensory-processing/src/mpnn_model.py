```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

logger = logging.getLogger(__name__)


class MPNNModel(nn.Module):
    def __init__(self, input_dim: int, edge_dim: int, hidden_dim: int, output_dim: int, num_layers: int = 2):
        """
        Message Passing Neural Network (MPNN) model for sensorimotor alignment.

        Args:
            input_dim (int): Dimension of input node features.
            edge_dim (int): Dimension of edge features.
            hidden_dim (int): Dimension of hidden node features.
            output_dim (int): Dimension of output features.
            num_layers (int): Number of message passing layers.
        """
        super().__init__()
        self.input_dim = input_dim
        self.edge_dim = edge_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers

        # Initial node embedding layer
        self.node_emb = nn