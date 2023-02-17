from shared_memory_dict import SharedMemoryDict
from time import sleep
import pickle

import sys
import os
sys.path.append(os.path.abspath("./../../"))
print(sys.path)

from model.movement_recognition.HandInfront import HandInfront

smd_config = SharedMemoryDict(name='config', size=1024)

if __name__ == "__main__":

    hand = HandInfront()
    print(len((pickle.dumps(hand))))

    #smd_config["status"] = True
    smd_config["hand"] = hand

    while True:
        #smd_config["status"] = not smd_config["status"]
        sleep(0.1)