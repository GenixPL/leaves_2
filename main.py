import os

import cv2

# RENAME FILES
# baseDirPath = os.path.dirname(__file__) + "/data/test/type_"
#
# for i in range(1, 7):
#     images = []
#     filesNames = os.listdir(baseDirPath + str(i))
#
#     counter = 1
#     for file in filesNames:
#         img = cv2.imread(baseDirPath + str(i) + "/" + file)
#         newFile = baseDirPath + str(i) + "/" + str(i) + "_" + str(counter) + ".jpg"
#         cv2.imwrite(newFile, img)
#         counter += 1

# CHECK CORRECTNESS
baseDirPath = os.path.dirname(__file__) + "/data/results/type_"
sum_counter = 0
for i in range(1, 7):
    files = os.listdir(baseDirPath + str(i))

    counter = 0
    for file in files:
        if file[0] == str(i):
            counter += 1

    sum_counter += counter

    print("class: " + str(i) + ", proper: " + str(counter))

print("sum proper: " + str(sum_counter / 60 * 100) + "%")