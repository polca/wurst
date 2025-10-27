# -*- coding: utf-8 -*-
import logging
import os
import time
import uuid
from pathlib import Path

import platformdirs
from pythonjsonlogger import jsonlogger


def create_dir(dirpath):
    """Create directory tree to `dirpath`; ignore if already exists"""
    path = Path(dirpath)
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)
    return dirpath


def check_dir(directory):
    """Returns ``True`` if given path is a directory and writeable, ``False`` otherwise."""
    path = Path(directory)
    return path.is_dir() and os.access(path, os.W_OK)


def get_base_directory():
    """Return base directory where cache and output data are saved.

    Creates directory if it is not already present."""
    return create_dir(platformdirs.PlatformDirs("Wurst", "WurstTeam").user_data_dir)


def get_uuid():
    return uuid.uuid4().hex


def get_log_filepath(run_id):
    """Get filepath for Wurst run log"""
    return Path(get_base_directory()) / (run_id + ".wurst.log")


def create_log(run_id=None):
    """Create and setup a JSON logger"""
    if not run_id:
        run_id = get_uuid()
    filepath = get_log_filepath(run_id)

    logger = logging.getLogger("wurst")
    logger.propagate = False
    handler = logging.FileHandler(filepath, encoding="utf-8")
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return run_id, filepath


def cleanup_data_directory():
    base_dir = Path(get_base_directory())
    one_week, now, to_delete = 7 * 24 * 60 * 60, time.time(), []

    print("\nCleaning up data directory {}".format(base_dir))
    is_sausage = lambda x: x.endswith(".wurst.log")
    for file in filter(is_sausage, os.listdir(base_dir)):
        filepath = base_dir / file
        created = os.path.getctime(str(filepath))
        if created < now - one_week:
            to_delete.append(filepath)

    if not to_delete:
        print("\nNo old runs to delete!\n")
        return

    to_delete.sort()
    print("Deleting {count} runs".format(len(to_delete)))

    for filepath in to_delete:
        Path(filepath).unlink()
