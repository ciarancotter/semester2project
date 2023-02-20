from multiprocessing import Process
from kinect import MovementHandler
from main import main

def run_kinect():
    # code to run script1
    mv = MovementHandler(100, 100)
    while True:
        mv.update()


def run_game():
    # code to run script2
    main()

if __name__ == '__main__':
    p1 = Process(target=run_kinect)
    p2 = Process(target=run_game)
    p1.start()
    p2.start()