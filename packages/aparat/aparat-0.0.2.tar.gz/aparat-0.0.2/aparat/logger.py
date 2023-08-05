import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_logger(name: str, level: int = logging.INFO, log_dir: str = str(Path.home())) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')

    # file logger
    log_path = os.path.join(log_dir, '{}.log'.format(name))
    handler_file = RotatingFileHandler(log_path, maxBytes=1024 * 100000, backupCount=10)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)

    return logger
