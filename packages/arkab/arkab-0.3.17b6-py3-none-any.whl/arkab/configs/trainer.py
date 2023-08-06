from typing import Union

from tap import Tap


class TrainerConfigBase(Tap):
    parallel: bool = False  # set true to enable multi gpu
    debug: bool = False  # debug if TRUE
    gpus: str = '-1'  # set gpu, default is -1 for CPU
    valid_interval: int = 1
    epochs: int = 10  # training epochs
    max_epoch: int = 10
    min_epoch: int = 1

    @property
    def gpu(self) -> Union[int, str]:
        if self.parallel and int(self.gpus) != -1:
            return int(self.gpus)
        else:
            return self.gpus
