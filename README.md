# P2P Socket Communication Hackathon
## Group: Ingi Hong, Tristen Liu (tristenl@bu.edu)

The goal of this hackathon is to develop a Peer to Peer socket communication architecture that can communicate between two devices on different networks. 

This code currently only works on LOCALHOST (127.0.0.1) port 5000, and has offline messaging implemented via a local SQLite database. 

## Testing
To test normal message sending (both online):

1) Run server.py in one terminal, and client.py in a different terminal
2) In client.py, when prompted to select a receiver, type CREATE NEW (case insensitive) to create a new receiver
3) Name the new receiver whatever you want, then assign the ip to be `127.0.0.1` and the port number to be `5000`
4) The connection to the server from the client should begin, and messages should begin to transfer between terminals.

To test offline message sending:

1) First do not run server.py, and just run client.py
2) If steps 2-3 were followed in the online test, then the name if the previously created receiver should appear. Type that name to connect to the same receiver
3) Otherwise follow steps 2-3 in the online testing mode
4) Then, type whatever messages you want. These messages will be stored in an SQL table "MESSAGES", with ISSENT attribute set to 0.
5) Type 'exit' in order to close the client connection. 
6) To see if the messages sent, first open the server connection, then open the client connection and connect to the same receiver. We decided not to constantly ping the server in order to save computational efficiency.
7) The messages should appear in the server terminal, indicating the time the message was sent. 
