# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import logging
import sys
import socket
import threading
import urllib.request
import sqlite3


class client:
    def __init__(self, hostPortTuple):
        # open the database, or create it if it doesn't exist
        self.db = sqlite3.connect("receivers.db")
        self.cur = self.db.cursor()

        # If the database is new, we need to create the tables. 
        # Check if the tables exist, create if not
        ListReceivers = self.cur.execute(
            """SELECT name FROM sqlite_master 
            WHERE type='table' AND name='RECEIVERS'; """).fetchall()
        
        ListMessages = self.cur.execute(
            """SELECT name FROM sqlite_master 
            WHERE type='table' AND name='MESSAGES'; """).fetchall()
        
        if ListReceivers == []:
            logging.info("Receivers not found")
            self.cur.execute('''CREATE TABLE RECEIVERS
                (ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL);''')
            logging.info("Receivers table created")
        else:
            logging.info("Receivers found")
            
        if ListMessages == []:
            logging.info("Messages not found")
            self.cur.execute('''CREATE TABLE MESSAGES
                (TO         TEXT         NOT NULL,
                MESSAGE     TEXT        NOT NULL,
                TIME        TEXT        NOT NULL,
                ISSENT      INT         NOT NULL);''')
            logging.info("Messages table created")
        else:
            logging.info("Messages found")
         
        try:
            logging.info("client __init__: Connecting to socket")
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect(hostPortTuple)
        except Exception as e:
            print(e)
            print(f"Connection invalid, messages sent to {hostPortTuple[0]} will be pending until connection is successful")
            exit(1)

    def client_send(self):
        while True:
            s_msg = input().encode('utf-8')
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
            self.s.bind(('', port))
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
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # my_server = server()

    # external_ip = urllib.request.urlopen(
    #     'https://v4.ident.me/').read().decode('utf8')
    # print("Tell your friend to connect to: " + external_ip)

    # serverThread = threading.Thread(
    #     target=my_server.server_loop)
    
    # serverThread.start()

    ip_address = input("Enter your friends ip_address: ")
    port = input("Enter your friends port: ")
    hostPortTuple = (ip_address, int(port))

    logging.info("Creating client object")
    my_client = client(hostPortTuple)

    clientThread = threading.Thread(
        target=my_client.client_loop)
    
    logging.info("Starting clientThread")
    clientThread.start()
    # serverThread.join()
    clientThread.join()
