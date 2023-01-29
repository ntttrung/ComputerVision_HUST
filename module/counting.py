import os
import numpy as np
import cv2

class Counting:
    def __init__(self, path_in, path_out, opening_sign):
        self.opening_sign = opening_sign
        self.path_in = path_in
        self.path_out = path_out

    def create_folder(self, path_out):
        if not os.path.exists(path_out):
            os.mkdir(path_out)

    def get_shape(self, img):
        height = img.shape[0]
        width = img.shape[1]
        channels = img.shape[2]

        return height, width

    def apply_adaptive_threshold(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh_adaptive = 180
        kernelSize = 25
        C = -10
        img_adapt_thresh = cv2.adaptiveThreshold(gray,thresh_adaptive,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,kernelSize, C)
        return img_adapt_thresh

    def apply_opening(self, img):
        if self.opening_sign == '0':
            kernelSize = (3, 3)
        else:
            kernelSize = (7, 9)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
        # print(kernel)
        opening_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening_img

    def extract_contour(self, img):
        extracted_contours = []
        threshold = 0
        contours, _ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for item in contours:
            area = cv2.contourArea(item)
            if area > threshold:
                extracted_contours.append(item)

        return extracted_contours

    
    def saving(self, img):
        # Saving
        name_list = self.path_in.split("/")
        name_png = name_list[-1]
        path_out_png = self.path_out + "/" + name_png
        cv2.imwrite(path_out_png, img)


    def counting_object(self):
        # Create destination folder
        self.create_folder(self.path_out)

        # Read original image
        # img = cv2.imread(self.path_in)
        # cv2.imshow("Denoise image",img)

        # h_img, w_img = self.get_shape(img)

        # # Apply adaptive thresholding
        # adaptive_img = self.apply_adaptive_threshold(img)
        # cv2.imshow("Applying adaptive thresholding",adaptive_img)

        # # Apply opening operation
        # opening_img = self.apply_opening(adaptive_img)
        # cv2.imshow("Applying opening operation",opening_img)

        # Getting contours
        extracted_contours = self.extract_contour(opening_img)

        # list = array

        # Visualize bounding box and contours
        for item in extracted_contours:
            # Rectangle
            x,y,w,h = cv2.boundingRect(item)
            rect = cv2.minAreaRect(item)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            area_rec = cv2.contourArea(box)
            area_contour = cv2.contourArea(item)
            # print(area_contour/area_rec)
            # if area_rec > 1000:
            if area_contour/area_rec < 10:

            # Large rectangle
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                
                # Bounding contour
                img = cv2.drawContours(img,[item],0,(255,0,0),2)

                # Small rectangle
                img = cv2.drawContours(img,[box],0,(0,255,255),2)

            # img_copy = adaptive_img[y:y+h,x:x+w]
            # kernelSize = (5, 5)
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
            # img_copy = cv2.morphologyEx(img_copy, cv2.MORPH_OPEN, kernel)
            # adaptive_img[y:y+h,x:x+w] = img_copy

            # area = cv2.contourArea(box)
            # print(area)

        # cv2.imshow("Applying adaptive thresholding part 2",adaptive_img)

        # Visualize text
        font = cv2.FONT_HERSHEY_SIMPLEX
        position_1 = (w_img-40, h_img-25)
        position_2 = (w_img-35, h_img-10)
        fontScale  = 0.5
        fontColor  = (0,0,255)
        thickness  = 2

        cv2.putText(img,'Total', position_1, font, fontScale, fontColor, thickness)
        cv2.putText(img,str(len(extracted_contours)), position_2, font, fontScale, fontColor, thickness)


        # Showing final result
        # cv2.imshow("Contour and Counting",img)
        
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        print("The total number of objects is: " + str(len(extracted_contours))) 

        # Saving
        self.saving(img)


# counting_test = Counting('denoise/noise_periodic.png', 'out', 1)
# counting_test = Counting('denoise/noise_pepper.png', 'out', 1)
# counting_test = Counting('denoise/noise_connected.png', 'out', 0)
# counting_test = Counting('denoise/normal.png', 'out', 1)
# counting_test.counting_object()