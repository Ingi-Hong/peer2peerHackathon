# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import sys
import socket
import threading
import urllib.request
import logging


class server:
    def __init__(self, port=5000):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('127.0.0.1', port))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            exit(1)    

    def server_connect(self):
        print("Server Accepted Connection")
        while True:
            received = self.conn.recv(1024)
            if not received: 
                break
            if received == ' ':
                pass
            else:
                print(f"Message: {received.decode()}")

    def server_loop(self):
        print("Server Waiting for Connection", self.s)
        self.s.listen()
        (self.conn, self.addr) = self.s.accept()

        listenerThread = threading.Thread(
            target=self.server_connect)
        listenerThread.start()
        listenerThread.join()


if __name__ == '__main__':
    # Change logging level to INFO for runtime information
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.WARNING,
                        datefmt="%H:%M:%S")

    my_server = server()

    external_ip = urllib.request.urlopen(
        'https://v4.ident.me/').read().decode('utf8')
    print("Tell your friend to connect to: " + external_ip)

    serverThread = threading.Thread(
        target=my_server.server_loop)
    
    serverThread.start()
    
    serverThread.join()
