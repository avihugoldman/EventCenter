from event import Event
import time

class Checker(Event):
    def __init__(self, args, type, cameraId):
        super().__init__(args, type, cameraId)
        self.eventType = type
        self.cameraId = cameraId
        self.eventInCamera = False
        self.eventInCamera = False
        self.eventInCamera = False

    def isTimePassedFromLastEvent(self, camera):
        if camera.timeoutCount is not None:
            if time.time() - camera.timeoutCount < camera.timeToOpenAfterClose:
                return None
        return self

    def isEventInCamera(self, event, eventsInCamera):
        if event == "PERSONS":
            if "NO_HELMET" in eventsInCamera and "NO_CROSS_ZONE" in eventsInCamera:
                return
            if "NO_HELMET" not in eventsInCamera and "NO_CROSS_ZONE" in eventsInCamera:
                self.eventType = "NO_CROSS_ZONE"
            elif "NO_HELMET" in eventsInCamera:
                self.eventType = "NO_HELMET"
            else:
                return False
        else:
            if event in eventsInCamera:
                self.eventType = event
            return False

    def checkBoundaries(self, camera, detection):
        detection_x_start = detection.x[0][0]
        detection_x_end = detection.x[0][1]
        detection_x_size = detection_x_end - detection_x_start
        detection_y_start = detection.y[0][0]
        detection_y_end = detection.y[0][1]
        detection_y_size = detection_y_end - detection_y_start
        detectionTotalArea = detection_x_size * detection_y_size
        if detection_x_start < float(camera.x_start):
            print("off limits!")
            detection.x[0][0] = camera.x_start
        if detection_x_end > float(camera.x_end):
            # print("off limits!")
            detection.x[0][1] = camera.x_end
        if abs(detection.x[0][1] - detection.x[0][0]) <= 0.01:
            return False
        if detection_y_size < camera.minSize or detection_y_size > camera.maxSize and detection.eventType == "PERSONS":
            return False
        if detection_y_start < float(camera.y_start):
            # print("off limits!")
            detection.y[0][0] = camera.y_start
        if detection_y_end > float(camera.y_end):
            # print("off limits!")
            detection.y[0][1] = camera.y_end
        if abs(detection.y[0][1] - detection.y[0][0]) <= 0.01:
            # print("problem")
            return False
        detection_x_start = detection.x[0][0]
        detection_x_end = detection.x[0][1]
        detection_x_size = detection_x_end - detection_x_start
        detection_y_start = detection.y[0][0]
        detection_y_end = detection.y[0][1]
        detection_y_size = detection_y_end - detection_y_start
        newDetectionTotalArea = detection_x_size * detection_y_size
        if newDetectionTotalArea / detectionTotalArea < 0.8:
            return False
        return detection.x, detection.y

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