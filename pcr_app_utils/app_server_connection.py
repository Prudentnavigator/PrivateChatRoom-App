#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
app_server_connection.py--a module to connect 'PrivateChatroom' to the
               'PrivateChatRoom-Server'.
               It also provides functions to alter the IPv4 address
               and port to be used.
'''

from tkinter import simpledialog
import socket
from pcr_app_utils.app_dialogs import dialog
from pcr_app_utils.app_logging import app_log

logger = app_log(__name__)


def connect_to_server(host, port):
    ''' Function to connect to the server. '''

    try:
        # Creating socket.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a time limit for the connection to establish.
        sock.settimeout(2)

        # Connecting to the server and log attempt.
        logger.info(" trying to connect to the server...")
        sock.connect((host, port))

        # When connectionn is established, cancel time limit.
        sock.settimeout(None)

        # Log successfull connection.
        logger.info(" connected to %s:%s", host, port)

        return {"conn": True,
                "sock": sock,
                "host": host,
                "port": port,
                "inet": True}

    except ConnectionRefusedError:
        # Error message if server is not running.
        logger.warning(" could not connect to the server!")
        msg = "verify that the server is running and ip/port are correct!"
        logger.error(" %s", msg)
        return {"conn": False,
                "sock": None,
                "host": host,
                "port": port,
                "inet": True}

    except OSError:
        # Error message if there is no internet connection.
        host, port = get_ip_port()
        logger.warning(" could not connect to the server!")
        error_msg = "are you connected to the internet?"
        logger.error(" %s", error_msg)
        return {"conn": False,
                "sock": None,
                "host": host,
                "port": port,
                "inet": False}


def get_ip_port():
    '''
    Function that returns the IPv4 address and the port.
    If the .pcr_ip_port.txt does not exist, a new file is created
      with default values.
    '''

    try:
        with open(".pcr_ip_port.txt", "r", encoding="utf-8") as infile:
            for line in infile:
                values = line.split(",")
                ip_addr = values[0]
                port = values[1]

                return ip_addr, port

    except FileNotFoundError:
        with open(".pcr_ip_port.txt", "w", encoding="utf-8") as outfile:
            ip_addr = "127.0.0.1"
            port = 5050
            values = f"{ip_addr},{port}"

            outfile.write(values)

            return ip_addr, port


def set_ip():
    ''' Methode to create a window to set the ipv4_address. '''

    msg_win = dialog()

    win_text = "\tPlease enter the ipv4 address\t\t"

    while True:
        # Getting user's name
        ipv4 = simpledialog.askstring("PrivateChatRoom",
                                      win_text,
                                      parent=msg_win)

        # If the user canceled or closed the window, return the previous ip.
        if ipv4 is None:
            return get_ip_port()

        try:
            # Verify that the ip entered is a valid ipv4 address.
            if socket.inet_aton(ipv4):
                break
        except OSError:
            win_text = "\tPlease enter a valid ipv4 address\t\t"

    with open(".pcr_ip_port.txt", "r", encoding="utf-8") as infile:
        for line in infile:
            values = line.split(",")
            port = values[1]

    with open(".pcr_ip_port.txt", "w", encoding="utf-8") as outfile:
        ip_addr = ipv4
        values = f"{ip_addr},{port}"
        outfile.write(values)
        logger.info(" ipv4 address has been changed to %s",
                    ip_addr)

    return ip_addr, port


def set_port():
    ''' Methode to create a window to set the port number. '''

    msg_win = dialog()

    win_text = "\tPlease enter the port number\t\t"

    while True:
        port = simpledialog.askstring("PrivateChatRoom",
                                      win_text,
                                      parent=msg_win)

        # If the user canceled or closed the window, return the previous port.
        if port is None:
            return get_ip_port()

        # Check that the port number entered are digits.
        if not port.isdigit():
            win_text = "Port must be numbers!\t\t"
            continue

        # If the user entered a port that is too high, let them know.
        if int(port) > 65535:
            win_text = "Max port number is 65535\t\t"
        else:
            break

    with open(".pcr_ip_port.txt", "r", encoding="utf-8") as infile:
        for line in infile:
            values = line.split(",")
            ip_addr = values[0]

    with open(".pcr_ip_port.txt", "w", encoding="utf-8") as outfile:
        values = f"{ip_addr},{port}"
        outfile.write(values)
        logger.info(" port number has been changed to %s.",
                    port)

    return ip_addr, port


def main():
    ''' Test for functionality '''

    ip_addr, port = get_ip_port()
    logger.info("[TEST]: ip-address: %s and port: %s", ip_addr, port)
    connection = connect_to_server(ip_addr, int(port))
    logger.info("[TEST]: testing socket %s", connection)


if __name__ == "__main__":
    main()
