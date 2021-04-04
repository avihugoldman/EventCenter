import socket
import json
import pickle
import random
import time
from queue import Queue

class Creator:
    def __init__(self):
        #, camera_number, frame_number, event_type, obj_sub_class, obj_id, top_left_rect, bottom_right_rect, algo_type):
        self.msg = {}
                    #'camera_number': camera_number, 'frame_number': frame_number,
                 # 'event_type': event_type, 'obj_sub_class': obj_sub_class, 'obj_id': obj_id, 'top_left_rect': top_left_rect,
                   # 'bottom_right_rect': bottom_right_rect, 'algo_name': algo_type}
        self.HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
        self.PORT = 5055
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.creat_connection()

    def creat_connection(self):
        try:
            self.client.connect((self.HOST, self.PORT))
            print("Connection")
        except Exception as e:
            #print(e, "Connection Refused!")
            pass

    def configuration(self):
        print("------ Loading JSON Event File ------\n")
        f = open("events.json", "r")
        data = json.loads(f.read())

    def send_dedctions(self, counter):
        try:
            if self.client:
                #client.send((data[f"{random.randint(0,3)}"]["name"]+" \n").encode()) #RANDOM OPTION
                self.rendomize_massage(counter)
                counter += 1
                msg_to_socket = pickle.dumps(self.msg)
                self.client.send(msg_to_socket)
                # print(self.msg)
                # bdata = bytes(data[f"{x}"]["name"], encoding="utf8")
                # client.send(bdata[f"{x}"]["name"]+" \n").encode()
        except BrokenPipeError:
            pass

    def rendomize_massage(self, counter):
        net = random.randrange(0, 4, 1)
        if net == 3:
            event, netName = 3, "anomaly"
        elif net == 2:
            event, netName = 1, "smoke_and_leakage"
        else:
            event, netName = 0, "persons"
        eventList = ["PERSONS", "SMOKE", "LEAKAGE", "ANOMALY", "DEAD_MAN_ALERT"]
        #currMsg = Creator(random.randrange(0, 9, 1), counter, eventList[event], random.randrange(0, 2, 1), 1, [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)], [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)], netName)
        self.msg["camera_number"] = random.randrange(0, 3, 1)
        self.msg["frame_number"] = counter
        self.msg["event_type"] = eventList[event]
        if self.msg["event_type"] == "PERSONS":
            self.msg["obj_sub_class"] = random.randrange(0, 3, 1)
        else:
            self.msg["obj_sub_class"] = -1
        self.msg["obj_id"] = 1
        self.msg["top_left_rect"] = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
        self.msg["bottom_right_rect"] = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
        self.msg["algo_name"] = netName
        #print(self.msg)


counter = 0
tmpCreator = Creator()
while True:
    time.sleep(0.04)
    tmpCreator.send_dedctions(counter)
    counter += 1
