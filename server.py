# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import sys
import socket
import threading
import urllib.request


class client:
    def __init__(self, hostPortTuple):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect(hostPortTuple)
        except Exception as e:
            print(e)
            exit(1)

    def client_send(self):
        while True:
            s_msg = input().replace('b', '').encode('utf-8')
            if s_msg == '':
                pass
            if s_msg.decode() == 'exit':
                print("wan exit")
                break
            else:
                self.s.sendall(s_msg)

    def client_loop(self):
        senderThread = threading.Thread(target=self.client_send)
        senderThread.start()
        senderThread.join()


class server:
    def __init__(self, port=6500):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('127.0.0.2', port))
        except Exception as e:
            print(e)
            exit(1)    

    def server_connect(self):
        print("Server Accepted Connection")
        while True:
            received = self.conn.recv(1024)
            if received == ' ':
                pass
            else:
                print(received.decode())

    def server_loop(self):
        print("Server Waiting for Connection", self.s)
        self.s.listen()
        (self.conn, self.addr) = self.s.accept()

        listenerThread = threading.Thread(
            target=self.server_connect)
        listenerThread.start()
        listenerThread.join()


if __name__ == '__main__':
    my_server = server()

    external_ip = urllib.request.urlopen(
        'https://v4.ident.me/').read().decode('utf8')
    print("Tell your friend to connect to: " + external_ip)

    serverThread = threading.Thread(
        target=my_server.server_loop)
    
    serverThread.start()

    ip_address = input("Enter your friends ip_address: ")
    port = input("Enter your friends port: ")
    hostPortTuple = (ip_address, int(port))
    my_client = client(hostPortTuple)

    clientThread = threading.Thread(
        target=my_client.client_loop)
    
    clientThread.start()
    serverThread.join()
    clientThread.join()
