import numpy as np
import cv2
import matplotlib.pyplot as plt
from rect import Rect
import time
import argparse
import imutils
from imutils import face_utils
from scipy.spatial import distance
import dlib


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")

args = vars(ap.parse_args())


class EyeTracker:
    x = 0
    y = 0
    left_closed = False
    right_closed = False

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    cap = cv2.VideoCapture(0)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    past_values_x = []
    past_values_y = []

    flag = 0

    def __init__(self):
        pass

    def get_eye_info(self, frame):
        return EyePacket(self.left_closed, self.right_closed, self.x, self.y)

    def min_intensity_x(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        min_sum_y = 255 * len(img)
        min_index_x = -1

        for x in range(len(img[0])):

            temp_sum_y = 0

            for y in range(len(img)):
                temp_sum_y += img[y][x]

            if temp_sum_y < min_sum_y:
                min_sum_y = temp_sum_y
                min_index_x = x

        self.past_values_x.append(min_index_x)

        if len(self.past_values_x) > 3:
            self.past_values_x.pop(0)

        return int(sum(self.past_values_x) / len(self.past_values_x))

    def min_intensity_y(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        min_sum_x = 255 * len(img[0])
        min_index_y = -1

        for y in range(len(img)):

            temp_sum_x = 0

            for x in range(len(img[0])):
                temp_sum_x += img[y][x]

            if temp_sum_x < min_sum_x:
                min_sum_x = temp_sum_x
                min_index_y = y

        self.past_values_y.append(min_index_y)

        if len(self.past_values_y) > 3:
            self.past_values_y.pop(0)

        return int(sum(self.past_values_y) / len(self.past_values_y))

    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def extract_eye(self, image, left, bottom_left, bottom_right, right, upper_right, upper_left):
        lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
        upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

        eye = image[upper_bound - 3:lower_bound + 3, left[0] - 3:right[0] + 3]

        self.x = pupil_x = self.min_intensity_x(eye)
        self.y = pupil_y = self.min_intensity_y(eye)

        cv2.line(eye, (pupil_x, 0), (pupil_x, len(eye)), (0, 255, 0), 1)
        cv2.line(eye, (0, pupil_y), (len(eye[0]), pupil_y), (0, 255, 0), 1)

        cv2.line(image, (int((bottom_left[0] + bottom_right[0]) / 2), lower_bound), (int((upper_left[0] + upper_right[0]) / 2), upper_bound), (0, 0, 255), 1)
        cv2.line(image, (left[0], left[1]), (right[0], right[1]), (0, 0, 255), 1)

        image[upper_bound - 3:lower_bound + 3, left[0] - 3:right[0] + 3] = eye
        return eye

    def detect_closed_eyes(self, image):
        thresh = 0.3  # Higher thresh, more often finds closed eyes
        frame_check = 3  # Alters how long you have to close your eye to draw

        # Drowsiness Tracker
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        subjects = self.detector(gray, 0)
        for subject in subjects:
            shape = self.predictor(gray, subject)
            shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < thresh:
                print('Eye closed?', self.flag)
                if leftEAR < rightEAR:
                    self.left_closed = True
                    print('left closed')
                else:
                    self.right_closed = True
                    print('right closed')

                self.flag += 1
                # print (flag)
                if self.flag >= frame_check:
                    cv2.putText(image, "****************ALERT!****************", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(image, "****************ALERT!****************", (10, 325),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.left_closed = False
                self.right_closed = False
                self.flag = 0
        # cv2.imshow("Frame", image)

    def run(self):
        while True:
            # load the input image, resize it, and convert it to grayscale
            ret, image = self.cap.read()
            image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale image
            rects = self.detector(gray, 1)

            # loop over the face detections
            for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # convert dlib's rectangle to a OpenCV-style bounding box
                # [i.e., (x, y, w, h)], then draw the face bounding box
                # (x, y, w, h) = face_utils.rect_to_bb(rect)
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # show the face number
                # cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
                #	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # loop over the (x, y)-coordinates for the facial landmarks
                # and draw them on the image
                count = 1
                right_eye = imutils.resize(self.extract_eye(image, shape[36], shape[41], shape[40], shape[39], shape[38], shape[37]), width=100, height=50)

                for (x, y) in shape:
                    if count > 36 and count < 43:
                        cv2.circle(image, (x, y), 1, (255, 0, 0), -1)

                    count += 1

                image[0:len(right_eye), 0:len(right_eye[0])] = right_eye
            self.detect_closed_eyes(image)
            cv2.imshow("PupilTrack v.0.1", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


class EyePacket:

    def __init__(self, left_is_closed, right_is_closed, x, y):
        self.left_is_closed = left_is_closed
        self.right_is_closed = right_is_closed
        self.x = x
        self.y = y

run = EyeTracker()
run.run()