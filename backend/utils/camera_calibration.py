"""
This module contains function to apply the camera calibration.
The code is based on https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html.
"""

# Import standard packages
import logging
import os.path
from typing import Tuple

# Import third party packages
import numpy as np
#from cv2 import cv2
import cv2


def undistort_image(
    image: np.ndarray,
    calibration_file: str = os.path.join(
        os.path.dirname(__file__), "camera_calibration", "calib_data.npz"
    ),
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies the camera calibration to a given raw image.
    IMPORTANT: This function does not test if the image has been
    calibrated before. Applying it twice (or multiple times) will
    result in erroneous image deformation.
    :param image: the raw image given as a np.ndarray
    :param calibration_file: option calibration file path in the
    numpy npz format.
    Check the test script in tests/manual/test_camera_calibration.py
    for more info regarding the .npz content format
    :return: a Tuple of [calibrated image as np.ndarray, region of
    interest as np.ndarray]
    """

    corrected_img: np.ndarray
    reg_of_int: np.ndarray

    try:
        with np.load(calibration_file) as data:
            matrix = data["mtx"]
            distance = data["dist"]
            height, width = image.shape[:2]
            # Obtain the new camera matrix and undistort the image
            optimal_cam_mtx, reg_of_int = cv2.getOptimalNewCameraMatrix(
                matrix, distance, (width, height), 1, (width, height)
            )
            corrected_img = cv2.undistort(
                image, matrix, distance, None, optimal_cam_mtx
            )
    except FileNotFoundError:
        logging.error("Calibration file not found!")
        return np.zeros((1080, 1920)), np.zeros((3, 3))

    except KeyError:
        logging.error(
            "The calibration file is malformed! Could not find the key 'mtx' or 'dist'."
        )
        return np.zeros((1080, 1920)), np.zeros((3, 3))

    return corrected_img, reg_of_int
