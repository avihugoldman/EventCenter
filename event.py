import time
from detection import Detection
#from event import event
import logging
import requests
import threading


class Event(Detection):
    def __init__(self, args, cameraId, type, open = False):
        super().__init__(args)
        self.cameraId = cameraId
        self.eventType = type
        self.id = int
        self.published = False
        self.lastUpdate = float
        self.startTime = float
        self.subClassList = []
        self.realDetectionList = []
        self.open = bool(open)
        self.publishedTime = float
        self.closedTime = None
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)

    def __repr__(self):
        return (f"Event [{self.id}] type [{self.eventType}] camera [{self.cameraId}] open? [{self.open}]")

    def __eq__(self, other):
        return self.eventType == other.eventType and self.cameraId == other.cameraId

    def handle_no_detction(self, camList, listOfTotalEvents):
        counter = -1
        tempPublishedEventList = [tempEvent for tempEvent in listOfTotalEvents if tempEvent.published and tempEvent.eventType != "WATCHMAN"]
        for obj in tempPublishedEventList:
            if time.time() - obj.lastUpdate > camList[obj.originalCameraId].timeToPublish or time.time() - obj.publishedTime > \
                    camList[obj.originalCameraId].timeoutAfterPublish:
                obj.endShipEvent()
                listOfTotalEvents.remove(obj)
                camList[obj.originalCameraId].timeoutCount = time.time()
                break
            if obj.eventType == "WATCHMAN" and camList[obj.originalCameraId].personEventList.notempty():#
                if camList[obj.originalCameraId].personEventList.get().updateTime - obj.startTime > 0:
                    obj.endShipEvent()
                    listOfTotalEvents.remove(obj)
                    camList[obj.originalCameraId].timeoutCount = time.time()
        tempNotPublishedEventList = [tempEvent for tempEvent in listOfTotalEvents if not tempEvent.published and tempEvent.eventType != "WATCHMAN"]
        for obj in tempNotPublishedEventList:
            if time.time() - obj.startTime > camList[obj.originalCameraId].timeToPublish + 1:
                obj.endShipEvent()
                listOfTotalEvents.remove(obj)
                camList[obj.originalCameraId].timeoutCount = None
        for camera in camList:
            counter += 1
            if "WATCHMAN" in camera.eventTypes and time.time() - camera.lastDetectionInCamera > camera.timeForWatchman:
                event = Event(self.args, camera.id, "WATCHMAN")
                if event in listOfTotalEvents:
                    curr = listOfTotalEvents[listOfTotalEvents.index(event)]
                    curr.x, curr.y, curr.serialId = [[0, 1]], [[0, 1]], 1
                    if time.time() - curr.startTime > camera.timeoutAfterPublish:
                        curr.endShipEvent()
                        camList[curr.originalCameraId].timeoutCount = time.time()
                        camera.WatchmanStarted = False
                        listOfTotalEvents.remove(curr)
                        continue
                    curr.fire_and_forget()
                    curr.lastUpdate = time.time()
                else:
                   # if time.time() - float(camera.timeoutCount) < camera.timeToOpenAfterClose:
                       # continue
                   if camera.timeoutCount is None:
                       event.originalCameraId = counter
                       event.startShipEvent()
                       camera.timeoutCount = time.time()
                       camera.WatchmanStarted = True
                       if event.id:
                           event.publishShipEvent(camList)
                           event.cameraId = camera.id
                           listOfTotalEvents.append(event)
                   else:
                       if not time.time() - camera.timeoutCount < camera.timeToOpenAfterClose:
                            event.originalCameraId = counter
                            event.startShipEvent()
                            camera.timeoutCount = time.time()
                            camera.WatchmanStarted = True
                            if event.id:
                                event.publishShipEvent(camList)
                                event.cameraId = camera.id
                                listOfTotalEvents.append(event)
        return listOfTotalEvents

    def handle_detection(self, event, detection, camList, eventList):
        if event in eventList:
            flag = False
            curr = eventList[eventList.index(event)]
            curr.addObjectToList(detection.subClass, camList[curr.originalCameraId].queueSize)
            #curr.realDetectionLIst = self.addObjectToList([], camList[curr.id].queueSize)
            curr.lastUpdate = time.time()
            curr.originalCameraId = detection.originalCameraId
            time_diff = time.time() - curr.startTime
            curr.x, curr.y, curr.serialId = detection.x, detection.y, detection.serialId
            if detection.eventType != "ANOMALY":
                if time_diff > camList[curr.originalCameraId].timeToPublish:
                    flag = True
            else:
                if time_diff > camList[curr.originalCameraId].timeToPublish: #ready for new parmeter for anomaly
                    flag = True
            if flag:
                if len(curr.subClassList) >= camList[curr.originalCameraId].queueSize:
                    if detection.eventType != "PPE_HELMET":
                        if curr.isItRealDetection(curr.subClassList):
                            if curr.published:
                                curr.fire_and_forget()
                                if self.args["DEBUG"]:
                                    print(f"event {curr.id} has been sent in time {time.time()} in camera {self.cameraId}")
                            else:
                                curr.publishShipEvent(camList)
                                if self.args["DEBUG"]:
                                    print(f"NO_CROSS_ZONE event published in camera {self.cameraId} in time {time.time()}")
                    else:
                        if curr.isItRealHelmetDetection(curr.subClassList, camList[curr.originalCameraId]):
                            if curr.published:
                                curr.fire_and_forget()
                                if self.args["DEBUG"]:
                                    print(f"event {curr.id} has been sent in time {time.time()} in camera {self.cameraId}")
                            else:
                                curr.publishShipEvent(camList)
                                if self.args["DEBUG"]:
                                    print(f"NO_CROSS_ZONE event published in camera {self.cameraId} in time {time.time()}")
        else:
            if event.eventType == "ANOMALY":
                if camList[detection.originalCameraId].personEventList.qsize() == 0:
                    event.originalCameraId = detection.originalCameraId
                    event.startShipEvent()
                    #camList[detection.originalCameraId].timeoutCount = None
                    if event.id:
                        event.subClassList.append(detection.subClass)
                        event.originalCameraId = detection.originalCameraId
                        eventList.append(event)
                else:
                    if time.time() - camList[detection.originalCameraId].personEventList.pop().updateTime < camList[detection.originalCameraId].TimeWithNoPerson:
                        return eventList
                    else:
                        event.originalCameraId = detection.originalCameraId
                        event.startShipEvent()
                        #camList[detection.originalCameraId].timeoutCount = None
                        if event.id:
                            event.subClassList.append(detection.subClass)
                            event.originalCameraId = detection.originalCameraId
                            eventList.append(event)
            if event.eventType == "PPE_HELMET":
                if detection.subClass == 2:
                    event.originalCameraId = detection.originalCameraId
                    event.startShipEvent()
                    #camList[detection.originalCameraId].timeoutCount = None
                    if event.id:
                        event.subClassList.append(detection.subClass)
                        eventList.append(event)
            else:
                event.originalCameraId = detection.originalCameraId
                event.startShipEvent()
                #camList[detection.originalCameraId].timeoutCount = None
                if event.id:
                    event.subClassList.append(detection.subClass)
                    eventList.append(event)
        return eventList

    def addObjectToList(self, tempDetection, size):
        if len(self.subClassList) > size:
            self.subClassList.pop()
        self.subClassList.append(tempDetection)

    def startShipEvent(self):
        eventId = None
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        string_to_send = """
           mutation{
               startShipEvent(event:{ 
                 cameraUid: "%d"
                 eventType: %s
               }){ 
               id
                 }
               }
           """ % (self.cameraId, self.eventType)
        request = requests.post(self.args["URL"], json={'query': string_to_send})
        if request.status_code != 200 and self.args["ERRORS"]:
            logging.error(f"Query failed to run by returning code of {request.status_code} in startEvent")
        else:
            try:
                if self.args["DEBUG"]:
                    logging.debug(request.json())
                eventId = request.json()['data']['startShipEvent']['id']
                if self.args["INFO"]:
                    print(f"start event {eventId} type {self.eventType} in camera {self.cameraId} in time {current_time}")
            except:
                eventId = None
                if self.args["WARNINGS"]:
                    logging.warning("Failed to get id from server")
        self.id = eventId
        self.startTime, self.lastUpdate = time.time(), time.time()
        self.open = True

    def publishShipEvent(self, camList):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        string_to_send = """
           mutation{
               publishShipEvent(eventId: %d, publish: true){ 
               id
             }
           }""" % (self.id)
        request = requests.post(self.args["URL"], json={'query': string_to_send})
        if request.status_code != 200 and self.args["ERRORS"]:
            logging.error(f"Query failed to run by returning code of {request.status_code} in publishEvent")
        else:
            if self.args["DEBUG"]:
                logging.debug(request.json())
            if self.args["INFO"]:
                print(
                    f"Published event {self.id} type {self.eventType} in camera {self.cameraId} in time {current_time}")
        self.lastUpdate = time.time()
        self.published = True
        self.publishedTime = time.time()
        if len(camList[self.originalCameraId].lastEventsInCamera) > 50:
            camList[self.originalCameraId].lastEventsInCamera.pop()
        camList[self.originalCameraId].lastEventsInCamera.append(self)

    def sendDetection(self):
        if self.x and self.y:
            num_objects = len(self.x)
            if num_objects <= 0:
                return
            all_rects_str = ""
            if True:
                empty_rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
                    0, 0, 0, 0)
                all_rects_str += empty_rect_str
                rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
                self.x[0],
                self.y[0], self.x[1],
                self.y[1])
                all_rects_str += rect_str
            string_to_send = """
               mutation{
                   addShipDetection(event:{
                     eventId: %d
                     serialId: %d
                     boundingAreas: [%s]
                   }){
                     id,
                     serialId,
                     boundingAreas {
                       x1, y1, x2, y2
                     }
                   }
                   }""" % (self.id, self.serialId, all_rects_str)
        else:
            tempSerialId = 1
            string_to_send = """
               mutation
               {
                   addShipDetection(event:{
                     eventId: %d
                     serialId: %d
                     boundingAreas: {x1:0.0,y1:0.0,x2:0.0,y2:0.0}
                   }){
                     id,
                     boundingAreas {
                       x1, y1, x2, y2
                     }
                   }
               }""" % (self.id, tempSerialId)
        if self.args["DEBUG"]:
            logging.debug(string_to_send)
        request = requests.post(self.args["URL"], json={'query': string_to_send})
        if request.status_code != 200 and self.args["ERRORS"]:
            if self.args["WARNINGS"]:
                logging.warning(f"Query failed to run by returning code of {request.status_code} in sendDetection")
        self.lastUpdate = time.time()

    def fire_and_forget(self):
        threading.Thread(target=self.sendDetection, args=()).start()

    def endShipEvent(self):
        time.sleep(0.05)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        tempDetection = Detection(self.args)
        tempDetection.serialId, tempDetection.x, tempDetection.y = 0, [], []
        self.fire_and_forget()
        string_to_send = """
           mutation{
               endShipEvent(eventId: 
                 %d
               ){ 
               id,
                 }
               }
           """ % (self.id)
        request = requests.post(self.args["URL"], json={'query': string_to_send})
        if self.args["INFO"]:
            print(
                f"close event {self.id} type {self.eventType} in camera {self.cameraId} in time {current_time}")
        if request.status_code != 200 and self.args["ERRORS"]:
            if self.args["WARNINGS"]:
                logging.warning(f"Query failed to run by returning code of {request.status_code} in endShipEvent")
        self.open = False
        self.published = False
        self.closedTime = time.time()

    def isItRealDetection(self, detection_queue):
        event_happening_counter = 0
        for detection in detection_queue:
            if detection != None:
                event_happening_counter += 1
            else:
                continue
        if (event_happening_counter) > len(detection_queue) / 2:
            return True
        return False

    def isItRealHelmetDetection(self, detection_queue, camera):
        event_happening_counter = 0
        # Runs over 60 frames and counts in how many of them there is an event
        for detection in detection_queue:
            if detection == 2:
                event_happening_counter += 1
            else:
                continue
        # Check if at least half of the frames has an event
        try:
            score = float(len(detection_queue)) / 100
        except IndexError:
            score = float(20 / 100)
        try:
            score *= int(camera.detectionRatio)
        except IndexError:
            score *= int(camera.detectionRatio)
        if (event_happening_counter) > score:
            return True
        return False

class Events:
    def __init__(self):
        self.eventList = []
        self.openEventsOnly = bool

    def __repr__(self):
        return (f"[{self.eventList}]")

    def addObjectToList(self, tempDetection, size):
        if len(self.eventList) > size:
            self.eventList.pop()
        self.eventList.append(tempDetection)
