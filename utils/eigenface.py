import cv2
import numpy as np

class EigenfaceRecognizer:
    def __init__(self):
        self.model = cv2.face.EigenFaceRecognizer_create()

    def train(self, images, labels):
        self.model.train(images, np.array(labels))

    def predict(self, image):
        label, confidence = self.model.predict(image)
        return label, confidence
