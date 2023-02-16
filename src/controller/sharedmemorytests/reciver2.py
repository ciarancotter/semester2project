from shared_memory_dict import SharedMemoryDict
from time import sleep

import sys
import os
sys.path.append(os.path.abspath("./../../"))


movementPool = SharedMemoryDict(name='config', size=1024)

if __name__ == "__main__":
    while True:
        print("select:", movementPool["select"],
            "mouse:", movementPool["mouse"],
            "jump:", movementPool["jump"],
            "leftpunch:", movementPool["leftpunch"],
            "rightpunch:", movementPool["rightpunch"],
            "leftwalk:", movementPool["leftwalk"],
            "rightwalk:", movementPool["rightwalk"],
            "turntest:", movementPool["turntest"]
        )