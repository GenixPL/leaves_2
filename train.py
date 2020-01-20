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


    # slimness = set.dispersion
    # print(setDirPath + "\tslimness -> average: " + str(slimness.get_mean()) +
    #       ", limited avg:" + str(slimness.get_average_without_outliers()) +
    #       ", smallest: " + str(slimness.smallest) +
    #       ", biggest: " + str(slimness.biggest))
    #
    # roundness = set.roundness
    # print(setDirPath + "\troundness -> average: " + str(roundness.get_mean()) +
    #       ", limited avg:" + str(roundness.get_average_without_outliers()) +
    #       ", smallest: " + str(roundness.smallest) +
    #       ", biggest: " + str(roundness.biggest))
    #
    # dispersion = set.dispersion
    # print(setDirPath + "\tdispersion -> average: " + str(dispersion.get_mean()) +
    #       ", limited avg:" + str(dispersion.get_average_without_outliers()) +
    #       ", smallest: " + str(dispersion.smallest) +
    #       ", biggest: " + str(dispersion.biggest))
    #
    # print


NaiveBayes(os.path.dirname(__file__) + "/data/", classes)