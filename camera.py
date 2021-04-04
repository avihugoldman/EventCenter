import time
from queue import Queue


class Camera:
    def __init__(self, args, id, intEventTypes, timeToPublish, queueSize, timeoutAfterPublish, timeToOpenAfterClose, timeBetweenEvents, timeForWatchman,
                 maxSize, minSize, x_start, x_end, y_start, y_end, detectionRatio, TimeWithNoPerson, timeToPublishAnomly, queueSizeAnomaly):
        self.args = args
        self.id = id
        self.intEventTypes = intEventTypes
        self.eventTypes = []
        self.timeToPublish = timeToPublish
        self.queueSize = queueSize
        self.timeoutAfterPublish = timeoutAfterPublish
        self.timeToOpenAfterClose = timeToOpenAfterClose
        self.timeBetweenEvents = timeBetweenEvents
        self.timeForWatchman = timeForWatchman
        self.maxSize = maxSize
        self.minSize = minSize
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.detectionRatio = detectionRatio
        self.timeOfLastClose = int
        self.typeOfLastClose = str
        self.timeoutCount = None
        self.lastDetectionInCamera = time.time()
        self.WatchmanStarted = False
        self.TimeWithNoPerson = TimeWithNoPerson
        self.timeToPublishAnomly = timeToPublishAnomly
        self.queueSizeAnomaly = queueSizeAnomaly
        self.personEventList = Queue(maxsize=2)
        self.anomalyDetectionList = Queue(maxsize=2)
        self.lastEventsInCamera = []

    def __repr__(self):
        return (f"camera {self.id} event_type are: {self.eventTypes}")

    def convert_event_int_to_str(self):
        strEventTypes = []
        for eventType in self.intEventTypes:
            if int(eventType) == self.args["PERSONS"]:
                strEventTypes.append("PERSONS")
            elif int(eventType) == self.args["NO_CROSS_ZONE"]:
                strEventTypes.append("NO_CROSS_ZONE")
            elif int(eventType) == self.args["PPE_HELMET"]:
                strEventTypes.append("PPE_HELMET")
            elif int(eventType) == self.args["SMOKE"]:
                strEventTypes.append("SMOKE")
            elif int(eventType) == self.args["WATCH_MAN_ALERT"]:
                strEventTypes.append("WATCHMAN")
            elif int(eventType) == self.args["DEAD_MAN_ALERT"]:
                strEventTypes.append("DEAD_MAN_ALERT")
            elif int(eventType) == self.args["ANOMALY"]:
                strEventTypes.append("ANOMALY")
        self.eventTypes = strEventTypes

# class timeout:
#     def __init__(self, eventType):
#         self.eventType = eventType
#         self.timeout = time.time()