import os
import numpy as np
import cv2
import datetime


class Counting:
    def __init__(self, path_in, opening_sign):
        self._path_out = "/media/Z/TrungNT108/ComputerVision_HUST/processed_image"
        self.path_in = path_in
        self.opening_sign = opening_sign

    def create_path_out(self):
        if not os.path.exists(self._path_out):
            os.mkdir(self._path_out)

    def apply_adaptive_threshold(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Using thresh_adaptive = 180, kernel_size = 27, C = -10
        adaptive_threshold = cv2.adaptiveThreshold(
            gray,
            180,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            27,
            -10,
        )
        return adaptive_threshold

    def apply_opening(self, img):
        if self.opening_sign == "0":
            kernel_size = (3, 3)
        else:
            kernel_size = (7, 9)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        opening_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening_img

    def save_img(self, img):
        # Saving
        name_list = self.path_in.split("/")
        path_out_png = (
            self._path_out
            + "/"
            + str(datetime.datetime.now().timestamp())
            + name_list[-1]
        )
        cv2.imwrite(path_out_png, img)
        return path_out_png

    def extract_contour_from_img(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        threshold = 0
        extracted_contours = []

        for item in contours:
            area = cv2.contourArea(item)
            if threshold < area:
                extracted_contours.append(item)

        return extracted_contours

    def process(self):
        img = cv2.imread(self.path_in)
        # Apply adaptive thresholding
        adaptive_img = self.apply_adaptive_threshold(img)
        # Apply opening operation
        opening_img = self.apply_opening(adaptive_img)
        # Getting contours
        extracted_contours = self.extract_contour_from_img(opening_img)
        # Save
        path_adaptive = self.save_img(adaptive_img)
        path_opening = self.save_img(opening_img)
        return (path_adaptive, path_opening, extracted_contours)

    def counting_object(self):
        # Create destination folder
        self.create_path_out()

        path_adaptive, path_opening, extracted_contours = self.process()

        # Visualize bounding box and contours
        for item in extracted_contours:
            # Rectangle
            x, y, w, h = cv2.boundingRect(item)
            rect = cv2.minAreaRect(item)
            area_contour = cv2.contourArea(item)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            area_rec = cv2.contourArea(box)

            if 10 > area_contour / area_rec:
                # Large rectangle
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Bounding contour
                img = cv2.drawContours(img, [item], 0, (255, 0, 0), 2)

                # Small rectangle
                img = cv2.drawContours(img, [box], 0, (0, 255, 255), 2)

        return {
            "denoise_image": self.path_in,
            "path_adaptive": path_adaptive,
            "path_opening": path_opening,
            "output_image": self.saving(img),
            "total_contours": len(extracted_contours),
        }
