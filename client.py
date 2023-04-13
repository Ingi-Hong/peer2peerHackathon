# https://stackoverflow.com/questions/56804394/python-p2p-1-to-1-chat-programming

import logging
import sys
import socket
import threading
import urllib.request
import sqlite3
from datetime import datetime as dt


class client:
    def __init__(self, name, hostPortTuple):
        self.name = name
        # open the database, or create it if it doesn't exist
        self.db = sqlite3.connect("receivers.db", check_same_thread=False)
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
                (ID             INT     PRIMARY KEY,
                NAME            TEXT    NOT NULL,
                IP              TEXT    NOT NULL,
                PORT            INT     NOT NULL);''')
            logging.info("Receivers table created")
        else:
            logging.info("Receivers found")
            
        if ListMessages == []:
            logging.info("Messages not found")
            self.cur.execute('''CREATE TABLE MESSAGES
                (RECEIVER   TEXT        NOT NULL,
                MESSAGE     TEXT        NOT NULL,
                TIME        TEXT        NOT NULL,
                ISSENT      INT         NOT NULL);''')
            logging.info("Messages table created")
        else:
            logging.info("Messages found")
         
        try:
            logging.info("client __init__: Connecting to socket")
            self.offline = False
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect(hostPortTuple)
        except TimeoutError:
            print(f"Connection unsuccessful, Sending messages to {name} in offline mode")
            self.offline = True
            
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            exit(1)

    def client_send(self):
        while True:
            s_msg = input(f"You: ").encode('utf-8')
            if self.offline:
                if s_msg.decode().upper() == 'EXIT':
                    print("Exiting offline mode")
                    return
                else:
                    sql_insert = '''INSERT INTO MESSAGES (RECEIVER, MESSAGE, TIME, ISSENT) 
                                    VALUES (?,?,?,?)'''
                
                    info = (self.name, s_msg, dt.isoformat(dt.now()), 0)
                    self.cur.execute(sql_insert, info)
                    self.db.commit()
            else:
                if s_msg == '':
                    pass
                if s_msg.decode().upper() == 'EXIT':
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
    
    db = sqlite3.connect("receivers.db")
    cur = db.cursor()

    # my_server = server()

    # external_ip = urllib.request.urlopen(
    #     'https://v4.ident.me/').read().decode('utf8')
    # print("Tell your friend to connect to: " + external_ip)

    # serverThread = threading.Thread(
    #     target=my_server.server_loop)
    
    # serverThread.start()
    
    ListReceivers = cur.execute("""SELECT NAME FROM RECEIVERS""").fetchall()

    print("Please pick a receiver from the list:")
    for receivers in ListReceivers:
        print(receivers[0])
    print("Create New")
    name = input("Receiver: ")

    if name.upper() == "CREATE NEW":
        logging.info("Creating a new row in RECEIVERS")
        sql = '''INSERT INTO RECEIVERS (NAME, IP, PORT) VALUES (?,?,?)'''

        r_name = input("What is the receiver's name: ")
        r_ip = input("Enter the receiver's ip_address: ")
        r_port = input("Enter the receiver's port: ")
        while(not r_port.isdigit()):
            print("ERROR! The port must be an integer")
            r_port = input("Enter the receiver's port: ")
        info = (r_name.upper(), r_ip, int(r_port))

        logging.info("Executing INSERT")
        cur.execute(sql, info)
        db.commit()
        logging.info("INSERT Committed")
    else:
        info = cur.execute(
            "SELECT NAME,IP,PORT FROM RECEIVERS WHERE NAME=?",
            (name.upper(),)
        ).fetchone()
    
    hostPortTuple = (info[1], int(info[2]))

    logging.info("Creating client object")
    my_client = client(info[0], hostPortTuple)

    clientThread = threading.Thread(
        target=my_client.client_loop)
    
    logging.info("Starting clientThread")
    clientThread.start()
    # serverThread.join()
    clientThread.join()