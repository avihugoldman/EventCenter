from camera import Camera
from massage import Massage
from event_master import EventMaster
from socket import *

class Test(Camera):
    def __init__(self, type):
        super().__init__()
        self.type = str(type)

    def start_test(self, eventType):
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(EventMaster.ADDR)
        file_exist = False
        list_of_videos_names = []
        list_of_tagging_files = []
        list_of_detections_times = []
        true_counter = []
        finished_list = []
        false_counter = []
        lenght_per_video = []
        time_diffrence_per_camera = []
        subclass_list = []
        list_of_subclass = []
        helmet_false_counter = []
        helmet_true_counter = []
        noDetectionsList = []
        eventType = EventMaster.convertEventIntToSTR(eventType)
        test_start_time = time.time()
        # max_lenght_of_video = input("please enter the longest video lenght in seconds")
        if eventType == "SMOKE":
            stream_files_file = open(EventMaster.VIDEO_STREAMS_SMOKE_PATH, "r")
            helmets = False
        else:
            stream_files_file = open(VIDEO_STREAMS_PATH, "r")
            helmets = True
        names_of_videos_temp = stream_files_file.readlines()
        # [names_of_videos_temp.pop(k) for k in range(len(names_of_videos_temp)) if names_of_videos_temp[k] == "\n"]
        names_of_videos_temp.pop(0)
        names_of_videos = [s[:-1] for s in names_of_videos_temp if s[-1] == "\n" and len(s) > 2]
        list_of_videos_names.append([os.path.basename(full_path) for full_path in names_of_videos])
        test_result_file = open("tag_test_file.txt", "w")
        for i in range(len(list_of_videos_names[0])):
            list_of_start_time = []
            list_of_end_time = []
            list_of_line_splitted = []
            subclass_list = []
            true_counter.append(0)
            finished_list.append(False)
            false_counter.append(0)
            helmet_false_counter.append(0)
            helmet_true_counter.append(0)
            time_diffrence_per_camera.append([])
            path = os.path.dirname(names_of_videos[i])
            list_of_videos_names[0][i] += ".txt"
            try:
                list_of_tagging_files.append(open(str(path) + '/' + str(list_of_videos_names[0][i]), "r"))
                file_exist = True
                temp = list_of_tagging_files[i].readline()
                temp_list = temp.split(':')
                lenght = int(temp_list[0]) * 60 + float(temp_list[1])
                lenght *= AVG_FRAME_RATE
                lenght_per_video.append(lenght)
                for line in list_of_tagging_files[i].readlines():
                    if line != "\n":
                        line_splitted = line.split()
                        list_of_line_splitted.append(line_splitted)
                        s_time = line_splitted[0]
                        start_time_l = s_time.split(':')
                        start_time = int(start_time_l[0]) * 60 + float(start_time_l[1])
                        start_time *= AVG_FRAME_RATE
                        list_of_start_time.append(start_time)
                        e_time = line_splitted[1]
                        end_time_l = e_time.split(':')
                        end_time = int(end_time_l[0]) * 60 + float(end_time_l[1])
                        end_time *= AVG_FRAME_RATE
                        list_of_end_time.append(end_time)
                        if helmets:
                            try:
                                subclass = line_splitted[2]
                                subclass_list.append(int(subclass))
                            except IndexError:
                                print(f"no subclass, check text file {list_of_tagging_files[i]}")
                                subclass = 0
                    else:
                        break
            except FileNotFoundError:
                if not str(list_of_videos_names[0][i]) == ".txt":
                    logging.warning(f"There is no file named {list_of_videos_names[0][i]}")
                file_exist = False
                list_of_start_time.append(0)
                list_of_end_time.append(0)
                lenght_per_video.append(1)
            if len(list_of_start_time) == 0 and len(list_of_end_time) == 0:
                noDetectionsList.append(True)
            else:
                noDetectionsList.append(False)
            list_of_detections_times.append((list_of_start_time, list_of_end_time))
            list_of_subclass.append(subclass_list)
            try:
                [time_diffrence_per_camera[i].append(
                    (list_of_detections_times[i][1][j] - list_of_detections_times[i][0][j])) for j in
                    range(len(list_of_videos_names[0]))]
            except:
                pass
        [fl.close() for fl in list_of_tagging_files]
        stream_files_file.close()
        print(f"The lenghts of the videos are: {lenght_per_video}")
        while True:
            list_of_strings = Massage.handle_massage(client)
            try:
                for string in list_of_strings:
                    if file_exist:
                        str_list = string.split(" ")
                        if DEBUG and str_list[0] != 'Non':
                            print(str_list)
                        serialId = int(str_list[1])
                        objSubclass = int(str_list[3])
                        cameraId = int(str_list[0])
                        total_detections_list = []
                        total_helmet_detection_list = []
                        if all(finished_list):
                            for i in range(len(true_counter)):
                                total_detections_list.append(true_counter[i] + false_counter[i])
                                total_helmet_detection_list.append(helmet_true_counter[i] + helmet_false_counter[i])
                                try:
                                    false_ratio = (false_counter[i] / total_detections_list[i]) * 100
                                except ZeroDivisionError:
                                    false_ratio = (false_counter[i] / (total_detections_list[i] + 1)) * 100
                                try:
                                    true_ratio = (true_counter[i] / sum(time_diffrence_per_camera[i])) * 100
                                except ZeroDivisionError:
                                    true_ratio = (true_counter[i] / (sum(time_diffrence_per_camera[i]) + 1)) * 100
                                if helmets:
                                    try:
                                        helmet_false_ratio = (helmet_false_counter[i] / total_helmet_detection_list[
                                            i]) * 100
                                    except ZeroDivisionError:
                                        helmet_false_ratio = (helmet_false_counter[i] / (
                                                total_helmet_detection_list[i] + 1)) * 100
                                    try:
                                        helmet_true_ratio = (helmet_true_counter[i] / sum(
                                            time_diffrence_per_camera[i])) * 100
                                    except ZeroDivisionError:
                                        helmet_true_ratio = (helmet_true_counter[i] / (
                                                sum(time_diffrence_per_camera[i]) + 1)) * 100
                                test_result_file.write(f"For video {list_of_videos_names[0][i]}: \n")
                                test_result_file.write(f"Number of true detections is: {true_counter[i]} \n")
                                test_result_file.write(f"Number of false detections is: {false_counter[i]} \n")
                                test_result_file.write(f"The true detection ratio is: {true_ratio} \n")
                                if helmets:
                                    test_result_file.write(f"The false detection ratio is: {false_ratio} \n")
                                else:
                                    test_result_file.write(f"The false detection ratio is: {false_ratio} \n\n")
                                if helmets:
                                    test_result_file.write(
                                        f"Number of helmet true detections is: {helmet_true_counter[i]} \n")
                                    test_result_file.write(
                                        f"Number of helmet false detections is: {helmet_false_counter[i]} \n")
                                    test_result_file.write(
                                        f"The true helmet detection ratio is: {helmet_true_ratio} \n")
                                    test_result_file.write(
                                        f"The false helmet detection ratio is: {helmet_false_ratio} \n\n")
                            test_result_file.close()
                            print("finished the test, see results in the file")
                            raise Finisihed_Error
                        for i in range(len(finished_list)):
                            if serialId > lenght_per_video[i] and not finished_list[i]:
                                print(f"{list_of_videos_names[0][i]} has finished")
                                finished_list[i] = True
                        counter = 0
                        for j in range(len(list_of_detections_times[cameraId])):
                            if noDetectionsList[cameraId] and not finished_list[cameraId]:
                                false_counter[cameraId] += 1
                                break
                            if serialId >= list_of_detections_times[cameraId][1][j] + 15 and counter < len(
                                    list_of_detections_times[cameraId]):
                                counter += 1
                                continue
                            if serialId >= list_of_detections_times[cameraId][0][j] and serialId <= \
                                    list_of_detections_times[cameraId][1][j]:
                                if not finished_list[cameraId]:
                                    true_counter[cameraId] += 1
                                    if helmets:
                                        if objSubclass == 2 and int(list_of_subclass[cameraId][j]) == 0:
                                            helmet_true_counter[cameraId] += 1
                                        elif objSubclass == 1 and int(list_of_subclass[cameraId][j]) == 1:
                                            helmet_true_counter[cameraId] += 1
                                        elif objSubclass == 0:
                                            pass
                                        else:
                                            helmet_false_counter[cameraId] += 1
                                break
                            else:
                                if not finished_list[cameraId]:
                                    if serialId < list_of_detections_times[cameraId][0][j] - 25 or serialId > \
                                            list_of_detections_times[cameraId][1][j] + 25:
                                        false_counter[cameraId] += 1
            except ValueError and IndexError:
                if (time.time() - test_start_time) / 25 > max(lenght_per_video):
                    finished_list = [True for item in finished_list]
                    if (time.time() - test_start_time) / 25 / 25 > max(lenght_per_video) * 2:
                        print("No events in all videos!")
                        raise ZeroDivisionError

class Finisihed_Error(Exception):
    pass