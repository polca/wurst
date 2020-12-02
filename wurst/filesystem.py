# -*- coding: utf-8 -*-
from pythonjsonlogger import jsonlogger
import appdirs
import logging
import os
import time
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
    return create_dir(appdirs.user_data_dir("Wurst", "WurstTeam"))


def get_uuid():
    return uuid.uuid4().hex


def get_log_filepath(run_id):
    """Get filepath for Wurst run log"""
    return os.path.join(get_base_directory(), run + ".wurst.log")


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
    base_dir = get_base_directory()
    one_week, now, to_delete = 7 * 24 * 60 * 60, time.time(), []

    print("\nCleaning up data directory {}".format(base_dir))
    is_sausage = lambda x: x.endswith(".wurst.log")
    for file in filter(is_sausage, os.listdir(base_dir)):
        filepath = os.path.join(base_dir, file)
        created = os.path.getctime(filepath)
        if created < now - one_week:
            to_delete.append(filepath)

    if not to_delete:
        print("\nNo old runs to delete!\n")
        return

    to_delete.sort()
    print("Deleting {count} runs".format(len(to_delete)))

    for filepath in to_delete:
        os.remove(filepath)
