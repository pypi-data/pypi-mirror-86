from tap import Tap
from ..Foundation import *


class PretrainBase(Tap):
    path: str  # model path, required
    name: Optional[str]  # model name, optional
