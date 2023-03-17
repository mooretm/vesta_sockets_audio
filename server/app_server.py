""" Main server code for Socket Audio Player.
"""

###########
# Imports #
###########
# Import server packages
import socket
import selectors
import traceback

# Import GUI packages
import tkinter as tk
from tkinter import messagebox

# Import system packages
import sys

# Import custom modules
#import server.libserver as libserver
from server import libserver


class Server:

    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback
    

    def __init__(self, audio_device, host=None, port=None, **kwargs):
        #super().__init__(parent, **kwargs)

        # Initialize values
        self.audio_device = audio_device

        # Assign host
        if not host:
            self.host = "127.0.0.1"
        else:
            self.host = host

        # Assign port
        if not port:
            self.port = 65432
        else:
            self.port = port

        # While loop control for server listening
        self.listening = 1

        # Create selector
        self.sel = selectors.DefaultSelector()

        # Start listening
        self._listen()


    def _listen(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print(f"\nappserver: Listening on {(self.host, self.port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while self.listening == 1:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                f"appserver: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("appserver: Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
            sys.exit()


    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('\n\nappserver: *** Begin Server Event ***')
        print(f"appserver: Accepted connection from {addr}")
        conn.setblocking(False)
        message = libserver.Message(self, self.sel, conn, addr, self.audio_device)
        #self._event(message.event_to_send)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
