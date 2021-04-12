import socket
import threading
import pickle
import logging
import coloredlogs

coloredlogs.install(fmt='%(asctime)s.%(msecs)04d %(levelname)s %(message)s', datefmt='%H:%M:%S')


class OpenSocket:
    def __init__(self, args):
        self.args = args
        self.serverName = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.args["HOST"]
        self.port = self.args["PORT"]
        self.currMassage = []
        self.max_message_length = self.args["Max_Message_Size"] # 1024

    def receive_massage(self, conn):
        # maybe get it out to config \ args
        while conn:
            data = conn.recv(self.max_message_length)
            if len(data) < self.max_message_length:
                try:
                    self.currMassage = pickle.loads(data)
                except Exception as e:
                    # show me the error message and continue
                    logging.error(e)
                    continue
            else:
                # changed to continue from break, because want to take next message and not break from loop!
                continue
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
