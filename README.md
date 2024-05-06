PrivateChatRoom-App v1.0.0

This application allows users to communicate privately in real time
 using TCP socket programming in Python.
It is designed to be used with the 'PrivateChatRoom-Server'.

Usage:
1. Assure that your device is connected to the internet and the server is
    running.
2. When starting the program, a pop-up window will request an alias (username).
3. Set the IPv4 address of the server and the port number (click on the
    respective buttons) that the server is listening on.
   If the the App was previously connected to the server and the IPv4/port
    have not changed, this step won't be neccessary.
4. Enter a message in the box below 'Message' and click the 'Send' button.
5. Click 'X' on top-right corner of the window to exit the program.

Requirements:
- python3 or higher version required.
- Tkinter and all modules used in the App should already be part of the
   python3 installation therefore eliminating the need to install any
   external packages or modules.

Note:
1. The color of the App is red if there is no internet connection and/or
    the App is not connected to the server.
    ('no_internet.png' and 'not_connected_to_server.png')
3. When a connection with the server is established the color of the App is green.
    ('chat.png')
5. The App logs info for troubleshooting purposes only and does not log messages
    that have been send or received.
    Once the App is closed, the messages disappear.
6. Please note that the messages are not encrypted in this version.

Features:
- Logs are written to the '.client.log' file on a rotating bases (max 3 files).
- Ipv4 address and port number used to connect to the server are displayed
   in the GUI.
- Set ipv4 address button to change the ip address.
   ('set_ipv4_address.png')
- Set port button to change the port number.
   ('set_port.png')
- A display that indicates the amount of users in the chat.
- A scrolled text field that display's the messages in the chat.
- An entry field for the messages.
- A send button for sending the messages.
