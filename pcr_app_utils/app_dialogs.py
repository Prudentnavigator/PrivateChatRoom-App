#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
app_dialogs.py--module for "PrivateChatRoom-App to create and hide a
message box with an input field for user input.
'''

import sys
import tkinter
from tkinter import simpledialog
from pcr_app_utils.app_logging import app_log

logger = app_log(__name__)


def dialog():
    ''' Function to create a popup message box. '''

    msg_win = tkinter.Tk()
    msg_win.option_add('*Entry*background', 'lightgreen')
    msg_win.option_add('*font', 'Times')
    msg_win.withdraw()  # Hiding the window

    return msg_win


if __name__ == "__main__":
    win = dialog()
    TEXT = "Please enter an alias to test funcionality.\t\t"
    test = simpledialog.askstring("Test-app_dialogs.py",
                                  TEXT,
                                  parent=win)

    # If the user canceled or closed the window, log a message.
    if test is None:
        logger.info("[APP_DIALOGS_TEST]: user canceled test window.")
        sys.exit()

    logger.info("[APP_DIALOGS_TEST]: test successfull.")
