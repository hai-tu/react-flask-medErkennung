"""This is the main method, where every step of the pipeline is controlled.
There are two different modes train and test. Train generates files
and input data used for training with YOLO. Test runs input images through
the whole pipeline, resulting in prediction labels.
"""
# Import standard packages
import shutil
import os
import timeit
from typing import Tuple
import os

# Import third party packages
import numpy as np
from utils.camera_calibration import undistort_image
import cv2

# Import project modules
from params import PARAMS, PATHS
import preparation
import utility
import processing
import visualization
import integration


# Get pipeline parameters
t_x = PARAMS["translation_x"]
t_y = PARAMS["translation_y"]
crop_width = PARAMS["crop_width"]
crop_height = PARAMS["crop_height"]


def init_datastructure(src_path, type="box"):
    """Initialize the data structure used throughout the pipeline.
    The dictionary keys are initialized as filenames of all ".jpg"
    in the given path. All other files are initialized empty.

    Args:
        src_path (string): Path to a directory containing .jpg images
        to list as keys in the datastructure.
        type (str, optional): There a to types "med" and "box". "Med" needs
        a list in the "processed" fields, since there are 5 different images
        and labels. Defaults to "box".

    Returns:
        dict: An empty dict with keys set as file names.
        The precise format is shown below.
        Data_Box = {
            "name": {
                "raw": {
                    "image": raw_img,
                    "label": raw_label
                },
                "processed": {
                    "image": proc_img,
                    "label": proc_label
                }
            }
        }
        Data_Med = {
            "name": {
                "raw": {
                    "image": raw_img,
                    "label": raw_label
                },
                "processed": {
                    "image": [proc_img0, proc_img1, ..., proc_img4],
                    "label": [proc_label0, proc_label1, ..., proc_label4]
                }
            }
        }
    """
    data = {}
    if type != "box" and type != "med":
        print(
            "The type ",
            type,
            ' should not be used for initialization. \
            Please use "box" or "med".',
        )
    for dirpath, dirnames, filenames in os.walk(src_path):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            name = filename.split(".")[0]
            data[name] = {}
            data[name]["raw"] = {}
            data[name]["processed"] = {}
            # Med needs a multiple (5) entries for processed images and labels
            if type == "med":
                data[name]["processed"]["image"] = list()
                data[name]["processed"]["label"] = list()
    return data


def prepare_data(
    data, src_path, dest_data_path=None, dest_list_path=None, format="yolo"
):
    """Load images and labels. Transform label format. Optionally places
        all label and images in single directory and generate 'train.txt'
        and 'test.txt'. Assumes there's a 'train'  and a 'test' folder
        containing the images (.jpg) with labels (.json) in src_path.
        Attention: The pipeline works only with yolo formatted labels.

    Args:
        data (dict): The datastructure used throughout the pipeline.
            See init_datastructure for precise structure format.
        src_path (string): Path to raw input data. Should contain
            a 'train' and a 'test' folder.
        dest_data_path (string): If set save the prepared/raw images and labels
            to this path. Defaults to None.
        dest_list_path (string): If set save 'train.txt' and 'test.txt'
            to this path. Defaults to None.
        format (str, optional): The new format the labels
             are transformed to. Defaults to "yolo".
    Returns:
        dict: The datastructure used throughout the pipeline.
            Now the "raw" fields are set.
            See init_datastructure for precise structure format.
    """
    train_src_path = os.path.join(src_path, "train")
    test_src_path = os.path.join(src_path, "test")

    # Prepare and list train data
    data = preparation.prepare_label(
        data, train_src_path, dest_data_path, format
    )
    data = preparation.prepare_images(data, train_src_path, dest_data_path)
    if dest_list_path:
        utility.list_paths(
            dest_data_path, os.path.join(dest_list_path, "train.txt")
        )

    # Prepare and list test data
    if not dest_list_path:
        data = preparation.prepare_label(data, test_src_path, format=format)
        data = preparation.prepare_images(data, test_src_path)
    elif dest_list_path:
        # Move all data to a temporary folder first,
        # so the path listing can be created.
        temp_path = utility.create_path(dest_data_path, "temp")
        data = preparation.prepare_label(
            data, test_src_path, temp_path, format
        )
        data = preparation.prepare_images(data, test_src_path, temp_path)
        utility.list_paths(temp_path, os.path.join(dest_list_path, "test.txt"))
        # Move data to dest folder.
        for f in os.listdir(temp_path):
            dest = os.path.join(dest_data_path, f)
            if not os.path.exists(dest):
                os.rename(os.path.join(temp_path, f), dest)
        shutil.rmtree(temp_path)

    return data


