import argparse
import os
import sys
from cv2 import cv2 as open_cv
import time
import yaml
from motion_detector import MotionDetector
from sql_worker import SQL as Database

def main():
    args = parse_args()

    street_name = args.name
    camera_link = args.camera
    url = findCurrentMinute(camera_link)

    db = Database()

    with open("recognition/data/" + street_name + ".yml", "r") as data:
        points = yaml.load(data)
        while True:
            detector = MotionDetector(url, points)
            start_time = time.time()
            space_amount = detector.detect_motion(street_name)
            db.set_spaces_amount(1, space_amount)
            exec_time = time.time() - start_time
            time.sleep(63 - exec_time)
            url = nextUrl(url)
            print(url)

def findCurrentMinute(without_id):
    current_timestamp = round(time.time())
    while True:
        # capture = open_cv.VideoCapture(without_id + str(current_timestamp) + '.mp4')
        # capture.set(6, open_cv.VideoWriter_fourcc('H', '2', '6', '4'))
        if (open_cv.VideoCapture(without_id + str(current_timestamp) + '.mp4').isOpened()):
            print("Opened")
            return without_id + str(current_timestamp) + '.mp4'
        print("Aint found")
        current_timestamp = current_timestamp - 1


def nextUrl(currentUrl):
    id = int(currentUrl.split('_')[1].split('.')[0]) + 62
    without_id = currentUrl.split('_')[0]
    if (open_cv.VideoCapture(without_id + "_" + str(id) + '.mp4').isOpened()):
        print("Default")
        return without_id + "_" + str(id) + '.mp4'
    elif (open_cv.VideoCapture(without_id + "_" + str(id - 1) + '.mp4').isOpened()):
        print("-1")
        return without_id + "_" + str(id - 1) + '.mp4'
    elif (open_cv.VideoCapture(without_id + "_" + str(id + 1) + '.mp4').isOpened()):
        print("+1")
        return without_id + "_" + str(id + 1) + '.mp4'
    else:
        print("fuck up")
        return findCurrentMinute(without_id + "_")

def parse_args():
    parser = argparse.ArgumentParser(description='Start recognition')

    parser.add_argument("--name",
                        dest="name",
                        required=True,
                        help="Name of street")

    parser.add_argument("--camera",
                        dest="camera",
                        required=True,
                        help="Link to camera")

    return parser.parse_args()


if __name__ == '__main__':
    main()