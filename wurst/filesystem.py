# -*- coding: utf-8 -*-
from pythonjsonlogger import jsonlogger
import appdirs
import logging
import os
import uuid


def create_dir(dirpath):
    """Create directory tree to `dirpath`; ignore if already exists"""
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    return dirpath


def check_dir(directory):
    """Returns ``True`` if given path is a directory and writeable, ``False`` otherwise."""
    return os.path.isdir(directory) and os.access(directory, os.W_OK)


def get_base_directory():
    """Return base directory where cache and output data are saved.

    Creates directory if it is not already present."""
    return create_dir(appdirs.user_data_dir("Wurst", "wurst_is_sausage"))


def get_log_filepath():
    """Get filepath for Wurst run log"""
    return os.path.join(get_base_directory(), uuid.uuid4().hex + ".log")


def create_log(filepath):
    """Create and setup a JSON logger"""
    logger = logging.getLogger('wurst')
    logger.propagate = False
    handler = logging.FileHandler(filepath, encoding='utf-8')
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
