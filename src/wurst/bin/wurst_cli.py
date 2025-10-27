#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Wurst command line interface. See https://github.com/cmutel/wurst for more info.

Commands:

  * show: Launch an interactive web browser for a Wurst model run.
  * cleanup: Delete all model runs more than one week old.

Usage:
  wurst-cli show <run_id>
  wurst-cli cleanup
  wurst-cli -l | --list
  wurst-cli -h | --help
  wurst-cli --version

Options:
  -h --help          Show this screen.
  --version          Show version.

"""
from docopt import docopt
from wurst.filesystem import cleanup_data_directory
import os
import sys


def main():
    try:
        args = docopt(__doc__, version="Wurst CLI 0.1.dev")
        if args["cleanup"]:
            cleanup_data_directory()
        elif args["show"]:
            pass
        else:
            raise ValueError
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
