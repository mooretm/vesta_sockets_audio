""" Main server code for Socket Audio Player.
"""

###########
# Imports #
###########
# Import server packages
import socket
import selectors
import traceback

import tkinter as tk

# Import custom modules
#import server.libserver as libserver
from server import libserver


class Server(tk.Frame):

    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback
    

    def __init__(self, host=None, port=None, **kwargs):
        #super().__init__(parent, **kwargs)

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

        self.looping = 1

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
        print(f"Listening on {(self.host, self.port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            #while True:
            while self.looping == 1:
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
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()


    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"\nAccepted connection from {addr}")
        conn.setblocking(False)
        message = libserver.Message(self, self.sel, conn, addr)
        #self._event(message.event_to_send)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
