## <ins>PrivateChatRoom-App v1.1.2</ins>

This application allows users to communicate privately in real time.\
It is designed to be used with the "PrivateChatRoom-Server".\
As long as python3 is installed on your device, this program can be used with any 
operating system, (Windows, Mac, Linux, etc.).\

### Usage:
1. Assure that your device is connected to the internet and the server is
    running.
2. When starting the program (run gui_client.py from the terminal), a pop-up window will request an alias (username).
3. Set the IPv4 address of the server and the port number (click on the
    respective buttons) that the server is listening on.
   If the the App was previously connected to the server and the IPv4/port
    have not changed, this step won't be neccessary.
4. Enter a message in the box below 'Message' and click the 'Send' button.
5. Click 'X' on top-right corner of the window to exit the program.

### Requirements:
- python3.10 or higher version (may also work with lower versions).
- Tkinter and all modules used in the App should already be part of the
   python3 installation therefore eliminating the need to install any
   external packages or modules.

[!NOTE]
>The color of the App is red if there is no internet connection and/or
    the App is not connected to the server.\
>When a connection with the server is established the color of the App is green.\
>The App logs info for troubleshooting purposes only and does not log messages
    that have been send or received.
    Once the App is closed, the messages disappear.\
[!TIP]
>The application can also be packaged with pyinstaller or other packaging
    software to a standalone executable.\

[!CAUTION]
>The messages are not encrypted in this version.

### Features:
- Logs are written to the '.client.log' file on a rotating bases (max 3 files).
- Ipv4 address and port number used to connect to the server are displayed
   in the GUI.
- Set ipv4 address button to change the ip address.
- Set port button to change the port number.
- A display that indicates the amount of users in the chat.
- A scrolled text field that display's the messages in the chat.
- An entry field for the messages.
- A send button for sending the messages.

If you have any questions/recommendations or want to report a bug you can reach
 me by email (tommy_software@mailfence.com).

  

