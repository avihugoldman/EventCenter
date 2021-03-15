import struct
import logging
from socket import *


class Massage:
    def __init__(self, args):
        self.args = args
        self.client = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        print(f"Open socekt: [{self.args['ADDR']}]")
        self.client.connect(self.args["ADDR"])

    def recv_msg(self, sock):
        """
        :return: Read message length and unpack it into an integer
        """
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        """
        :return: Helper function to recv n bytes or return None if EOF is hit
        """
        data = bytearray()
        while len(data) < n:
            try:
                sock.settimeout(self.args["MASSAGE_TIMEOUT"])
            except IndexError:
                sock.settimeout(0.07)
            try:
                packet = sock.recv(n - len(data))
            except timeout:
                return None
            if not packet:
                return None
            data.extend(packet)
        return data

    def handle_massage(self):
        # time.sleep(0.05)
        massage = self.recv_msg(self.client)
        # # logging.warning(f"massage read in {time.time()}")
        massage = str(massage)
        massage = massage.strip("bytearray(b'{" "}')")
        if self.args["DEBUG"]:
            logging.debug(massage)
        list_of_strings = massage.split("|")
        if self.args["DEBUG"]:
            logging.debug(list_of_strings)
        return list_of_strings
