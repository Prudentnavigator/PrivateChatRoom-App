#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
client.py--a GUI client app to be used with the 'PrivateChatRoom-Server'.
'''

import threading
import time
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import os
import sys
import app_server_connection
from app_dialogs import dialog
from app_logging import app_log

logger = app_log(__name__)

# Format in which we will encode/decode the data
FORMAT = "utf-8"


class Client():
    ''' The client GUI class. '''

    win = None
    gui_done = False

    def __init__(self, connected, alias=None):
        self.connected = connected
        self.widget = {"ip_label": None,
                       "port_label": None,
                       "ipv4_button": None,
                       "port_button": None,
                       "connections_text": None,
                       "text_area": None,
                       "msg_label": None,
                       "input_area": None,
                       "send_button": None,
                       "copy_label": None}

        if alias is None:
            # Get alias from the user.
            self.alias = Client.alias_win()
        else:
            self.alias = alias

        # Start the gui thread.
        self.start_threads()

    @staticmethod
    def alias_win():
        ''' Methode to create the alias window. '''

        msg_win = dialog()

        logger.debug(" alias is being requested.")

        # Getting user's name
        alias = simpledialog.askstring("PrivateChatRoom",
                                       "\t\tPlease enter your alias\t\t",
                                       parent=msg_win)

        # If the user canceled or closed the window, exit the program.
        if alias is None:
            logger.info(" program exited by the user.")
            sys.exit()

        logger.debug(" alias has been received.")

        return alias

    def start_threads(self):
        ''' Initiate a thread for the main GUI. '''

        # Creating a thread for GUI part.
        gui_thread = threading.Thread(target=self.gui_loop)

        # Creating another thread for receiving messages from server.
        receive_thread = threading.Thread(target=self.receive)

        # Starting the threads.
        gui_thread.start()
        receive_thread.start()

        logger.debug(" gui and receive threads have started.")

    def gui_loop(self):
        '''Method to create the main GUI'''

        # Creating the main window.
        Client.win = tkinter.Tk()
        Client.win.title("PrivateChatRoom-App v1.1.2")
        Client.win.geometry("685x780")

        # Create a frame.
        frame = tkinter.Frame(Client.win)

        # Set color variables for the background.
        green = "lightgreen"
        red = "#FF6347"

        if not self.connected["conn"]:
            Client.win.config(bg=red)
            frame.config(bg=red)
            status_color = red
        else:
            Client.win.config(bg=green)
            frame.config(bg=green)
            status_color = green

        # Call the gui_texts method which contains the text
        #   widgets for the GUI.
        self.gui_texts(frame)

        # Call the gui_labels which contains the GUI's labels.
        self.gui_labels(frame, status_color)

        # Call the gui_buttons methode which contains the GUI's buttons.
        self.gui_buttons(frame)

        # Call the gui_layout method which organizes the GUI layout.
        self.gui_layout()

        # Pack the frame
        frame.pack(expand=1)

        # Setting flag to true indicating GUI has been set up.
        Client.gui_done = True

        # Function to be called when user tries to close the window.
        Client.win.protocol("WM_DELETE_WINDOW", self.stop)

        logger.debug(" gui has been created.")

        Client.win.mainloop()

    def gui_texts(self, frame):
        ''' Text boxes for the GUI. '''

        # Add a textbox to display connections.
        self.widget["connections_text"] = tkinter.Text(frame,
                                                       height=1,
                                                       width=25,
                                                       bg="#f5f5f5",
                                                       fg="#ff4d04")

        self.widget["connections_text"].config(state="disabled")

        # Scrolled text area to display chat history
        self.widget["text_area"] = tkinter.scrolledtext.ScrolledText(
                                                           frame,
                                                           bg="#f5f5f5",
                                                           font=("italic",
                                                                 10))

        # Let the user know that the app is connected to the server.
        if self.connected["conn"]:
            msg = "\tconnected to the server...\n"
            self.widget["text_area"].insert("end", chars=msg)

        # If there is no internet connection, display a message.
        elif not self.connected["inet"]:
            msg = "\n\n\n\n\n\tcould not connect to the server...\n\n"
            msg1 = "\tPlease verify that you are connected to the internet!\n"
            self.widget["text_area"].insert("end", chars=msg)
            self.widget["text_area"].insert("end", chars=msg1)

        # Otherwise display a message to check server, ip/port.
        elif self.connected["inet"]:
            msg = "\n\n\n\n\n\tcould not connect to the server...\n\n"
            msg1 = "\tPlease verify that the server is running and that the"
            msg2 = " ip/port are correct!\n"
            self.widget["text_area"].insert("end", chars=msg)
            self.widget["text_area"].insert("end", chars=msg1+msg2)

        # Disabling the widget as we don't need to type here.
        self.widget["text_area"].config(state="disabled")

        # Text area where users can type messages.
        self.widget["input_area"] = tkinter.Text(frame,
                                                 height=2,
                                                 font=("italic", 10))

        logger.debug(" gui text widgets have been set-up.")

    def gui_labels(self, frame, status_color):
        ''' Contains labels for the GUI. '''

        ip_addr = f"ip: {self.connected['host']} "
        port = f"port: {self.connected['port']}"

        # Add a label for displaying ip_v4 in use.
        self.widget["ip_label"] = tkinter.Label(frame,
                                                text=ip_addr,
                                                bg=status_color)

        self.widget["ip_label"].config(font=("sans-serif", 15))

        # Add a label for displaying port in use.
        self.widget["port_label"] = tkinter.Label(frame,
                                                  text=port,
                                                  bg=status_color)

        self.widget["port_label"].config(font=("sans-serif", 15))

        # Label displaying 'Message'.
        self.widget["msg_label"] = tkinter.Label(frame,
                                                 text="Message: ",
                                                 bg=status_color)

        self.widget["msg_label"].config(font=("Times", 18))

        # Label to display the copyright.
        label_text = "Copyright\xa92024 Thomas Pirchmoser"
        self.widget["copy_label"] = tkinter.Label(frame,
                                                  text=label_text,
                                                  bg=status_color)

        self.widget["copy_label"].config(font=("Times", 9))

        logger.debug(" gui label widgets have been set-up.")

    def gui_buttons(self, frame):
        ''' Available buttons for the GUI. '''

        # Button to send message.
        self.widget["send_button"] = tkinter.Button(
                                            frame,
                                            text="Send",
                                            activebackground="lightblue",
                                            activeforeground="black",
                                            bd=8,
                                            relief="raised",
                                            command=self.send)

        self.widget["send_button"].config(font=("Times", 15), width=40)

        # Button to set the ip-address.
        self.widget["ipv4_button"] = tkinter.Button(
                                            frame,
                                            text="set ipv4 address",
                                            activebackground="lightblue",
                                            activeforeground="black",
                                            bd=8,
                                            relief="raised",
                                            command=self.change_ip)

        self.widget["ipv4_button"].config(font=("Times", 12), width=20)

        # Button to set the port.
        self.widget["port_button"] = tkinter.Button(
                                            frame,
                                            text="set port",
                                            activebackground="lightblue",
                                            activeforeground="black",
                                            bd=8,
                                            relief="raised",
                                            command=self.change_port)

        self.widget["port_button"].config(font=("Times", 12), width=20)

        logger.debug(" gui button widgets have been set-up.")

    def gui_layout(self):
        ''' Layout of the widgets in the GUI. '''

        self.widget["ip_label"].grid(row=0,
                                     column=0,
                                     sticky="w",
                                     padx=30,
                                     pady=5)

        self.widget["port_label"].grid(row=0,
                                       column=0,
                                       sticky="e",
                                       padx=50,
                                       pady=5)

        self.widget["ipv4_button"].grid(row=1,
                                        column=0,
                                        padx=25,
                                        pady=5,
                                        sticky="w")

        self.widget["port_button"].grid(row=1,
                                        column=0,
                                        padx=25,
                                        pady=5,
                                        sticky="e")

        self.widget["connections_text"].grid(row=2,
                                             column=0,
                                             pady=10)

        self.widget["text_area"].grid(row=4,
                                      column=0,
                                      padx=10,
                                      pady=5)

        self.widget["msg_label"].grid(row=5,
                                      column=0)

        self.widget["input_area"].grid(row=6,
                                       column=0,
                                       padx=20,
                                       pady=10)

        self.widget["send_button"].grid(row=7,
                                        column=0,
                                        pady=5)

        self.widget["copy_label"].grid(row=8)

        logger.debug(" gui layout has been set-up.")

    def send(self):
        ''' Method to send a message to the server'''

        try:
            # Constructing the message with user's alias and content.
            msg = self.widget['input_area'].get('1.0', 'end')
            msg = msg.strip()
            message = f"{self.alias}: {msg}\n"

            if self.connected["conn"]:
                # Sending it to server.
                self.connected["sock"].send(message.encode(FORMAT))

            # Clearing the input area.
            self.widget["input_area"].delete("1.0", "end")

        except OSError:
            logger.error("disconnected from the server...")

            # Let the user know the the server is disconnected.
            self.widget["text_area"].config(state="normal")
            msg = "\t\tdisconnected from the server...\n"
            self.widget["text_area"].insert("end", chars=msg)
            self.widget["text_area"].yview("end")
            self.widget["text_area"].config(state="disabled")

    def stop(self):
        ''' Method to be called when user wants to quit '''

        # Send a message to the server that the alias has left the chat.
        try:
            if self.connected["conn"]:
                msg = f"\t{self.alias} has left the chat...\n"
                self.connected["sock"].send(msg.encode(FORMAT))
        except BrokenPipeError:
            logger.info(" sever is offline...")

        # Setting the socket connection to false, so the receive loop will end.
        self.connected["conn"] = False

        Client.win.destroy()  # Closing the window.

        if self.connected["sock"]:
            self.connected["sock"].close()  # Closing the socket connection.
            logger.info(" disconnected from the server by the user.")

        logger.info("[STOP]: program closed by the user...")

        os._exit(0)  # Exiting program.

    def receive(self):
        ''' Method to receive a message from the server '''
        while self.connected["conn"]:
            try:
                # Receiving a message from the server.
                message = self.connected["sock"].recv(1024).decode(FORMAT)
                if message == "ALIAS":
                    # If server asks for alias, send it.
                    self.connected["sock"].send(self.alias.encode(FORMAT))

                connections_display = message[:1].isdigit() or \
                    message.endswith(" online...")

                if Client.gui_done and connections_display:
                    # Updating connections display.
                    # Enabling the text area to add message.
                    if self.widget["connections_text"]:
                        self.widget["connections_text"].config(state="normal")

                        # Clear the previous message.
                        self.widget["connections_text"].delete(1.0,
                                                               tkinter.END)

                        # Adding the newly received message.
                        self.widget["connections_text"].insert(1.0,
                                                               message)

                        # Disabling text area again as it's not for
                        #   user input.
                        self.widget["connections_text"].config(
                                                            state="disabled")

                if Client.gui_done and not connections_display:
                    # Updating chat display.
                    if self.widget["text_area"]:
                        self.widget["text_area"].config(state="normal")

                        # Insert the message as if typed.
                        for letter in message:
                            # Adding the newly received message.
                            self.widget["text_area"].insert("end",
                                                            letter)
                            time.sleep(0.07)

                            # Auto scroll down to see new messages.
                            self.widget["text_area"].yview("end")

                        self.widget["text_area"].config(state="disabled")

            except ConnectionAbortedError:
                # Log error message if connection is aborted.
                logger.error(" connection has been aborted!")
                break

            except IndexError:
                # Close the socket and log message.
                self.connected["sock"].close()
                logger.error(" disconnected from the server!")
                sys.exit()

    def change_ip(self):
        ''' The user can set the server's ipv4 address. '''

        # Disable the ipv4 button.
        self.widget["ipv4_button"].config(state="disabled",
                                          disabledforeground="green",
                                          relief="sunken")

        # Disable the port button.
        self.widget["port_button"].config(state="disabled",
                                          disabledforeground="black",
                                          relief="sunken")

        ip_addr, port = app_server_connection.set_ip()

        # Close socket connection.
        self.connected["conn"] = False
        if self.connected["sock"]:
            self.connected["sock"].close()
            logger.debug(" socket has been closed.")

        # Pass the updated IPv4 address, port and alias to the main().
        main(ip_addr, int(port), self.alias)

        Client.gui_done = False

    def change_port(self):
        ''' the user can set the server's port number. '''

        # Disable the port button.
        self.widget["port_button"].config(state="disabled",
                                          disabledforeground="green",
                                          relief="sunken")

        # Disable the ipv4 button.
        self.widget["ipv4_button"].config(state="disabled",
                                          disabledforeground="black",
                                          relief="sunken")

        ip_addr, port = app_server_connection.set_port()

        # Close socket connection.
        self.connected["conn"] = False
        if self.connected["sock"]:
            self.connected["sock"].close()
            logger.debug(" socket has been closed.")

        # Pass the updated port, IPv4 address and alias to the main().
        main(ip_addr, int(port), self.alias)

        Client.gui_done = False


def main(host, port, alias=None):
    ''' Main entry point. '''

    # On start-up of the App, an alias is not kown yet.
    if alias is None:
        connect = app_server_connection.connect_to_server(host, port)
        Client(connect)
    else:
        Client.win.destroy()
        logger.debug(" gui window has been destroyed.")

        connect = app_server_connection.connect_to_server(host, port)
        Client(connect, alias=alias)


if __name__ == "__main__":
    logger.info("[START]: program started by the user...")

    HOST, PORT = app_server_connection.get_ip_port()
    main(HOST, int(PORT))
