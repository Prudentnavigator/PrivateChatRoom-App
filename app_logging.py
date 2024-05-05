#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
app_logging.py--set up the logging for client.py.
'''

import logging
from logging import handlers


def app_log(__name__):
    ''' Set-up the logging object. '''

    # Get current logger instance with name of the module.
    logger = logging.getLogger(__name__)

    # Set log level to debug - higher than info.
    logger.setLevel(logging.DEBUG)

    # Create a formatter object with specified format for the logs.
    formatter = logging.Formatter(
                            '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                            "%Y-%m-%d %H:%M:%S")

    # Create file handler to handle log files rotation and backup.
    file_handler = handlers.RotatingFileHandler('.client.log',
                                                maxBytes=20000,
                                                backupCount=2)

    # Set formatter for the file handler object.
    file_handler.setFormatter(formatter)

    # Add file handler to logger instance.
    logger.addHandler(file_handler)

    return logger


# Calling the function and logging a message.
if __name__ == "__main__":
    log = app_log(__name__)
    log.info("[TEST] logging is set up.")
