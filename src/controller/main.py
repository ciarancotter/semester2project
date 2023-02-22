from multiprocessing import Process
from game import main

def run_kinect():
    try:
        from kinect import MovementHandler
        mv = MovementHandler(1280, 784)
        while True:
            mv.update()
    except:
        return

def run_game():
    main()

if __name__ == '__main__':
    p1 = Process(target=run_kinect)
    p2 = Process(target=run_game)
    p1.start()
    p2.start()
