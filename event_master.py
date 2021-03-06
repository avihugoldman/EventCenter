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
        with open(jsonName, "r") as read_file:
            self.args = json.load(read_file)
        self.args["HOST"] = socket.gethostbyname(socket.gethostname())
        self.args["ADDR"] = (self.args["SERVER"], self.args["PORT"])
        return self.read_camera_data_from_json()

    def load_configuration(self, configName, jsonName):
        f = open(configName, "r")
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
        if type == 0:
            tmpList = tmpStr.split()
            tmpList = [int(num) for num in tmpList]
        elif type == 1:
            tmpList = tmpStr.split()
            tmpList = [float(num) for num in tmpList]
        elif type == 2:
            tmpList = tmpStr.split(",")
            tmpList = [string.strip().split(" ") for string in tmpList if string]
        return tmpList

    def open_socket(self):
        massageReader = Massage(self.args)
        massageReader.connect()
        return massageReader

    def run_as_server(self, camList):
        server = OpenSocket(self.args)
        server.server()
        eventList = []
        anomalyFrameCounter = 0
        massageCounter = 0
        lastFrame = -1
        while True:
            str_list = server.currMassage
            lastMassageTime = time.time()
            massageCounter += 1
            if not server.currMassage or time.time() - lastMassageTime > 0.5:
                tempEvent = Event(self.args, -1, -1)
                eventList = tempEvent.handle_no_detction(camList, eventList)
            else:
                if massageCounter % 10:
                    tempEvent = Event(self.args, -1, -1)
                    eventList = tempEvent.handle_no_detction(camList, eventList)
                currDetection = Detection(self.args)
                currDetection.encode(str_list)
                # Handle each frame once:
                if lastFrame == (currDetection.serialId, currDetection.cameraId):
                    continue
                lastFrame = (currDetection.serialId, currDetection.cameraId)
                try:
                    currDetection.cameraId = camList[int(currDetection.originalCameraId)].id
                except IndexError:
                    continue
                # Handle one of 100 anomaly detections:
                # if currDetection.netName == "Anomaly":
                #     anomalyFrameCounter += 1
                #     if anomalyFrameCounter % self.args["anomaly_reduce"]:
                #         continue
                currChecker = Checker(self.args, currDetection.eventType, currDetection.cameraId)
                currChecker.is_time_passed_from_last_event(camList[currDetection.originalCameraId])
                currChecker.check_boundaries(camList[currDetection.originalCameraId], currDetection)
                currChecker.is_event_in_camera(currDetection.eventType, camList[currDetection.originalCameraId].eventTypes)
                checkList = [currChecker.boundaries, currChecker.timeFromLastClosed, currChecker.eventInCamera]
                if self.args["DEBUG"] and currDetection.eventType != "ANOMALY":
                    print(currDetection)
                self.add_detection_to_list(currDetection, camList)
                if not all(checkList):
                    #if self.args["DEBUG"]:
                       # print(f"fail: boundaries: {currChecker.boundaries} timeFromLastClosed: {currChecker.timeFromLastClosed} eventInCamera: {currChecker.eventInCamera}")
                    continue
                currDetection.x, currDetection.y = currChecker.x, currChecker.y
                camList[currDetection.originalCameraId].lastDetectionInCamera = time.time()
                if currDetection.eventType != "PERSONS":
                    currEvent = Event(self.args, currDetection.cameraId, currDetection.eventType)
                    eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)
                else:
                    currEvent = Event(self.args, currDetection.cameraId, "NO_CROSS_ZONE")
                    eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)
                    if "PPE_HELMET" in camList[currDetection.originalCameraId].eventTypes and currChecker.is_time_passed_from_last_helmet_event(
                        camList[currDetection.originalCameraId]):
                        currEvent = Event(self.args, currDetection.cameraId, "PPE_HELMET")
                        eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)

    def add_detection_to_list(self, currDetection, camList):
        if currDetection.eventType == "PERSONS":
            if camList[currDetection.originalCameraId].personEventList.full():
                camList[currDetection.originalCameraId].personEventList.get()
            camList[currDetection.originalCameraId].personEventList.put(currDetection)
        if currDetection.eventType == "ANOMALY":
            if camList[currDetection.originalCameraId].anomalyDetectionList.full():
                camList[currDetection.originalCameraId].anomalyDetectionList.get()
            camList[currDetection.originalCameraId].anomalyDetectionList.put(currDetection)

    def run_as_client(self, camList, sock, type):
        eventList = []
        if type == "s":
            self.args["SMOKE"] = 1
            self.args["PERSONS"] = 8
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
                    #print(currDetection)
                    try:
                        currDetection.cameraId = camList[int(currDetection.originalCameraId)].id
                    except IndexError:
                        continue
                    if currDetection.eventType == "PERSONS":
                        if camList[currDetection.originalCameraId].personEventsList.full():
                            camList[currDetection.originalCameraId].personEventsList.get()
                        camList[currDetection.originalCameraId].personEventsList.put(currDetection)
                    currChecker = Checker(self.args, currDetection.eventType, currDetection.cameraId)
                    currChecker.is_time_passed_from_last_event(camList[currDetection.originalCameraId])
                    currChecker.check_boundaries(camList[currDetection.originalCameraId], currDetection)
                    currChecker.is_event_in_camera(currDetection.eventType,
                                                   camList[currDetection.originalCameraId].eventTypes)
                    checkList = [currChecker.boundaries, currChecker.timeFromLastClosed, currChecker.eventInCamera]
                    if not all(checkList):
                        #print(f"fail: boundaries: {currChecker.boundaries} timeFromLastClosed: {currChecker.timeFromLastClosed} eventInCamera: {currChecker.eventInCamera}")
                        continue
                    currDetection.x, currDetection.y = currChecker.x, currChecker.y
                    camList[currDetection.originalCameraId].lastDetectionInCamera = time.time()
                    if currDetection.eventType != "PERSONS":
                        currEvent = Event(self.args, currDetection.cameraId, currDetection.eventType)
                        eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)
                    else:
                        currEvent = Event(self.args, currDetection.cameraId, "NO_CROSS_ZONE")
                        eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)
                        if "PPE_HELMET" in camList[
                            currDetection.originalCameraId].eventTypes and currChecker.is_time_passed_from_last_helmet_event(
                                camList[currDetection.originalCameraId]):
                            currEvent = Event(self.args, currDetection.cameraId, "PPE_HELMET")
                            eventList = currEvent.handle_detection(currEvent, currDetection, camList, eventList)