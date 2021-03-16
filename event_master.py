from camera import Camera
from detection import Detection
from open_socket import OpenSocket
from massage import Massage
from checker import Checker
from event import Event
from event import Events
import time
from socket import *
import socket
import json
from queue import Queue

class EventMaster:
    def __init__(self):
        self.args = {}
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.ADDR = tuple
        # self.ERRORS = self.is_print_on(self.ERRORS, self.args["list_of_words_mean_yes"])
        # self.WARNINGS = self.is_print_on(self.WARNINGS, self.args["list_of_words_mean_yes"])
        # self.INFO = self.is_print_on(self.INFO, self.args["list_of_words_mean_yes"])
        # self.DEBUG = self.is_print_on(self.DEBUG, self.args["list_of_words_mean_yes"])

    def read_camera_data_from_file(self, configName):
        """
        :param configName: name of config file
        :return: list of cameras with all the attributes.
        """
        f = open(configName, "r")
        line_list = [line for line in f]
        cameraList = []

        ACTIVE_CAMERAS_ID = self.str_to_camera_att(line_list, 1, 0)

        EVENT_TYPES = self.str_to_camera_att(line_list, 3, 2)

        SECONDS_TO_START_EVENT = self.str_to_camera_att(line_list, 5, 0)

        SIZE_OF_QUEUE = self.str_to_camera_att(line_list, 7, 0)

        TIMEOUT_AFTER_PUBLISH = self.str_to_camera_att(line_list, 9, 1)

        TIME_TO_CLOSE = self.str_to_camera_att(line_list, 11, 1)

        TIME_BETWEEN_EVENTS = self.str_to_camera_att(line_list, 13, 1)

        WATCHMAN_TIME = self.str_to_camera_att(line_list, 1, 1)

        MAX_SIZE_OF_MAN = self.str_to_camera_att(line_list, 17, 1)

        MIN_SIZE_OF_MAN = self.str_to_camera_att(line_list, 19, 1)

        START_INTREST_AREA_X = self.str_to_camera_att(line_list, 21, 1)

        END_INTREST_AREA_X = self.str_to_camera_att(line_list, 23, 1)

        START_INTREST_AREA_Y = self.str_to_camera_att(line_list, 25, 1)

        END_INTREST_AREA_Y = self.str_to_camera_att(line_list, 27, 1)

        DETECTION_RATIO = self.str_to_camera_att(line_list, 29, 1)

        for i in range(len(ACTIVE_CAMERAS_ID)):
            cameraList.append(Camera(self.args, ACTIVE_CAMERAS_ID[i], EVENT_TYPES[i], SECONDS_TO_START_EVENT[i], SIZE_OF_QUEUE[i],
                                      TIMEOUT_AFTER_PUBLISH[i], TIME_TO_CLOSE[i], TIME_BETWEEN_EVENTS[i],
                                      WATCHMAN_TIME[i], MAX_SIZE_OF_MAN[i],
                                      MIN_SIZE_OF_MAN[i], START_INTREST_AREA_X[i], END_INTREST_AREA_X[i],
                                      START_INTREST_AREA_Y[i],
                                      END_INTREST_AREA_Y[i], DETECTION_RATIO[i], DETECTION_RATIO[i], DETECTION_RATIO[i], DETECTION_RATIO[i]))
        f.close()
        return cameraList

    def read_camera_data_from_json(self):
        """
        :param configName: name of config file
        :return: list of cameras with all the attributes.
        """
        cameraList = []

        for i in range(len(self.args["camera_id"])):
            cameraList.append(
                Camera(self.args, self.args["camera_id"][i], self.args["event_in_camera"][i], self.args["Ts"][i],
                       self.args["Nd"][i], self.args["Tf"][i], self.args["Tc"][i], self.args["Ti"][i],
                       self.args["Tw"][i], self.args["Hmax"][i], self.args["Hmin"][i], self.args["Ar_x_start"][i],
                       self.args["Ar_x_end"][i],
                       self.args["Ar_y_start"][i], self.args["Ar_y_end"][i], self.args["Rh"][i], self.args["Pt"][i], self.args["Ta"][i], self.args["Na"][i]))
        return cameraList

    def load_configuration_from_json(self, jsonName):
        #self.args = json.loads(jsonName)
        with open(jsonName, "r") as read_file:
            self.args = json.load(read_file)
        self.args["HOST"] = socket.gethostbyname(socket.gethostname())
        self.args["ADDR"] = (self.args["SERVER"], self.args["PORT"])
        return self.read_camera_data_from_json()

    def load_configuration(self, configName, jsonName):
        f = open(configName, "r")
        #self.args = json.load(jsonName)
        line_list = [line for line in f]
        with open(jsonName, "r") as read_file:
            self.args = json.load(read_file)
        self.args["SERVER"] = str(line_list[31]).strip()
        self.args["HOST"] = socket.gethostbyname(socket.gethostname())
        self.args["URL"] = str(line_list[33]).strip()
        self.args["VIDEO_STREAMS_PATH"] = str(line_list[35]).strip()
        self.args["VIDEO_STREAMS_SMOKE_PATH"] = str(line_list[37]).strip()
        self.args["ADDR"] = (self.args["SERVER"], self.args["PORT"])
        self.args["ERRORS"] = int(str(line_list[39]).strip())
        self.args["WARNINGS"] = int(str(line_list[41]).strip())
        self.args["INFO"] = int(str(line_list[43]).strip())
        self.args["DEBUG"] = int(str(line_list[45]).strip())
        f.close()
        return self.read_camera_data_from_file(configName)

    def str_to_camera_att(self, att, listNumber, type):
        tmpStr = str(att[listNumber])
        tmpList = tmpStr.split()
        if type == 0:
            tmpList = [int(num) for num in tmpList]
        elif type == 1:
            tmpList = [float(num) for num in tmpList]
        elif type == 2:
            tmpList = [string[0] for string in tmpList]
            tmpList = [string.split(",") for string in tmpList]
        return tmpList

    def open_socket(self):
        massageReader = Massage(self.args)
        massageReader.connect()
        return massageReader

    def runAsServer(self, camList):
        server = OpenSocket(self.args)
        server.server()
        eventList = []
        personEventList = Queue(maxsize=100)
        counter = 0
        while True:
            counter += 1
            str_list = server.currMassage.split("/")
            if len(str_list) == 1:
                continue
            elif counter % 25 == 0:
                currDetection = Detection(self.args)
                currDetection.encode(str_list)
                currDetection.cameraId = camList[int(currDetection.originalCameraId)].id
                currChecker = Checker(self.args, currDetection.eventType, currDetection.cameraId)
                boundariesCheck = currChecker.checkBoundaries(camList[currDetection.cameraId], currDetection)
                currChecker.isEventInCamera(currDetection.eventType, camList[currDetection.cameraId].eventTypes)
                lastEventCheck = currChecker
                lastEventCheck.isTimePassedFromLastEvent(camList[currDetection.originalCameraId])
                if currDetection.eventType == "PERSONS":
                    personEventList.put(currDetection)
                #if not currDetection.eventType or not boundariesCheck or not lastEventCheck:
                if not lastEventCheck:
                    print(f"fail: {currDetection.eventType, boundariesCheck, lastEventCheck}")
                currDetection.x, currDetection.y = boundariesCheck
                camList[currDetection.cameraId].lastDetectionInCamera = time.time()
                if currDetection.eventType != "PERSONS":
                    currEvent = Event(self.args, currDetection.cameraId, currDetection.eventType)
                else:
                    currEvent = Event(self.args, currDetection.cameraId, "NO_CROSS_ZONE")
                    eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList, personEventList)
                    currEvent = Event(self.args, currDetection.cameraId, "PPE_HELMET")
                eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList, personEventList)

    def runAsClient(self, camList, sock):
        eventList = []
        while True:
            list_of_strings = sock.handle_massage()
            for string in list_of_strings:
                str_list = string.split(" ")
                if str_list[0] == 'Non':
                    tempEvent = Event(self.args, -1, -1)
                    eventList = tempEvent.handle_no_detction(camList, eventList)
                else:
                    currDetection = Detection(self.args)
                    currDetection.encode(str_list)
                    currDetection.cameraId = camList[int(currDetection.originalCameraId)].id
                    currChecker = Checker(self.args, currDetection.eventType, currDetection.cameraId)
                    currChecker.checkBoundaries(camList[currDetection.cameraId], currDetection)
                    currChecker.isEventInCamera(currDetection.eventType, camList[currDetection.cameraId].eventTypes)
                    lastEventCheck = currChecker
                    lastEventCheck.isTimePassedFromLastEvent(camList[currDetection.originalCameraId])
                    checkList = [currChecker.boundaries, currChecker.timeFromLastClosed, currChecker.eventInCamera]
                    if not all(checkList):
                        print(f"fail: boundaries: {currChecker.boundaries} timeFromLastClosed: {currChecker.timeFromLastClosed} eventInCamera: {currChecker.eventInCamera}")
                        break
                    currDetection.x, currDetection.y = currChecker.x, currChecker.y
                    camList[currDetection.cameraId].lastDetectionInCamera = time.time()
                    if currDetection.eventType != "PERSONS":
                        currEvent = Event(self.args, currDetection.cameraId, currDetection.eventType)
                        eventList = eventList.handle_detection(currEvent, currDetection, camList, eventList)
                    else:
                        currEvent = Event(self.args, currDetection.cameraId, "NO_CROSS_ZONE")
                        eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)
                        currEvent = Event(self.args, currDetection.cameraId, "PPE_HELMET")
                        eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)