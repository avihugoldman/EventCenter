import time


class Detection:
    def __init__(self, args):
        self.args = args
        self.originalCameraId = int
        self.cameraId = int
        self.objId = int
        self.eventType = str
        self.subClass = int
        self.topLeft = []
        self.bottomRight = []
        self.netName = str
        self.updateTime = time.time()

    def __repr__(self):
        return (f"camera [{self.cameraId}] frame [{self.serialId}] eventType [{self.eventType}] subClass [{self.subClass}] objId [{self.objId}] top left {self.topLeft} bottom right {self.bottomRight} net name [{self.netName}]")

    # def encode(self, string):
    #     self.originalCameraId = int(string[0])
    #     self.serialId = int(string[1])
    #     self.eventType = self.convert_event_int_to_str(int(string[2]))
    #     self.subClass = int(string[3])
    #     self.objId = int(string[4])
    #     self.lastUpdateTime = time.time()
    #     try:
    #         self.netName = str(string[7])
    #     except IndexError:
    #         self.netName = "SMOKE"
    #     if self.netName == "SMOKE":
    #         self.x = self.covert_str_to_float_list_yoav(string[5])
    #         self.y = self.covert_str_to_float_list_yoav(string[5])
    #     else:
    #         self.x = [float(f) for f in string[5]]
    #         self.y = [float(f) for f in string[6]]

    def encode(self, string):
        self.originalCameraId = int(string["camera_number"])
        self.serialId = int(string["frame_number"])
        self.eventType = self.convert_event_int_to_str(string["event_type"])
        self.subClass = int(string["obj_sub_class"])
        self.objId = int(string["obj_id"])
        self.lastUpdateTime = time.time()
        self.netName = str(string["algo_name"])
        self.topLeft = [float(f) for f in string["top_left_rect"]]
        self.bottomRight = [float(f) for f in string["bottom_right_rect"]]
        self.x_start = self.topLeft[0]
        self.x_end = self.bottomRight[0]
        self.y_start = self.topLeft[1]
        self.y_end = self.bottomRight[1]

    def convert_event_int_to_str(self, event_type):
        if event_type == self.args["PERSONS"]:
            return "PERSONS"
        elif event_type == self.args["NO_CROSS_ZONE"]:
            return "NO_CROSS_ZONE"
        elif event_type == self.args["PPE_HELMET"]:
            return "PPE_HELMET"
        elif event_type == self.args["SMOKE"]:
            return "SMOKE"
        elif event_type == self.args["WATCH_MAN_ALERT"]:
            return "WATCHMAN"
        elif event_type == self.args["DEAD_MAN_ALERT"]:
            return "DEAD_MAN_ALERT"
        elif event_type == self.args["ANOMALY"]:
            return "ANOMALY"
        else:
            return None

    def covert_str_to_float_list_yoav(self, str_object):
        temp_list = []
        list_object = []
        str_object = str_object.strip("[,]")
        str_object = str_object.split()
        str_object = [i.split(",") for i in str_object]
        for lst in str_object:
            for num in lst:
                temp_list.append(float(num))
            list_object.append(temp_list)
        return list_object[0]




