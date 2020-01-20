import os
import cv2
import numpy as np

# https://arxiv.org/pdf/1401.4447.pdf
from utils.models.set_slimness import SetSlimness


class SetTrainer:

    def __init__(self, set_path):
        self.set_path = set_path

        self.filesNames = os.listdir(set_path)

        self.images = self.load_images()

        self.contours = self.load_contours()


    def train(self):
        # for i in range(0, len(self.images)):
        #     cv2.drawContours(self.images[i], self.contours[i], -1, (255, 0, 0), 2)
        #
        #     cv2.imshow("image", self.images[i])
        #     cv2.waitKey(0)

        slimness = self.get_slimness()
        print(self.set_path + "\tslimness -> smallest: " + str(slimness.smallest_ratio) + ", biggest: " + str(slimness.biggest_ratio))


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

    # TRAINING

    def get_slimness(self):
        smallest_ration = 100
        biggest_ration = 0

        for c in self.contours:
            x, y, w, h = cv2.boundingRect(c)
            ration = float(w) / float(h)

            if ration > biggest_ration:
                biggest_ration = ration

            if ration < smallest_ration:
                smallest_ration = ration

        return SetSlimness(smallest_ration, biggest_ration)