import os
import cv2
import numpy as np
import glob

class DataLoader:
    def __init__(self, path):
        self.path = path
        self.dir_name = os.path.basename(path)
        self.height = 480
        self.width = 640
        self.channels = 3

    def load_folder(self):
        image_files = glob.glob(f"{self.path}/*.jpg")
        image_names = [os.path.basename(image) for image in image_files]
        length = np.shape(image_files)[0]
        image_array = np.zeros((length, self.height, self.width, self.channels))
        for i, image in enumerate(image_files):
            img = cv2.imread(image)
            if img is not None:
                image_array[i, :, :, :] = img
        return image_names, image_array

    def load_video(self):
        raise NotImplementedError