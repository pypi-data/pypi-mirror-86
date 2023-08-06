import torch


class Embedding:
    def __init__(self, weights: torch.Tensor):
        assert len(weights.shape) == 2
        self.weights = weights

    def forward(self, idx: torch.Tensor):
        return F.embedding(input=idx, weight=self.weights)

    def __call__(self, inputs: torch.Tensor):
        return self.forward(idx=inputs)