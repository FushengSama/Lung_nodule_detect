import cv2
from ultralytics import YOLO
yolo = YOLO(r'F:\code\flaskProject\model\jj4.pt', task="detect")
import numpy as np


def getYoloResult(image):
    results = yolo(source=image)
    result = results[0]
    boxes = result.boxes
    xywh = boxes.xywh

    xywhNP = xywh.clone().detach().cpu().numpy()
    #cv2.imshow('x',result.plot())
    #cv2.waitKey(0)
    return result.plot(),xywhNP
if __name__=='__main__':
    img=cv2.imread('0008.png')
    getYoloResult(img)