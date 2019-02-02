# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np
import cv2
import matplotlib.pyplot as plt
from rect import Rect
# display plots in this notebook
# %matplotlib inline
# filter out the warnings
import warnings
import time
warnings.filterwarnings('ignore')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def current_time():
    return int(round(time.time() * 1000))


def merge_overlapping_boxes(eye_rects):
    final_boxes = []
    overlapping_boxes = []

    for rect in eye_rects:
        overlapping_boxes.append(False)

    had_overlap = False

    # print('E', eye_rects)

    for i in range(len(eye_rects)):
        for j in range(i + 1, len(eye_rects)):
            print('Checking:', i, 'vs', j)
            if eye_rects[i].intersects(eye_rects[j]):
                had_overlap = True
                overlapping_boxes[i] = True
                overlapping_boxes[j] = True

                print(i, 'intersects', j)
                # Determine which is leftmost
                i_leftmost = False
                i_upmost = False

                # x = eye_rects[i].get_x()
                # y = eye_rects[i].get_y()
                # width = eye_rects[i].get_w()
                # height = eye_rects[i].get_h()

                if eye_rects[i].get_x() < eye_rects[j].get_x():
                    i_leftmost = True
                    x = eye_rects[i].get_x()
                    overlap_x = (eye_rects[i].get_x() + eye_rects[i].get_w()) - eye_rects[j].get_x()
                else:
                    x = eye_rects[j].get_x()
                    overlap_x = (eye_rects[j].get_x() + eye_rects[j].get_w()) - eye_rects[i].get_x()
                    # width = (x - eye_rects[i].get_x()) + overlap + (eye_rects[i].get_w() - overlap)
                if eye_rects[i].get_y() < eye_rects[j].get_y():
                    i_upmost = True
                    y = eye_rects[i].get_y()
                    overlap_y = (eye_rects[i].get_y() + eye_rects[i].get_h()) - eye_rects[j].get_y()
                    # height = (y - eye_rects[j].get_y()) + overlap + (eye_rects[j].get_h() - overlap)
                else:
                    y = eye_rects[j].get_y()
                    overlap_y = (eye_rects[j].get_y() + eye_rects[j].get_h()) - eye_rects[i].get_y()
                    # height = (x - eye_rects[i].get_y()) + overlap + (eye_rects[i].get_h() - overlap)

                width = eye_rects[i].get_w() + eye_rects[j].get_w() - overlap_x
                height = eye_rects[i].get_h() + eye_rects[j].get_h() - overlap_y

                final_boxes.append(Rect(x, y, width, height))

    for i, rect in enumerate(overlapping_boxes):
        if rect is False:
            final_boxes.append(eye_rects[i])

    if had_overlap:
        return merge_overlapping_boxes(final_boxes)

    return final_boxes


def extract_face_features(face, img, gray):
    [x, y, w, h] = face
    roi_gray = gray[y:y + h, x:x + w]
    face_image = np.copy(img[y:y + h, x:x + w])

    eyes = eye_cascade.detectMultiScale(roi_gray)
    eye_images = []
    eye_rects = []
    # for (ex, ey, ew, eh) in eyes:
    #     if ew > w / 15 and ey < h / 2:
    #         eye_images.append(np.copy(img[y + ey:y + ey + eh, x + ex:x + ex + ew]))

    roi_color = img[y:y + h, x:x + w]
    for (ex, ey, ew, eh) in eyes:
        if ew > w / 15 and ey < h / 2:
            eye_rects.append(Rect(ex, ey, ew, eh))
            # Todo: Loop through merged eye rects and produce these rectangles
            # cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    merged_eye_rects = merge_overlapping_boxes(eye_rects)
    print('M', merged_eye_rects)
    for eye in merged_eye_rects:
        print(eye.get())
        ex, ey, ew, eh = eye.get()
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    return face_image, eye_images


def get_face_grid(face, frameW, frameH, gridSize):
    faceX, faceY, faceW, faceH = face

    return faceGridFromFaceRect(frameW, frameH, gridSize, gridSize, faceX, faceY, faceW, faceH, False)


