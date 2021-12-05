
import cv2
import numpy as np

class TestScreen:
    def __init__(self, size):
        self.size = size
        cv2.startWindowThread()
        cv2.namedWindow("preview")
        
    def SetImage(self, img):
        cv2.imshow('preview', np.array(img)[:, :, ::-1].copy())
        return

    def Clear(self):
        #self.matrix.fill((0,0,0))
        return