import socket
import threading
import pickle


class OpenSocket:
    def __init__(self, args):
        self.args = args
        self.serverName = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.args["HOST"]
        self.port = self.args["PORT"]
        self.currMassage = []

    def receive_massage(self, conn):
        dict = {}
        while conn:
            data = conn.recv(1024)
            if data:  # SEND ONLY WHEN NEW INFO IS RECEIVED
                self.currMassage = pickle.loads(data)
                #print(self.currMassage)
            else:
                break
        conn.close()

        self.serverName.close()

    def server(self):
        print(f'Server started! On {self.host}:{self.port}')
        print('Waiting for clients...')
        self.serverName.bind((self.host, self.port))  # Bind to the port
        self.serverName.listen()  # Now wait for client connection.
        conn, addr = self.serverName.accept()  # Establish connection with client.
        print(f'Got connection from {addr}')
        x = threading.Thread(target=self.receive_massage, args=(conn,)).start()