def preprocess_box(data, dest_path=None, visualize=False):
    """Translate and center crop image. Does the same
        to the according label if in train mode.

    Args:
        data (dict): The datastructure used throughout the pipeline.
            See init_datastructure for precise structure format.
        dest_path (string): If set save the preprocessed images and labels
            to this path. Defaults to None.
        visualize (bool, optional): If True save processed images
            with their labels displayed as bounding boxes. Defaults to False.

    Returns:
        dict: The datastructure used throughout the pipeline.
            Now the "process" fields are set.
            See init_datastructure for precise structure format.
    """
    for name, data_case in data.items():
        img = data_case["raw"]["image"]
        # Save height and width of image before processing for later use
        old_height = img.shape[0]
        old_width = img.shape[1]
        # Translate and center crop image
        #img, roi = undistort_image(img)
        img = processing.translate_image(img, t_x, t_y)
        processed_img = processing.center_crop_image(
            img, crop_width, crop_height
        )
        data_case["processed"]["image"] = processed_img

        if dest_path:
            # Set path and save image
            img_dest_path = os.path.join(dest_path, name + ".jpg")
            cv2.imwrite(img_dest_path, processed_img)

        if PARAMS["mode"] == "train":
            # Load old label and calculate new one
            label = data_case["raw"]["label"]
            processed_label = processing.center_crop_label(
                label, [old_height, old_width]
            )
            data_case["processed"]["label"] = processed_label

            if dest_path:
                # Set path and save new label
                lbl_dest_path = os.path.join(dest_path, name + ".txt")
                lbl = open(lbl_dest_path, "w")
                lbl.write(processed_label)
                lbl.close()

        if visualize:
            # Draw resulting image and according labels and bounding boxes
            vis_dest_path = utility.create_path(dest_path, "visualization")
            visualization.draw_BB(
                name, processed_img, processed_label, vis_dest_path
            )

    return data


