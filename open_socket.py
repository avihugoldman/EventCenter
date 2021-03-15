import socket
import threading


class OpenSocket:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def receive_massage(self, conn, addr):
        while conn:
            data = conn.recv(1024).decode()
            if data:  # SEND ONLY WHEN NEW INFO IS RECEIVED
                print(data)
            else:
                break
        conn.close()
        # לנסות לסגור את ה Thread פה

    def server(self):
        print(f'Server started! On {self.host}:{self.port}')
        print('Waiting for clients...')
        self.server.bind((self.host, self.port))  # Bind to the port
        self.server.listen()  # Now wait for client connection.
        while True:
            conn, addr = self.server.accept()  # Establish connection with client.
            print(f'Got connection from {addr}')
            x = threading.Thread(target=self.receive_massage, args=(conn, addr)).start()
            # x.join() לברר לגבי זה
            if not x:
                break
        self.server.close()



