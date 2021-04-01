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

    def is_time_passed_from_last_event(self, camera):
        if len(camera.lastEventsInCamera) > 0:
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

    def is_time_passed_from_last_helmet_event(self, camera):
        flag = True
        if len(camera.lastEventsInCamera) > 0:
            tempList = [event for event in camera.lastEventsInCamera if event.eventType == "PPE_HELMET" and not event.open]
            if len(tempList) > 0:
                for event in tempList:
                    if time.time() - event.closedTime < camera.timeToOpenAfterClose:
                        return False
        return True

    def is_event_in_camera(self, event, eventsInCamera):
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
            else:
                self.eventInCamera = False

    # def check_boundaries(self, camera, detection):
    #     detection_x_start = detection.x[0]
    #     detection_x_end = detection.x[1]
    #     detection_x_size = detection_x_end - detection_x_start
    #     detection_y_start = detection.y[0]
    #     detection_y_end = detection.y[1]
    #     detection_y_size = detection_y_end - detection_y_start
    #     detectionTotalArea = detection_x_size * detection_y_size
    #     if detection_x_start < float(camera.x_start):
    #         # print("off limits!")
    #         detection.x[0] = camera.x_start
    #     if detection_x_end > float(camera.x_end):
    #         # print("off limits!")
    #         detection.x[1] = camera.x_end
    #     if abs(detection.x[1] - detection.x[0]) <= 0.01:
    #         self.boundaries = False
    #     if (detection_y_size < camera.minSize or detection_y_size > camera.maxSize) and detection.eventType == "PERSONS":
    #         self.boundaries = False
    #     if detection_y_start < float(camera.y_start):
    #         # print("off limits!")
    #         detection.y[0] = camera.y_start
    #     if detection_y_end > float(camera.y_end):
    #         # print("off limits!")
    #         detection.y[1] = camera.y_end
    #     if abs(detection.y[1] - detection.y[0]) <= 0.01:
    #         # print("problem")
    #         self.boundaries = False
    #     detection_x_start = detection.x[0]
    #     detection_x_end = detection.x[1]
    #     detection_x_size = detection_x_end - detection_x_start
    #     detection_y_start = detection.y[0]
    #     detection_y_end = detection.y[1]
    #     detection_y_size = detection_y_end - detection_y_start
    #     newDetectionTotalArea = detection_x_size * detection_y_size
    #     if newDetectionTotalArea / detectionTotalArea < 0.8:
    #         self.boundaries = False
    #     self.x, self.y = detection.x, detection.y

    def check_boundaries(self, camera, detection):
        detection_x_size = detection.x_end - detection.x_start
        detection_y_size = detection.y_end - detection.y_start
        detectionTotalArea = detection_x_size * detection_y_size
        if detection.x_start < float(camera.x_start):
            # print("off limits!")
            detection.x_start = camera.x_start
        if detection.x_end > float(camera.x_end):
            # print("off limits!")
            detection.x_end = camera.x_end
        if abs(detection.x_end - detection.x_start) <= 0.01:
            self.boundaries = False
        if (detection_y_size < camera.minSize or detection_y_size > camera.maxSize) and detection.eventType == "PERSONS":
            self.boundaries = False
        if detection.y_start < float(camera.y_start):
            # print("off limits!")
            detection.y_start = camera.y_start
        if detection.y_end > float(camera.y_end):
            # print("off limits!")
            detection.y_end = camera.y_end
        if abs(detection.y_end - detection.y_start) <= 0.01:
            self.boundaries = False
        detection_x_size = detection.x_end - detection.x_start
        detection_y_size = detection.y_end - detection.y_start
        newDetectionTotalArea = detection_x_size * detection_y_size
        if newDetectionTotalArea / detectionTotalArea < self.args["Ar"]:
            self.boundaries = False
        self.x, self.y = [detection.x_start, detection.x_end], [detection.y_start, detection.y_end]

    def check_dead_man(self):
        pass
        # get pos vector in size of VECTOR_SIZE (numpy vector or list of floats) from yoav
        # make histogram on the last 30 frames.
        # checks if 90% of changes are in the same 10% of bins.
        # sends Dead man event