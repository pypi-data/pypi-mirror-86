from torch import nn, Tensor
import torch
from typing import Optional


class Dense(nn.Module):
    def __init__(self, out_features: int = 1, bias: bool = True):
        super(Dense, self).__init__()
        self.out_features = out_features
        if bias:
            self.bias = nn.Parameter(data=torch.randn(out_features))
        else:
            self.bias = None

        self._weights: Optional[torch.nn.Parameter] = None

    @property
    def weights(self):
        return self._weights

    def forward(self, inputs: Tensor):
        in_features = inputs.shape[-1]
        if self._weights is None:
            self._weights = nn.Parameter(data=torch.randn((self.out_features, in_features)))
        if self.bias is not None:
            return nn.functional.linear(input=inputs, weight=self.weights, bias=self.bias)
        else:
            return nn.functional.linear(input=inputs, weight=self.weights)

    def __call__(self, inputs: Tensor):
        return self.forward(inputs)


if __name__ == '__main__':
    linear = Dense(out_features=5)
    input_1 = torch.randn((128, 25, 64))
    input_2 = torch.randn((128, 16, 16, 64))
    x1 = linear(input_1)  # [128, 25, 5]
    # x2 = linear(input_2)
    y1 = torch.randn(size=x1.size())
    loss = nn.functional.mse_loss(input=x1, target=y1)
    loss.backward()
    x2 = linear(input_1)  # [128, 25, 5]
    # x2 = linear(input_2)
    y2 = torch.randn(size=x1.size())
    loss = nn.functional.mse_loss(input=x2, target=y2)
    loss.backward()
