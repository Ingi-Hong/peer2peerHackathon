# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import sys
import socket
import threading
import urllib.request


class client:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect(host, port)

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
        senderThread = threading.Thread(target=self.client_send, args=([self]))
        senderThread.start()
        senderThread.join()


class server:
    def __init__(self, port=6500):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))

    def server_connect(self):
        while True:
            received = self.conn.recv(1024)
            if received == ' ':
                pass
            else:
                print(received.decode())

    def server_loop(self):
        self.s.listen()
        (self.conn, self.addr) = self.s.accept()
        listenerThread = threading.Thread(
            target=self.server_connect, args=([self]))
        listenerThread.start()
        listenerThread.join()


if __name__ == '__main__':
    my_server = server()

    external_ip = urllib.request.urlopen(
        'https://v4.ident.me/').read().decode('utf8')
    print("Tell your friend to connect to: " + external_ip)

    serverThread = threading.Thread(
        target=my_server.server_loop, args=([my_server]))

    ip_address = input("Enter your friends ip_address: ")
    port = input("Enter your friends port: ")
    my_client = client(ip_address, int(port))

    clientThread = threading.Thread(
        target=my_client.client_loop, args=([my_client]))
