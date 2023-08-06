import arkab.nlp as nlp
from arkab.nlp.knowledge import KnowledgeKit
from arkab.delegates import FileDelegate

from arkab.trainer import Trainable
from typing import Literal
from .logging import logger

__all__ = ['nlp', 'Trainable', '__version__', 'version', 'KnowledgeKit', 'Foundation',
           'MODE', 'FileDelegate']

__version__ = '0.3.17beta5'

MODE = Literal['train', 'valid', 'test']


def version():
    return __version__
