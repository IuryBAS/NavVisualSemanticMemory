from .basemodel import BaseModel
from .gcn_mlp import GCN_MLP
from .gcn_lstm import GCN
from .gcn_gru import GCN_GRU

__all__ = ["BaseModel", "GCN_MLP", "GCN", "GCN_GRU"]

variables = locals()
