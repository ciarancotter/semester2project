from shared_memory_dict import SharedMemoryDict
from time import sleep

import sys
import os
sys.path.append(os.path.abspath("./../../"))


movementPoolRead = SharedMemoryDict(name='movementPoolRead', size=1024)

if __name__ == "__main__":
    sleep(0.5)
    while True:
        print("select:", movementPoolRead["select"],
            "jump:", movementPoolRead["jump"],
            "leftpunch:", movementPoolRead["leftpunch"],
            "rightpunch:", movementPoolRead["rightpunch"],
            "leftwalk:", movementPoolRead["leftwalk"],
            "rightwalk:", movementPoolRead["rightwalk"],
        )
        #print(movementPoolRead)