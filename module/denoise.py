import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from math import log


class Denoise:
    def __init__(self, path_in: str):
        self._path_out = "denoise"
        self.path_in = path_in

    def local_maximum(self, spec, window_size, threshold):
        w, h = spec.shape
        global_max = np.max(spec)
        max_pos = []
        w_loop_times = int(w / window_size)
        h_loop_times = int(h / window_size)

        for i in range(w_loop_times):
            for j in range(h_loop_times):
                window = spec[
                    window_size * i : window_size * (i + 1),
                    window_size * j : window_size * (j + 1),
                ]
                local_max = np.max(window)
                if local_max < global_max and local_max > (global_max * threshold):
                    ind = np.unravel_index(np.argmax(window, axis=None), window.shape)
                    max_pos.append((5 * i + ind[0], 5 * j + ind[1]))

        return max_pos

    def create_path_out(self):
        if not os.path.exists(self._path_out):
            os.mkdir(self._path_out)

    def get_correct_gamma(self):
        # Reading input image
        img = cv2.imread(self.path_in)

        # Filter noise and convert to gray image
        median = cv2.medianBlur(img, 5)
        gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)

        # Using gamma correction
        gamma = log(img.mean()) / log(128)
        return np.array(255 * (gray / 255) ** gamma, dtype="uint8")

    def shift_dft(self, dft):
        # apply shift of origin from upper left corner to center of image
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(
            cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
        )

        max_pos = self.local_maximum(magnitude_spectrum, 5, 0.9)
        for pos in max_pos:
            dft_shift[pos] = 0

        # shift origin from center to upper left corner
        return np.fft.ifftshift(dft_shift)

    def denoise(self):
        # Init path
        self.create_path_out()
        name_list = self.path_in.split("/")
        path_out_png = (
            "/media/Z/TrungNT108/ComputerVision_HUST/processed_image"
            + "/"
            + name_list[-1]
        )

        # convert image to floats and do dft saving as complex output
        corrected_gamma = self.get_correct_gamma()
        dft = cv2.dft(np.float32(corrected_gamma), flags=cv2.DFT_COMPLEX_OUTPUT)
        back_ishift = self.shift_dft(dft)

        # do idft saving as complex output
        img_back = cv2.idft(back_ishift)

        # combine complex components into original image again
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
        img_back[:, -1] = img_back[:, -2]
        img_back[-1, :] = img_back[-2, :]

        plt.imsave(path_out_png, img_back, cmap="gray")

        return path_out_png
