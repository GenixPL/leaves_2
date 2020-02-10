import cv2

import utils.set_class as sc


class NaiveBayes:

    def __init__(self, base_path, classes):
        self.classes = classes

        for i in range(1, 7):  # TODO 7
            for j in range(1, 11):  # TODO 11
                file_name = str(i) + "_" + str(j) + ".jpg"
                path = base_path + "test/type_" + str(i) + "/" + file_name
                contour = sc.contour(path)
                img = sc.get_img_with_mask(path)

                probs = []
                probs.append(self.prob_for_class(1, contour, img, path))
                probs.append(self.prob_for_class(2, contour, img, path))
                probs.append(self.prob_for_class(3, contour, img, path))
                probs.append(self.prob_for_class(4, contour, img, path))
                probs.append(self.prob_for_class(5, contour, img, path))
                probs.append(self.prob_for_class(6, contour, img, path))

                max_prob = 0
                max_class = 0
                for x in range(0, 6):
                    if probs[x] > max_prob:
                        max_prob = probs[x]
                        max_class = x

                write_path = base_path + "/results/type_" + str(max_class + 1) + "/" + file_name
                cv2.imwrite(write_path, img)

    def prob_for_class(self, class_id, contour, image, file_path) -> float:
        proper_class: sc.SetClass

        for c in self.classes:
            if c.class_id == class_id:
                proper_class = c

        ps = proper_class.slimness.get_prob(sc.slimness(contour))
        pr = proper_class.roundness.get_prob(sc.roundness(contour))
        pd = proper_class.dispersion.get_prob(sc.dispersion(contour))
        pg = proper_class.green_color.get_prob(sc.get_green_color(image, sc.get_green_mask(file_path)))

        return pr * pd * pg