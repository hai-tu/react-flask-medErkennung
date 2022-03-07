from typing import Tuple

# Import third party packages
import numpy as np
import cv2 as cv
from utils.camera_calibration import undistort_image
import os

# folders = os.listdir("Hai_Latest_NewSetup")
img = cv.imread("testing.jpg")
corrected_image, roi = undistort_image(img)
# image_name = os.path.join(new_folder, "calibrated_" + file)
cv.imwrite("testing_calibrated.jpg", corrected_image)
# for folder in folders:
#     files = os.listdir(os.path.join("Hai_Latest_NewSetup", folder))
#     new_folder = "calibrated_" + folder
#     os.makedirs(new_folder)
#     for file in files:
#         image_path = os.path.join("Hai_Latest_NewSetup", folder, file)
#         #print(image_path)
#         img = cv.imread(image_path)
#         corrected_image, roi = undistort_image(img)
#         image_name = os.path.join(new_folder, "calibrated_" + file)
#         cv.imwrite(image_name, corrected_image)
# files = os.listdir("Hai_NewSetUp\Dienstag")
# for file in files:
#     image_path = os.path.join("Hai_NewSetUp\Dienstag", file)
#     #print(image_path)
#     img = cv.imread(image_path)
#     corrected_image, roi = undistort_image(img)
#     image_name = "calibrated_" + file
#     cv.imwrite(image_name, corrected_image)
# img = cv.imread('WIN_20220117_14_51_50_Pro.jpg')
# corrected_image, roi = undistort_image(img)
# cv.imwrite('calibrated.jpg', corrected_image)
