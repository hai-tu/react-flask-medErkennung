"""This module is for visualization of the pipeline outputs"""
# Import standard packages
import os
import cv2

# Import project modules
from params import CLASS_COLORS
import utility


def draw_BB(name, img, label, dest_path, postfix=""):
    """Draws bounding boxes given by a label on an image and saves it
    as a .jpg.

    Args:
        name (string): Name of the image to draw.
        img (numpy.ndarray): The image to draw the BB on.
            It's a 3D array (2D image with RBG colors) containing integers.
        label (string): The label which contains the BB to draw.
        postfix (string): A postfix to append to saved files name.
            Defaults to "".
    """
    img_bb = img
    for label_line in label.split("\n"):
        if label_line:  # There might be an empty label line caused by "\n"
            (
                class_lbl,
                x_center,
                y_center,
                width,
                height,
            ) = utility.read_yolo_lbl(label_line, img.shape[0], img.shape[1])
            top_left = (x_center-int(width/2), y_center-int(height/2))
            bot_right = (x_center+int(width/2), y_center+int(height/2))
            color = CLASS_COLORS[int(class_lbl)]
            thickness = 2  # Line thickness of 2 px
            img_bb = cv2.rectangle(img, top_left, bot_right, color, thickness)

    cv2.imwrite(os.path.join(dest_path, name + postfix + ".jpg"), img_bb)
