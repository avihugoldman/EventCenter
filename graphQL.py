# from detection import Detection
# #from event import Event
# import logging
# import requests
# import time
# import threading
#
#
# class GraphQL(Detection):
#     def __init__(self, args, type, cameraId):
#         super().__init__(args, type, cameraId)
#
#     def startShipEvent(self):
#         eventId = -1
#         string_to_send = """
#            mutation{
#                startShipEvent(event:{
#                  cameraUid: "%d"
#                  eventType: %s
#                }){
#                id
#                  }
#                }
#            """ % (self.cameraId, self.eventType)
#         request = requests.post(self.args["URL"], json={'query': string_to_send})
#         if request.status_code != 200:
#             logging.error(f"Query failed to run by returning code of {request.status_code}")
#         else:
#             try:
#                 if self.args["DEBUG"]:
#                     logging.debug(request.json())
#                 eventId = request.json()['data']['startShipEvent']['id']
#             except:
#                 eventId = None
#                 if self.args["WARNINGS"]:
#                     logging.warning("Failed to get id from server")
#             if self.args["INFO"]:
#                 print(f"start event {eventId} type {self.eventType} in camera {self.cameraId} in time {self.current_time}")
#         self.id = eventId
#         self.startTime, self.lastUpdate = time.time()
#         self.open = True
#
#     def publishShipEvent(self):
#         string_to_send = """
#            mutation{
#                publishShipEvent(eventId: %d, publish: true){
#                id
#              }
#            }""" % (self.id)
#         request = requests.post(self.args["URL"], json={'query': string_to_send})
#         if request.status_code != 200:
#             logging.error(f"Query failed to run by returning code of {request.status_code}")
#         else:
#             if self.args["DEBUG"]:
#                 logging.debug(request.json())
#             if self.args["DEBUG"]:
#                 print(
#                     f"Published event {self.id} type {self.eventType} in camera {self.cameraId} in time {self.current_time}")
#         self.lastUpdate = time.time()
#         self.published = True
#         self.publishedTime = time.time()
#
#     def sendDetection(self, detection):
#         if detection.x and detection.y:
#             num_objects = len(detection.x)
#             if num_objects <= 0:
#                 return
#             all_rects_str = ""
#             if True:
#                 empty_rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
#                     0, 0, 0, 0)
#                 all_rects_str += empty_rect_str
#             for i in range(num_objects):
#                 rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
#                     detection.x[i][0],
#                     detection.y[i][0], detection.x[i][1],
#                     detection.y[i][1])
#                 all_rects_str += rect_str
#             string_to_send = """
#                mutation{
#                    addShipDetection(event:{
#                      eventId: %d
#                      serialId: %d
#                      boundingAreas: [%s]
#                    }){
#                      id,
#                      serialId,
#                      boundingAreas {
#                        x1, y1, x2, y2
#                      }
#                    }
#                    }""" % (self.id, detection.serialId, all_rects_str)
#         else:
#             string_to_send = """
#                mutation
#                {
#                    addShipDetection(event:{
#                      eventId: %d
#                      serialId: %d
#                      boundingAreas: {x1:0.0,y1:0.0,x2:0.0,y2:0.0}
#                    }){
#                      id,
#                      boundingAreas {
#                        x1, y1, x2, y2
#                      }
#                    }
#                }""" % (self.id)
#         if self.args["DEBUG"]:
#             logging.debug(string_to_send)
#         request = requests.post(self.args["URL"], json={'query': string_to_send})
#         if request.status_code != 200:
#             if self.args["WARNINGS"]:
#                 logging.warning(f"Query failed to run by returning code of {request.status_code}")
#         self.lastUpdate = time.time()
#
#     def fire_and_forget(self, detection):
#         threading.Thread(target=self.sendDetection, args=(self, detection)).start()
#
#     def endShipEvent(self):
#         time.sleep(0.1)
#         tempDetection = Detection
#         tempDetection.serialId, tempDetection.x, tempDetection.y = 0, [], []
#         self.fire_and_forget(tempDetection)
#         string_to_send = """
#            mutation{
#                endShipEvent(eventId:
#                  %d
#                ){
#                id,
#                  }
#                }
#            """ % (self.id)
#         request = requests.post(self.args["URL"], json={'query': string_to_send})
#         if self.args["INFO"]:
#             print(f"close event {self.id} type {self.eventType} in camera {self.cameraId} in time {self.current_time}")
#         if request.status_code != 200:
#             if self.args["WARNINGS"]:
#                 logging.warning(f"Query failed to run by returning code of {request.status_code}")
#         self.open = False
#         self.published = False
#
# class Events:
#     def __init__(self):
#         self.eventsList = []
#         self.openEventsOnly = bool
#
#     def __repr__(self):
#         return (f"[{self.eventsList}]")