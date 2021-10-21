"""This module contains processing methods throughout the pipeline
This is mostly the center crop for images and labels and the
recalculation of the final 5 labels to a single label.
"""
# Import third party packages
import numpy as np
import cv2

# Import project modules
from params import PARAMS
import utility


t_x = PARAMS["translation_x"]
t_y = PARAMS["translation_y"]
crop_width = PARAMS["crop_width"]
crop_height = PARAMS["crop_height"]


def translate_image(img, t_x, t_y):
    """Translate given image by (t_x, t_y) in image coordinates.

    Args:
         image (numpy.ndarray): The image to translate.
            It's a 3D array (2D image with RBG colors) containing integers.
        t_x (int): Translation in x direction
        t_y (int): Translation in y direction

    Returns:
        numpy.ndarray: The translated image.
            It's a 3D array (2D image with RBG colors) containing integers.
    """
    T = np.float32([[1, 0, t_x], [0, 1, t_y]])
    img_trans = cv2.warpAffine(img, T, (img.shape[1], img.shape[0]))

    return img_trans


def center_crop_image(img, crop_width, crop_height):
    """Center crop a given image

    Args:
       image (numpy.ndarray): The image to center crop.
            It's a 3D array (2D image with RBG colors) containing integers.
        crop_width (float): A number in range [0,1]. Percentage of
            the resulting image width in contrast to original image width.
        crop_height (float):  A number in range [0,1]. Percentage of
            the resulting image height in contrast to original image height.

    Returns:
        numpy.ndarray: The cropped image
            It's a 3D array (2D image with RBG colors) containing integers.
    """
    img_height = img.shape[0]
    img_width = img.shape[1]

    w2 = int((crop_width * img_width) / 2)
    og_w2 = int(img_width / 2)

    h2 = int((crop_height * img_height) / 2)
    og_h2 = int(img_height / 2)
    img_crop = img[og_h2-h2:og_h2+h2, og_w2-w2:og_w2+w2]

    return img_crop


def center_crop_label(label, old_shape):
    """Iterates over all lines/labels in a given label file
    and recalculates the labels according to center or box crop

    Args:
        label (string): Old label as string which is recalculated
        old_shape ([int, int]): Shape of the original image [height, width]

    Returns:
        string: New label as string formatted for output as .txt
    """
    new_label = ""
    for label_line in label.split("\n"):
        if label_line:  # There might be an empty label line caused by "\n"
            (
                class_lbl,
                x_center_old,
                y_center_old,
                width_old,
                height_old,
            ) = utility.read_yolo_lbl(label_line, old_shape[0], old_shape[1])

            # Calc center crop
            new_height = int(old_shape[0] * crop_height)
            new_width = int(old_shape[1] * crop_width)
            x_center = (
                x_center_old + t_x - ((1 - crop_width) * old_shape[1] * 0.5)
            ) / new_width
            y_center = (
                y_center_old + t_y - ((1 - crop_height) * old_shape[0] * 0.5)
            ) / new_height
            width = width_old / new_width
            height = height_old / new_height

            new_label = (
                new_label
                + str(class_lbl)
                + " "
                + str(x_center)
                + " "
                + str(y_center)
                + " "
                + str(width)
                + " "
                + str(height)
                + "\n"
            )
    return new_label


def back_calculation_labels(med_labels, box_label):
    """Calculate back the labels in box cropped space to
    original space by moving according to the translations used in
    center crop and box crop. Also scale according to original image size.

    Args:
        med_labels (string): The label to calculate back to original space
        box_label (string):  The corresping box label, which was used for
            box cropping

    Returns:
        string: The recalculated label.
    """
    # FIXME: magic numbers
    height_og = 1080
    width_og = 1920
    height_cropped = height_og * PARAMS["crop_height"]
    width_cropped = width_og * PARAMS["crop_width"]

    # Get box label information
    (class_lbl_box,
        x_center_box,
        y_center_box,
        width_box,
        height_box,
        probability,
     ) = utility.read_yolo_lbl(
        box_label, height_cropped, width_cropped, probability=True
    )
    h2_box = int(height_box / 2)
    w2_box = int(width_box / 2)
    # NOTE: fix for rounding errors
    tl_x_box = max(0, x_center_box - w2_box)  # Top left x coordinate
    tl_y_box = y_center_box - h2_box  # Top left y coordinate

    lbl_meds_box = ""
    for med_label in med_labels.split("\n"):
        if med_label:
            # Get med label information
            (
                class_lbl_med,
                x_center_med,
                y_center_med,
                width_med,
                height_med,
            ) = utility.read_yolo_lbl(med_label, height_box, width_box)

            # Calculate new label information
            x_center_med = (
                x_center_med
                + tl_x_box
                - PARAMS["translation_x"]
                + ((1 - PARAMS["crop_width"]) * width_og * 0.5)
            ) / width_og
            y_center_med = (
                y_center_med
                + tl_y_box
                - PARAMS["translation_y"]
                + ((1 - PARAMS["crop_height"]) * height_og * 0.5)
            ) / height_og
            width_med = width_med / width_og
            height_med = height_med / height_og

            # Put together output string
            lbl_meds_box = (
                lbl_meds_box
                + str(class_lbl_med)
                + " "
                + str(x_center_med)
                + " "
                + str(y_center_med)
                + " "
                + str(width_med)
                + " "
                + str(height_med)
                + " "
                + str(probability)
                + " "
                + "\n"
            )
    return lbl_meds_box
