from torch.utils.data import DataLoader, Dataset
from typing import Literal, Union, List, Tuple
import torch

RETURN_TYPES = Literal['dict', 'tuple']

TL = Union[List, Tuple]


def debug_dataset(dataset: Dataset):
    r"""
    Debug dataset; observing each output.

    :param dataset: dataset for debug
    """
    dataloader = DataLoader(dataset=dataset, batch_size=1)
    for i, batch in enumerate(dataloader):
        if i == 1:
            return
        assert batch is not None, f"dataset __get__(index) return None"
        if isinstance(batch, tuple) or isinstance(batch, list):
            print(f"Return {len(batch)} data.")
            for e, j in enumerate(batch):
                if isinstance(j, torch.Tensor):
                    print(f"the {e}-th batch is tensor with shape {j.shape}")
                else:
                    print(f"the {e}-th batch {j=}")
        elif isinstance(batch, dict):
            for k, v in batch.items():
                print(f"Key {k} with Value type{type(v)}")
                if isinstance(v, torch.Tensor):
                    print(f"Tensor value with shape {v.shape}")

