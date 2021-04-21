import cv2 as cv
from threading import Thread, Lock

import yolo_v5 as yolo   


class Detection:

    # ['Tower', 'Canon_Minion', 'caster_minion', 'Melee_Minion',  'Ezreal']

    CONF_THRESHOLD = 0.6
    IGNORE_CALSSES = [ 0.0, 4.0]

    stopped = True
    lock = None
    rectangles = []
    conf = []
    classes = []
    screenshot = None
    dtc = None

    def __init__(self):

        self.lock = Lock()
        self.dtc = yolo.detector()

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:

                img = self.dtc.detect(cv.cvtColor(self.screenshot, cv.COLOR_RGB2BGR)).pred[0]

                # Get rectangles from prediction
                rectangels = []
                conf = []
                classes = []      
                for b_box in img:
                    rect = [b_box[0].item(), b_box[1].item(), b_box[2].item(), b_box[3].item()]
                    if b_box[4] > self.CONF_THRESHOLD and  b_box[5].item() not in self.IGNORE_CALSSES:
                        rectangels.append(rect)
                        conf.append(b_box[4].item())
                        classes.append(b_box[5].item())
                
                self.lock.acquire()
                self.rectangles = rectangels
                self.conf = conf
                self.classes = classes
                self.lock.release()