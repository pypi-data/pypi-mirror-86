import os
from typing import Protocol
from torch.utils.data import Dataset
from torch.utils.data.dataloader import DataLoader
from torch.nn import Module


class FileDelegate:
    def __init__(self, parent: str):
        self.parent = parent

    def provide(self, file: str):
        """Provide the full path

        Args:
            file (str): destination file

        Returns:
            [str]: full path concat the parent and the file path
        """
        return os.path.join(self.parent, file)


class TrainingDelegate(Protocol):
    def train_one_epoch(self, model: Module, dataloader: DataLoader): ...

    def valid_one_epoch(self, model: Module, dataloader: DataLoader): ...
