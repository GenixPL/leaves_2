import os
import cv2
import numpy as np

from utils.models.set_dispersion import SetDispersion
from utils.models.set_roundness import SetRoundness
from utils.models.set_slimness import SetSlimness


# https://arxiv.org/pdf/1401.4447.pdf
# https://medium.com/analytics-vidhya/tutorial-how-to-scale-and-rotate-contours-in-opencv-using-python-f48be59c35a2


class SetClass:

    def __init__(self, set_path, class_id):
        self.set_path = set_path
        self.class_id = class_id

        self.filesNames = os.listdir(set_path)

        self.images = self.load_images()

        self.contours = self.load_contours()
        self.contours = self.rotate_contours()

        self.slimness: SetSlimness = None
        self.roundness: SetRoundness = None
        self.dispersion: SetDispersion = None

    def train(self):
        # for i in range(0, len(self.images)):
        #     cv2.drawContours(self.images[i], self.contours[i], -1, (255, 0, 0), 2)
        #
        #     cv2.imshow("image", self.images[i])
        #     cv2.waitKey(0)

        self.slimness = self.get_slimness()
        self.roundness = self.get_roundness()
        self.dispersion = self.get_dispersion()

    # PRIVATE

    # INIT

    def load_images(self):
        images = []

        for f in self.filesNames:
            images.append(cv2.imread(self.set_path + "/" + f))

        return images

    def load_contours(self):
        contours = []

        for i in self.images:
            hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)

            low_green = np.array([0, 18, 0])
            high_green = np.array([255, 255, 255])
            green_mask = cv2.inRange(hsv, low_green, high_green)

            temp_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            biggest_contour = temp_contours[0]
            biggest_area = 0
            for contour in temp_contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                if area > biggest_area:
                    biggest_area = area
                    biggest_contour = contour

            contours.append(biggest_contour)

        return contours

    def rotate_contours(self):
        contours = []

        for contour in self.contours:
            c = contour.copy()

            x, y, w, h = cv2.boundingRect(c)

            # create rotated
            max_hr = h
            max_rotation = c
            for angle in range(0, 180, 5):
                rotated = rotate_contour(c, angle)
                xr, yr, wr, hr = cv2.boundingRect(rotated)
                if hr > max_hr:
                    max_hr = hr
                    max_rotation = rotated

            contours.append(max_rotation)

            # DISPLAY RESULTS
            # M = cv2.moments(c)
            # cx = int(M['m10'] / M['m00'])
            # cy = int(M['m01'] / M['m00'])
            #
            # print("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h))
            # print(str(cx) + " " + str(cy))
            #
            # blank_image = np.zeros((1000, 1000, 3), np.uint8)
            # cv2.drawContours(blank_image, c, -1, (255, 0, 0), 2)
            # cv2.circle(blank_image, (cx, cy), 7, (255, 0, 0), -1)
            #
            # cv2.drawContours(blank_image, max_rotation, -1, (0, 0, 255), 2)
            #
            # cv2.imshow("image", blank_image)
            # cv2.waitKey(0)

        return contours

    # TRAINING

    def get_slimness(self):
        set_slimness = SetSlimness()

        for c in self.contours:
            set_slimness.add_value(slimness(c))

        return set_slimness

    def get_roundness(self):
        set_roundness = SetRoundness()

        for c in self.contours:
            set_roundness.add_value(roundness(c))

        return set_roundness

    def get_dispersion(self):
        set_dispersion = SetDispersion()

        for c in self.contours:
            set_dispersion.add_value(dispersion(c))

        return set_dispersion


# HELPERS

def contour(file_path):
    img = cv2.imread(file_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    low_green = np.array([0, 18, 0])
    high_green = np.array([255, 255, 255])
    green_mask = cv2.inRange(hsv, low_green, high_green)

    temp_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = temp_contours[0]
    biggest_area = 0
    for contour in temp_contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > biggest_area:
            biggest_area = area
            biggest_contour = contour

    c = biggest_contour.copy()

    x, y, w, h = cv2.boundingRect(c)

    # create rotated
    max_hr = h
    max_rotation = c
    for angle in range(0, 180, 5):
        rotated = rotate_contour(c, angle)
        xr, yr, wr, hr = cv2.boundingRect(rotated)
        if hr > max_hr:
            max_hr = hr
            max_rotation = rotated

    return max_rotation


def slimness(contour):
    x, y, w, h = cv2.boundingRect(contour)
    ratio = float(w) / float(h)
    return ratio


def roundness(contour):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    return (4 * 3.14159 * area) / (perimeter ** 2)


def dispersion(contour):
    M = cv2.moments(contour)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cx = float(cx)
    cy = float(cy)

    max_val = 0
    min_val = 1000000

    for t in contour:
        (x, y) = tuple(t[0])
        val = np.math.sqrt((float(x) - cx) ** 2 + (float(y) - cy) ** 2)

        if val > max_val:
            max_val = val

        if val < min_val:
            min_val = val

    return float(max_val / min_val)





def rotate_contour(cnt, angle):
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    cnt_norm = cnt - [cx, cy]

    coordinates = cnt_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cart2pol(xs, ys)

    thetas = np.rad2deg(thetas)
    thetas = (thetas + angle) % 360
    thetas = np.deg2rad(thetas)

    xs, ys = pol2cart(thetas, rhos)

    cnt_norm[:, 0, 0] = xs
    cnt_norm[:, 0, 1] = ys

    cnt_rotated = cnt_norm + [cx, cy]
    cnt_rotated = cnt_rotated.astype(np.int32)

    return cnt_rotated


def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y
