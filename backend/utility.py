"""Provides some utility methods"""
# Import standard packages
import os


def list_paths(src, dest, prefix="data/obj/"):
    """This scripts creates a .txt file with paths to all .jpg's
    in a given folder. It can be used to create train.txt and test.txt.

    Args:
        src ([string]): Path to folder containing the .jpg's
        dest ([string]): Path to folder to save the created text file to
        prefix ([string]): Prefix written in front of every relative path,
        Defaults to "data/obj/".
    """

    f = open(dest, "w")
    for dirpath, dirnames, filenames in os.walk(src):
        for img_name in [f for f in filenames if f.endswith(".jpg")]:
            f.write(prefix + img_name + "\n")
    f.close()


def create_path(path, *paths):
    """Fuses strings to path and creates the according folders
    if they do not exist already

    Args:
        path (string): A string as a part of a path

    Returns:
        String: The complete path
    """
    new_path = os.path.join(path, *paths)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def read_yolo_lbl(line, img_height, img_width, probability=False):
    """Takes a single line off a yolo label .txt file
    and returns every single value as pixel values (not float)

    Args:
        line (string): A single single line of yolo label
        img_height (int): The height of the corresponsing image
        img_width (int): The height of the corresponsing image
        probability (bool); The probability of the network predicting
        the right label. Defaults to False.

    Returns:
        str, int, int, int, int: Every value of the label singled out.
            Also returns the probability as float if probability=True.
    """
    label = line.split()

    class_lbl = str(int(label[0]))
    x_center = int(float(label[1]) * img_width)
    y_center = int(float(label[2]) * img_height)
    width = int(float(label[3]) * img_width)
    height = int(float(label[4]) * img_height)
    if probability:
        return class_lbl, x_center, y_center, width, height, label[5]
    return class_lbl, x_center, y_center, width, height


"""Below is some one time used legacy code"""
# ###dirty evil helper script, to change all .txt file names in a given dir
# path = r""
# postfix = "_meds"
# def change_names(path, postfix):
#     for dirpath, dirnames, filenames in os.walk(path):
#         for file in [f for f in filenames if f.endswith(".txt")]:
#             src_path = os.path.join(dirpath, file)
#             os.rename(src_path, src_path[:-4] + postfix + ".txt")