def preprocess_meds(data_box, data_med, dest_path=False, visualize=False):
    """Crop images according to the bounding boxes in preprocessed data_box.
    Recalculates the labels accordingly if in train mode. Resulting in 5
    cropped images/labels per original input image/label.

    Args:
        data_box (dict): The datastructure containing preprocessed boxes.
            See init_datastructure for precise structure format.
        data_med (dict): The datastructure containing raw images.
            See init_datastructure for precise structure format.
        dest_path (string): If set save the preprocessed images and labels
            to this path. Defaults to None.
        visualize (bool, optional): If True save processed images
            with their labels displayed as bounding boxes. Defaults to False.

    Returns:
        dict: The datastructure used throughout the pipeline.
            Now the "process" fields are set.
            See init_datastructure for precise structure format.
    """
    for name, data_box_case in data_box.items():
        img = data_box_case["processed"]["image"]
        label_box = data_box_case["processed"]["label"]

        if PARAMS["mode"] == "train":
            # Center crop med labels
            label_med = data_med[name]["raw"]["label"]
            label_med_new = processing.center_crop_label(
                label_med,
                [
                    data_box_case["raw"]["image"].shape[0],
                    data_box_case["raw"]["image"].shape[1],
                ],
            )

        for box_num, box_line in enumerate(label_box.split("\n")):
            if box_line:
                (
                    class_lbl,
                    x_center,
                    y_center,
                    width,
                    height,
                ) = utility.read_yolo_lbl(box_line, img.shape[0], img.shape[1])
                
                # Bbox crop image
                h2 = int(height / 2)
                w2 = int(width / 2)
                tl_x = max(
                    0, x_center - w2
                )  # Top left x coordinate # NOTE: Fix for rounding errors
                br_x = x_center + w2  # Bottom right x coordinate
                tl_y = y_center - h2  # Top left y coordinate
                br_y = y_center + h2  # Bottom right y coordinate
                img_crop = img[tl_y:br_y, tl_x:br_x]
                data_med[name]["processed"]["image"].append(img_crop)

                if PARAMS["mode"] == "train":
                    lbl_meds_box = ""  # Label of meds in a single box
                    for meds_line in label_med_new.split("\n"):
                        if meds_line:
                            (
                                med_class_lbl,
                                med_x_center_old,
                                med_y_center_old,
                                med_width_old,
                                med_height_old,
                            ) = utility.read_yolo_lbl(
                                meds_line, img.shape[0], img.shape[1]
                            )

                            # check if center point of med label lies between
                            # the box points top left and bottom right
                            if (
                                med_x_center_old > tl_x
                                and med_x_center_old < br_x
                                and med_y_center_old > tl_y
                                and med_y_center_old < br_y
                            ):
                                med_x_center = (
                                    med_x_center_old - tl_x
                                ) / width
                                med_y_center = (
                                    med_y_center_old - tl_y
                                ) / height
                                med_width = med_width_old / width
                                med_height = med_height_old / height
                                lbl_meds_box = (
                                    lbl_meds_box
                                    + str(med_class_lbl)
                                    + " "
                                    + str(med_x_center)
                                    + " "
                                    + str(med_y_center)
                                    + " "
                                    + str(med_width)
                                    + " "
                                    + str(med_height)
                                    + "\n"
                                )
                                data_med[name]["processed"]["label"].append(
                                    lbl_meds_box
                                )

                if dest_path:
                    # Save box cropped image
                    img_dest_path = os.path.join(
                        dest_path, name + "_box" + str(box_num) + ".jpg"
                    )
                    cv2.imwrite(img_dest_path, img_crop)

                if PARAMS["mode"] == "train" and dest_path:
                    # save med labels for box cropped image
                    lbl_dest_path = os.path.join(
                        #dest_path, name[:-4] + "_box" + str(box_num) + ".txt"
                        dest_path, name + "_box" + str(box_num) + ".txt"
                    )
                    lbl = open(lbl_dest_path, "w")
                    lbl.write(lbl_meds_box)
                    lbl.close()

                    vis_dest_path = utility.create_path(dest_path, "visualize")
                    if visualize:
                        visualization.draw_BB(
                            name,
                            img_crop,
                            lbl_meds_box,
                            vis_dest_path,
                            postfix="_box" + str(box_num),
                        )
    return data_med


def visualize_result(data_box, data_med, dest_path=None):
    """Visualize the pipeline result after recalculating the 5 resulting
    labels into a single label in the original image dimensions.

    Args:
        data_box (dict): The datastructure containing box detection results.
            See init_datastructure for precise structure format.
        data_med (dict): The datastructure containing med detection results.
            See init_datastructure for precise structure format.
        dest_path (string): If set save the resulting images and labels
            to this path. Defaults to None.
    """
    for name, data_case in data_box.items():
        # Load and split box label for separate access later on
        box_labels = data_case["processed"]["label"].split("\n")

        # Load every single corresponding med label
        med_labels = ""
        for i in range(0, 4):
            med_label = data_med[name]["processed"]["label"][i]
            box_label = box_labels[i]  # Get Box corresponding to meds label
            med_labels += processing.back_calculation_labels(
                med_labels=med_label, box_label=box_label
            )

        if dest_path:
            # save med labels for box cropped image
            lbl_dest_path = os.path.join(dest_path, name + ".txt")
            lbl = open(lbl_dest_path, "w")
            lbl.write(med_labels)
            lbl.close()

            visualization.draw_BB(
                name, data_case["raw"]["image"], med_labels, dest_path
            )


