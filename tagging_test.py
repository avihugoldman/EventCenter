import cv2
import os
import time
from tkinter import filedialog
from os.path import splitext
from os import listdir, mkdir
import numpy as np

BASE_IMAGE_SIZE = (512, 512)
FONT = cv2.FONT_HERSHEY_SIMPLEX
BLACK = (0, 0, 0)
WHITE = (400, 450, 500)
YELLOW = (255, 0, 0)


def check_tagging():
    # read txt file of tagging and opens a player in the event time
    temp = input("How many seconds do you want to jump in keyboard press?")
    if temp:
        try:
            SECOND_JUMP = float(temp)
        except ValueError:
            SECOND_JUMP = 0.5
    else:
        SECOND_JUMP = 0.5

    temp2 = input("which color do you want for the text? for black press 'b', for white press 'w': ")
    if temp2:
        if temp2 == 'b':
            color_2 = BLACK
        elif temp2 == 'w':
            color_2 = WHITE
    else:
        color_2 = WHITE
    while True:
        temp = input("press 'e' to exit or 'enter' to continue")
        if temp == "e":
            break
        print("Chose directory:")
        selected_dir = filedialog.askdirectory()
        print("selected_dir:", selected_dir)
        time.sleep(1)
        print("********To go foward press 'F', To go backward press 'B', To back to start press 's', To jump to the end press 'Ee if you find an error, please press 'L' ********")
        time.sleep(2)
        # while True:
        # ccc = input("Ok to continue (y: continue   q: quit) ? ")
        # if (ccc == 'y'):
        # break
        # if (ccc == 'q'):
        # print("quitting")
        # return
        rootdir = os.walk(selected_dir)
        for root, subd, fils in rootdir:
            start_time_list, end_time_list, list_of_line_splitted = [], [], []
            f = open("/Users/avihugoldman/Documents/Captains Eye"+ "/" + "error_log.txt", "w")
            for name in fils:
                if name == 'error_log.txt':
                    continue
                full_path = root + "/" + name
                if ".txt" in splitext(name):
                    try:
                        start_time_list, list_of_line_splitted, end_time_list= [], [], []
                        input_text_file = open(full_path, 'r')
                        lines = input_text_file.readlines()
                        for line in lines:
                            if line != "\n":
                                line_splitted = line.split()
                                list_of_line_splitted.append(line_splitted)
                                s_time = line_splitted[2]
                                start_time_l = s_time.split(':')
                                start_time = int(start_time_l[0]) * 60 + float(start_time_l[1])
                                start_time_list.append(start_time)
                                e_time = line_splitted[3]
                                end_time_l = e_time.split(':')
                                end_time = int(end_time_l[0]) * 60 + float(end_time_l[1])
                                end_time_list.append(end_time)
                            else:
                                break
                        full_path = full_path.rstrip(".txt")
                        in_video_capture = cv2.VideoCapture(full_path)
                        fps = in_video_capture.get(cv2.CAP_PROP_FPS)
                        FRAME_JUMP = SECOND_JUMP * fps
                        num_of_frames = in_video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
                        clip_length = num_of_frames / fps
                        success, frame = in_video_capture.read()
                        # frame_num = in_video_capture.get(cv2.CAP_PROP_POS_FRAMES)
                        for i in range(len(start_time_list)):
                            frame_start = start_time_list[i] * fps
                            frame_end = end_time_list[i] * fps
                            print(frame_start, frame_end)
                            j = frame_start
                            # lines = [" ".join(line.split()) for line in lines]
                            x1 = 0
                            y1 = 0
                            x2 = 0
                            y2 = 0
                            text4 = str(name)
                            text1 = str(list_of_line_splitted[i][0]) + " " + str(list_of_line_splitted[i][1]) + " " + str(
                                list_of_line_splitted[i][2]) + " " + str(list_of_line_splitted[i][3]) \
                                    + " " + str(list_of_line_splitted[i][4]) + " " + str(list_of_line_splitted[i][5]) \
                                    + " " + str(list_of_line_splitted[i][6]) + " " + str(
                                list_of_line_splitted[i][7]) + " " + str(list_of_line_splitted[i][8]) + " " + str(
                                list_of_line_splitted[i][9])
                            if any("roi" in s for s in list_of_line_splitted[i]):
                                roi_index = [idx for idx, t in enumerate(list_of_line_splitted[i]) if "roi" in t][0]
                                temp = [float(list_of_line_splitted[i][roi_index + 1]), float(list_of_line_splitted[i][roi_index + 2]),
                                        float(list_of_line_splitted[i][roi_index + 3]), float(list_of_line_splitted[i][roi_index + 4])]
                                text2 = str(list_of_line_splitted[i][roi_index - 2]) + " " + str(list_of_line_splitted[i][roi_index - 1])
                                x1 = int((temp[0] - (temp[2] / 2)) * BASE_IMAGE_SIZE[0])
                                y1 = int((temp[1] - (temp[3] / 2)) * BASE_IMAGE_SIZE[1])
                                x2 = int((temp[0] + (temp[2] / 2)) * BASE_IMAGE_SIZE[0])
                                y2 = int((temp[1] + (temp[3] / 2)) * BASE_IMAGE_SIZE[1])
                                text3 = " "
                            else:
                                try:
                                    text3 = str(list_of_line_splitted[i][14]) + " " + str(list_of_line_splitted[i][15]) + " " + str(
                                        list_of_line_splitted[i][16]) + " " + str(list_of_line_splitted[i][17])
                                    text2 = str(list_of_line_splitted[i][10]) + " " + str(
                                        list_of_line_splitted[i][11]) + " " + str(list_of_line_splitted[i][12]) \
                                            + " " + str(list_of_line_splitted[i][13])
                                except:
                                    text3 = " "
                                    text2 = " "
                            in_video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
                            while j < (end_time_list[i] * fps) - 1 and j >= frame_start and success:
                                success, frame = in_video_capture.read()
                                if (j % FRAME_JUMP) == 0:
                                    frame = np.ascontiguousarray(frame, dtype=np.uint8)
                                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), YELLOW, 2)
                                    cv2.putText(frame, text1, (10, 450), FONT, 0.6, color_2, thickness=2)
                                    cv2.putText(frame, text2, (10, 470), FONT, 0.6, color_2, thickness=2)
                                    cv2.putText(frame, text3, (260, 470), FONT, 0.6, color_2, thickness=2)
                                    cv2.putText(frame, str(j), (260, 20), FONT, 0.6, color_2, thickness=1)
                                    cv2.imshow("avihu", frame)
                                    key = cv2.waitKey(0)
                                    if key == ord("l"):
                                        f.write(f"in {name} there is an error in line {i+1}: {str(list_of_line_splitted[i]).strip('[]'',')}\n")
                                        break
                                    elif key == ord("q"):
                                        break
                                    elif key == ord("f"):
                                        continue
                                    elif key == ord("b"):
                                        in_video_capture.set(cv2.CAP_PROP_POS_FRAMES, in_video_capture.get(cv2.CAP_PROP_POS_FRAMES) - 4 * FRAME_JUMP)
                                        if in_video_capture.get(cv2.CAP_PROP_POS_FRAMES) < frame_start:
                                            in_video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
                                        continue
                                    elif key == ord("s"):
                                        in_video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
                                        j = frame_start
                                        continue
                                    elif key == ord("e"):
                                        in_video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_end - 1)
                                        j = frame_end - 1
                                        continue
                                j += 1
                    except:
                        print("error reading  file: ", name)
                        continue
                else:
                    continue
            f.close()
        cv2.destroyAllWindows()

check_tagging()