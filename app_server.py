""" Main server code for Socket Audio Player.
"""

###########
# Imports #
###########
# Import server packages
import socket
import selectors
import traceback

# Import custom modules
import libserver


class Server:
    def __init__(self, host=None, port=None):
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
            while True:
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
        message = libserver.Message(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
