from threading import Thread
import time

class Engine(Thread):

    def __init__(self) -> None:
        Thread.__init__(self, daemon=True)
    
    def run(self):
        while(True):
            print("hello inside engine")
            time.sleep(10)

