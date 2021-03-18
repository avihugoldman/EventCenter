from event import Event
import time

class Checker(Event):
    def __init__(self, args, type, cameraId):
        super().__init__(args, type, cameraId)
        self.eventType = type
        self.cameraId = cameraId
        self.eventInCamera = True
        self.timeFromLastClosed = True
        self.boundaries = True

    def isTimePassedFromLastEvent(self, camera):
        if camera.lastEventsInCamera:
            if self.eventType != "PERSONS":
                tempList = [event for event in camera.lastEventsInCamera if event.eventType == self.eventType and not event.open]
                for event in tempList:
                    if time.time() - event.closedTime < camera.timeToOpenAfterClose:
                        self.timeFromLastClosed = False
            else:
                tempList = [event for event in camera.lastEventsInCamera if
                            event.eventType == "NO_CROSS_ZONE" and not event.open]
                for event in tempList:
                    if time.time() - event.closedTime < camera.timeToOpenAfterClose:
                        self.timeFromLastClosed = False

    def isTimePassedFromLastHelmetEvent(self, camera):
        if camera.lastEventsInCamera:
            tempList = [event for event in camera.lastEventsInCamera if event.eventType == "PPE_HELMET" and not event.open]
            for event in tempList:
                if time.time() - event.closedTime < camera.timeToOpenAfterClose:
                    self.timeFromLastClosed = False

    def isEventInCamera(self, event, eventsInCamera):
        if event == "PERSONS":
            if "PPE_HELMET" in eventsInCamera and "NO_CROSS_ZONE" in eventsInCamera:
                return
            if "PPE_HELMET" not in eventsInCamera and "NO_CROSS_ZONE" in eventsInCamera:
                self.eventType = "NO_CROSS_ZONE"
            elif "PPE_HELMET" in eventsInCamera:
                self.eventType = "PPE_HELMET"
            else:
                self.eventInCamera = False
        else:
            if event in eventsInCamera:
                self.eventType = event
            self.eventInCamera = False

    def checkBoundaries(self, camera, detection):
        detection_x_start = detection.x[0]
        detection_x_end = detection.x[1]
        detection_x_size = detection_x_end - detection_x_start
        detection_y_start = detection.y[0]
        detection_y_end = detection.y[1]
        detection_y_size = detection_y_end - detection_y_start
        detectionTotalArea = detection_x_size * detection_y_size
        if detection_x_start < float(camera.x_start):
            # print("off limits!")
            detection.x[0] = camera.x_start
        if detection_x_end > float(camera.x_end):
            # print("off limits!")
            detection.x[1] = camera.x_end
        if abs(detection.x[1] - detection.x[0]) <= 0.01:
            self.boundaries = False
        if (detection_y_size < camera.minSize or detection_y_size > camera.maxSize) and detection.eventType == "PERSONS":
            self.boundaries = False
        if detection_y_start < float(camera.y_start):
            # print("off limits!")
            detection.y[0] = camera.y_start
        if detection_y_end > float(camera.y_end):
            # print("off limits!")
            detection.y[1] = camera.y_end
        if abs(detection.y[1] - detection.y[0]) <= 0.01:
            # print("problem")
            self.boundaries = False
        detection_x_start = detection.x[0]
        detection_x_end = detection.x[1]
        detection_x_size = detection_x_end - detection_x_start
        detection_y_start = detection.y[0]
        detection_y_end = detection.y[1]
        detection_y_size = detection_y_end - detection_y_start
        newDetectionTotalArea = detection_x_size * detection_y_size
        if newDetectionTotalArea / detectionTotalArea < 0.8:
            self.boundaries = False
        self.x, self.y = detection.x, detection.y

    # def isItRealDetection(self, detection_queue):
    #     event_happening_counter = 0
    #     for detection in detection_queue:
    #         if detection:
    #             event_happening_counter += 1
    #         else:
    #             continue
    #     if (event_happening_counter) > len(detection_queue) / 2:
    #         return True
    #     return False
    #
    # def isItRealHelmetDetection(self, detection_queue, camera):
    #     event_happening_counter = 0
    #     # Runs over 60 frames and counts in how many of them there is an event
    #     for detection in detection_queue:
    #         if detection == 2:
    #             event_happening_counter += 1
    #         else:
    #             continue
    #     # Check if at least half of the frames has an event
    #     try:
    #         score = float(len(detection_queue)) / 100
    #     except IndexError:
    #         score = float(20 / 100)
    #     try:
    #         score *= int(camera.detectionRatio)
    #     except IndexError:
    #         score *= int(camera.detectionRatio)
    #     if (event_happening_counter) > score:
    #         return True
    #     return False