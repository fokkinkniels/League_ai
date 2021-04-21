import torch
from PIL import Image


class detector:
    def __init__(self, weights=r'C:\Users\fokki\Documents\NIELS\SCHOOL\ICT S4\Challenges\Genuine Challenges\League of legends Bot\Workspace\custom_classifiers\yolo_v5\best_19_4_2021.pt'):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model=weights)
        self.model = self.model.to('cuda')
        self.model = self.model.autoshape()  # for PIL/cv2/np inputs and NMS

    def detect(self, img):
        result = self.model(img)  # includes NMS
        return result