import sys
import json
import logging
import logging.config
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def init_logger(name, log_dir, config_dir):
    config_dict = json.load(open(config_dir + 'config.json'))
    config_dict['handlers']['file_handler']['filename'] = log_dir + name.replace('.', '')
    logging.config.dictConfig(config_dict)
    _logger = logging.getLogger(name)

    std_out_format = '%(asctime)s - [%(levelname)s] - %(message)s'
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logging.Formatter(std_out_format))
    _logger.addHandler(consoleHandler)

    return _logger


def logger(filename: Optional[str] = None):
    FORMAT = "[line %(lineno)d] %(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(
            level="NOTSET",
            format=FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=filename
    )
    log = logging.getLogger("rich")
    log.addHandler(RichHandler())
    return log


def display_dict(src: dict):
    result = ""
    line_item_count = 0
    for k, v in src.items():
        if isinstance(v, float):
            result = result + f" {k}: {v:.4f}|"
        else:
            result = result + f" {k}: {v}|"
        line_item_count += 1
        if line_item_count % 4 == 0:
            result = result[:-1]
            print(result)
            result = ""


console = Console()

plog = console.log