def postprocess():
    """TODO: Implement for better results."""
    pass


def preparation_yolo_training():
    """Runs through the preparation for YOLO training by processing and
    saving needed input files and data (images, labels).
    """
    # Preparation step1 - box
    data_box = init_datastructure(src_path=PATHS["in_box_path"], type="box")
    data_box = prepare_data(
        data=data_box,
        src_path=PATHS["in_box_path"],
        dest_data_path=PATHS["io_raw_box_path"],
        dest_list_path=PATHS["io_files_box_path"],
    )
    data_box = preprocess_box(
        data=data_box,
        dest_path=PATHS["io_preprocessed_box_path"],
        visualize=True,
    )

    # Preparation step2 - med
    data_med = init_datastructure(src_path=PATHS["in_med_path"], type="med")
    prepare_data(
        data=data_med,
        src_path=PATHS["in_med_path"],
        dest_data_path=PATHS["io_raw_med_path"],
        dest_list_path=PATHS["io_files_med_path"],
    )
    data_med = preprocess_meds(
        data_box=data_box,
        data_med=data_med,
        dest_path=PATHS["io_preprocessed_med_path"],
        visualize=True,
    )


def run_pipeline_live(out=True):
    """Runs through the whole pipeline in test mode.
    First process the box data to input and detect using YOLO,
    resulting in a single label for all boxes per image.
    Second  process the med data to input and detect using YOLO,
    resulting in five labels per image.
    Third recalculate the med labels to a single label
    and in original image dimensions. Save and visualize final result.
    """
    # Stage 1
    data_box = init_datastructure(src_path=PATHS["in_test_path"], type="box")
    data_box = preparation.prepare_images(
        data=data_box, src_path=PATHS["in_test_path"]
    )
    data_box = preprocess_box(data=data_box)
    for name, data_case in data_box.items():
        label = integration.detect_image(
            image=data_case["processed"]["image"], network_type="box"
        )
        #print("label is", label.split("\n"))
        label_list = label.split("\n")
        label_list = label_list[:-1]
        label_list.sort(key=lambda x:float(x.split()[1]))
        label_list.append("\n")
        label = "\n".join(label_list)
        data_case["processed"]["label"] = label
        if out:
            out = open(
                os.path.join(PATHS["io_result_box_path"], name + ".txt"), "w"
            )
            out.write(label)
            out.close()
            visualization.draw_BB(
                name,
                data_case["processed"]["image"],
                label,
                PATHS["io_result_box_path"],
            )
    # fileName = ""
    # for name, data_case in data_box.items():
    #     fileName = os.path.join(PATHS["io_result_box_path"], name + ".txt")
    # with open(fileName, "r+") as f:
    #     lines = f.readlines()
    # lines.sort(key=lambda x:float(x.split()[1]))
    # with open(fileName, "w") as f:
    #     for line in lines:
    #         f.write(line)


    # Stage 2
    data_med = init_datastructure(src_path=PATHS["in_test_path"], type="med")
    data_med = preprocess_meds(data_box=data_box, data_med=data_med)
    for name, data_case in data_med.items():
        for i in range(0, 4):
            label = integration.detect_image(
                image=data_case["processed"]["image"][i], network_type="med"
            )
            if out:
                out = open(
                    os.path.join(
                        PATHS["io_result_med_path"], name + str(i) + ".txt"
                    ),
                    "w",
                )
                out.write(label)
                out.close()
                visualization.draw_BB(
                    name,
                    data_case["processed"]["image"][i],
                    label,
                    PATHS["io_result_med_path"],
                )
            data_case["processed"]["label"].append(label)

    # Postprocessing and visualization
    postprocess()
    visualize_result(
        data_box=data_box, data_med=data_med, dest_path=PATHS["io_result_path"]
    )


def main():
    """Starts train or test mode"""
    if PARAMS["mode"] == "train":
        preparation_yolo_training()
    else:
        run_pipeline_live()


if __name__ == "__main__":  # Stops code from running main method unexpectedly
    main()
