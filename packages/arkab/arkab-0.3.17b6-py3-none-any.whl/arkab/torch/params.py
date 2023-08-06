import torch
import torch.nn as nn


def xavier(*shape, device: torch.device):
    """
    Return Tensor Param with shape `shape`
    """
    return nn.Parameter(nn.init.xavier_uniform_(torch.empty(shape, device=device)))


def unif(*shape, device: torch.device):
    return nn.Parameter(nn.init.uniform_(torch.empty(shape, device=device), -0.1, 0.1))


def fill(value, *shape, device: torch.device):
    return nn.Parameter(torch.empty(shape, device=device).fill_(value))
