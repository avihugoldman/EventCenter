
class Detection:
    def __init__(self, args):
        self.args = args
        self.originalCameraId = int
        self.cameraId = int
        self.objId = int
        self.eventType = str
        self.subClass = int
        self.x = []
        self.y = []

    def __repr__(self):
        return (f"camera [{self.cameraId}] objId [{self.objId}] eventType [{self.eventType}] subClass [{self.subClass}] x {self.x} y {self.y}")

    def encode(self, string):
        self.originalCameraId = int(string[0])
        self.serialId = int(string[1])
        self.eventType = self.convertEventIntToSTR(int(string[2]))
        self.subClass = int(string[3])
        self.objId = int(string[4])
        try:
            self.netName = str(string[7])
        except ValueError:
            self.netName = "Smoke"
        if self.netName == "SMOKE":
            self.x = self.covertStrToFloatListYoav(string[5])
            self.x = self.covertStrToFloatListYoav(string[5])
        else:
            self.x = self.covertStrToFloatList(string[5])
            self.y = self.covertStrToFloatList(string[6])

    def convertEventIntToSTR(self, event_type):
        if event_type == self.args["PERSONS"]:
            return "PERSONS"
        elif event_type == self.args["NO_CROSS_ZONE"]:
            return "NO_CROSS_ZONE"
        elif event_type == self.args["PPE_HELMET"]:
            return "PPE_HELMET"
        elif event_type == self.args["SMOKE_AND_LEAKAGE"]:
            return "SMOKE"
        elif event_type == self.args["WATCH_MAN_ALERT"]:
            return "WATCHMAN"
        elif event_type == self.args["DEAD_MAN_ALERT"]:
            return "DEAD_MAN_ALERT"
        elif event_type == self.args["ANOMALY"]:
            return "ANOMALY"
        else:
            return None

    def covertStrToFloatList(self, str_object):
        temp_list = []
        list_object = []
        str_object = str_object.strip("[ ]")
        str_object = str_object.split(", ")
        str_object = [i.split(",") for i in str_object]
        for lst in str_object:
            for num in lst:
                temp_list.append(float(num))
            list_object.append(temp_list)
        return list_object

    def covertStrToFloatListYoav(self, str_object):
        temp_list = []
        list_object = []
        str_object = str_object.strip("[,]")
        str_object = str_object.split()
        str_object = [i.split(",") for i in str_object]
        for lst in str_object:
            for num in lst:
                temp_list.append(float(num))
            list_object.append(temp_list)
        return list_object