def extract_image_features(full_img_path):
    img = cv2.imread(full_img_path)
    start_ms = current_time()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detections = face_cascade.detectMultiScale(gray, 1.3, 5)

    faces = []
    face_features = []
    for [x, y, w, h] in face_detections:
        face = [x, y, w, h]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_image, eye_images = extract_face_features(face, img, gray)
        face_grid = get_face_grid(face, img.shape[1], img.shape[0], 25)

        faces.append(face)
        face_features.append([face_image, eye_images, face_grid])

    duration_ms = current_time() - start_ms
    print("Face and eye extraction took: ", str(duration_ms / 1000) + "s")

    return img, faces, face_features


gridSize = 25


# Given face detection data, generate face grid data.
#
# Input Parameters:
# - frameW/H: The frame in which the detections exist
# - gridW/H: The size of the grid (typically same aspect ratio as the
#     frame, but much smaller)
# - labelFaceX/Y/W/H: The face detection (x and y are 0-based image
#     coordinates)
# - parameterized: Whether to actually output the grid or just the
#     [x y w h] of the 1s square within the gridW x gridH grid.

def faceGridFromFaceRect(frameW, frameH, gridW, gridH, labelFaceX, labelFaceY, labelFaceW, labelFaceH, parameterized):
    scaleX = gridW / frameW
    scaleY = gridH / frameH

    if parameterized:
        labelFaceGrid = np.zeros(4)
    else:
        labelFaceGrid = np.zeros(gridW * gridH)

    grid = np.zeros((gridH, gridW))

    # Use one-based image coordinates.
    xLo = round(labelFaceX * scaleX)
    yLo = round(labelFaceY * scaleY)
    w = round(labelFaceW * scaleX)
    h = round(labelFaceH * scaleY)

    if parameterized:
        labelFaceGrid = [xLo, yLo, w, h]
    else:
        xHi = xLo + w
        yHi = yLo + h

        # Clamp the values in the range.
        xLo = int(min(gridW, max(0, xLo)))
        xHi = int(min(gridW, max(0, xHi)))
        yLo = int(min(gridH, max(0, yLo)))
        yHi = int(min(gridH, max(0, yHi)))

        faceLocation = np.ones((yHi - yLo, xHi - xLo))
        grid[yLo:yHi, xLo:xHi] = faceLocation

        # Flatten the grid.
        grid = np.transpose(grid)
        labelFaceGrid = grid.flatten()

    return labelFaceGrid


def set_title_and_hide_axis(title):
    plt.title(title)
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)


def render_face_grid(face_grid):
    to_print = np.copy(face_grid)
    result_image = np.copy(to_print).reshape(25, 25).transpose()
    plt.figure()
    set_title_and_hide_axis('Face grid')
#     print(result_image.shape)
    plt.imshow(result_image)


# Removed params: , faces, face_features
def show_extraction_results(img):
    plt.figure(figsize=(10,10))
    set_title_and_hide_axis('Original image and extracted features')
    # Original image with overlay
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), interpolation="bicubic")
    plt.show()

    # final_img = extract_image_features(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # return final_img
    # return final_img

    # for i, face in enumerate(faces):
    #     print('Face #' + str(i))
    #     #print('i', face, i)
    #     face_image, eye_images, face_grid = face_features[i]
    #     plt.figure()
    #     # set_title_and_hide_axis('Extracted face image')
    #     # plt.imshow(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB), interpolation="bicubic")
    #     # plt.figure()
    #     # plt.show()
    #     #print('face image after extraction')
    #     render_face_grid(face_grid)
    #
    #     # for eye_image in eye_images:
    #     #     plt.figure()
    #     #
    #     #     #print('eye image after extraction')
    #     #     set_title_and_hide_axis('Extracted eye image')
    #     #     plt.imshow(cv2.cvtColor(eye_image, cv2.COLOR_BGR2RGB), interpolation="bicubic")
    #     #     plt.show()


def show_webcam(mirror=True):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        # Do facial recognition and then draw this
        img = show_extraction_results(img)
        cv2.imshow('my webcam', img)

        k = cv2.waitKey(1)

        if k % 256 == 27:
            break  # esc to quit
        elif k % 256 == 32:
            print('Space')

    cam.release()
    cv2.destroyAllWindows()


# show_webcam()
img, faces, face_features = extract_image_features('photos/Galvanize Headshot Cropped.JPG')
show_extraction_results(img)