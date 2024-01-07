import cv2
import numpy as np


class Acquisition:
    """
    OpenCV VideoCapture -based acquisition
    """

    def __init__(self, roi: tuple[int, int, int, int], camera_index: int = 0):
        self.roi = roi
        self.camera = cv2.VideoCapture(camera_index)

    def set_exposure(self, exposure: float) -> bool:
        return self.camera.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def set_gain(self, gain: float) -> bool:
        return self.camera.set(cv2.CAP_PROP_GAIN, gain)

    def capture_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            return None
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def get_spectrum(self, image):
        x, y, w, h = self.roi
        roi_img = image[y : y + h, x : x + w].astype(np.float32)
        spectrum = np.sum(roi_img, axis=0)
        return spectrum

    def close(self):
        self.camera.release()
        cv2.destroyAllWindows()
