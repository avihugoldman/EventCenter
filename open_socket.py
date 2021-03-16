import socket
import threading


class OpenSocket:
    def __init__(self, args):
        self.args = args
        self.serverName = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.args["HOST"]
        self.port = self.args["PORT"]
        self.currMassage = str

    def receive_massage(self, conn):

        while conn:
            data = conn.recv(1024).decode()
            if data:  # SEND ONLY WHEN NEW INFO IS RECEIVED
                self.currMassage = data
                print(threading.active_count())
                if self.args["DEBUG"]:
                    print(data)
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
