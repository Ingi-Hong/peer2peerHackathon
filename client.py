# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import sys
import socket
import threading
import urllib.request


class client: 
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SCOKET, socket.SO_REUSEADDR, 1)
        self.s.connect(host, port)

    #TODO:end connection with 'exit'
    def client_connect(s):
        while True:
            r_msg = s.recv(1024)
            if not r_msg:
                break
            if r_msg == '':
                pass
            else:
                print(r_msg.decode())

    def client_receive(s):
        while True:
            s_msg = input().replace('b', '').encode('utf-8')
            if s_msg == '':
                pass
            if s_msg.decode() == 'exit':
                print("wan exit")
                break
            else:
                s.sendall(s_msg)

class server: 
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SCOKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 6500))

        external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
        print(external_ip)


    def server_connect(self):

        self.s.listen() 

        while True:
            received = self.conn.recv(1024)
            if received ==' ':
                pass
            else:
                print(received.decode())

def init_client(host, port):
    print("usage: %s [ip adress][port] " % host)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((sys.argv[1], int(sys.argv[2])))
    thread1 = threading.Thread(target = client_connect, args = ([s]))
    thread2 = threading.Thread(target = client_receive, args = ([s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


def init_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('172.20.10.2', 49152))
    s.listen()
    (conn, addr) = s.accept() 
    thread1 = threading.Thread(target = server_connect, args = ([conn]))
    thread2 = threading.Thread(target = server_sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == '__main__':
    
    thread_c = threading.Thread(target=init_client, args = ())
