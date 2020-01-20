import os

from utils.naive_bayes import NaiveBayes
from utils.set_class import SetClass

baseDirPath = os.path.dirname(__file__) + "/data/train/"

classes = []
for i in range(1, 7):  # TODO (7)
    setDirPath = baseDirPath + "type_" + str(i)

    set = SetClass(setDirPath, i)
    set.train()
    classes.append(set)

NaiveBayes(os.path.dirname(__file__) + "/data/", classes)