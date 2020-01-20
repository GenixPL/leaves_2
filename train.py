import os

from utils.set_trainer import SetTrainer


baseDirPath = os.path.dirname(__file__) + "/data/train/"

for i in range(1, 7):  # TODO (7)
    setDirPath = baseDirPath + "type_" + str(i)
    SetTrainer(setDirPath).train()

