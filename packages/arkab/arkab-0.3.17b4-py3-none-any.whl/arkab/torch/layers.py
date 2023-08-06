from typing import Literal, List, Callable

import torch
from torch.nn import functional as F

__all__ = ['Flatten', 'Embedding']


class Flatten(torch.nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, vec_t):
        return vec_t.view(vec_t.size(0), -1)

    __call__ = forward


class Embedding:
    def __init__(self, weights: torch.Tensor):
        assert len(weights.shape) == 2
        self.weights = weights

    def forward(self, idx: torch.Tensor):
        return F.embedding(input=idx, weight=self.weights)

    def __call__(self, inputs: torch.Tensor):
        return self.forward(idx=inputs)


AGGR = Literal['nil', 'sum', 'flat']


def calc_cnn_stack(inputs: tuple, call_chain: List[Callable], aggr: AGGR = 'flat'):
    h, w = inputs
    for c in call_chain:
        h, w = c(shape=(h, w))
    if aggr == 'nil':
        return h, w
    elif aggr == 'sum':
        return h + w
    else:
        # flat
        return h * w