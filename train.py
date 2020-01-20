import os

from utils.set_trainer import SetTrainer


baseDirPath = os.path.dirname(__file__) + "/data/train/"

for i in range(1, 7):  # TODO (7)
    setDirPath = baseDirPath + "type_" + str(i)

    set = SetTrainer(setDirPath)
    set.train()

    slimness = set.slimness
    # print(setDirPath + "\tslimness -> average: " + str(slimness.get_average()) + ", smallest: " +
    #       str(slimness.smallest) + ", biggest: " + str(slimness.biggest))

    roundness = set.roundness
    print(setDirPath + "\troundness -> average: " + str(roundness.get_average()) + ", smallest: " +
          str(roundness.smallest) + ", biggest: " + str(roundness.biggest))


