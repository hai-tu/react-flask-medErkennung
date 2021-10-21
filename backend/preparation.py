"""This module is used to prepare given raw supervisely data for later use.
Mainly for converting the .json labels into another format
and moving/renaming the data.
"""
# Import standard packages
import os
import shutil
import json

# Import third party packages
import cv2


def prepare_label(data, src_path, dest_path=None, format="yolo"):
    """Preparation of the labels by converting them to an other format
    and moving them to the same folder. Set the "raw""label" fields in data.

    Args:
        data (dict): The datastructure used throughout the pipeline.
        src_path (string): Path to the raw data set, containing .json
            files as labels. Assumes the supervisely format.
        dest_path (string): If set save the labels to this path.
            Defaults to None.
        format (string): The resulting label format.
            Choose between "json", "up_left" and "yolo".
            Defaults to "yolo".

    Returns:
        dict: The datastructure used throughout the pipeline.
            Now the "raw""label" fields are set.
            See init_datastructure for precise structure format.
    """
    for dirpath, dirnames, filenames in os.walk(src_path):
        for filename in [f for f in filenames if f.endswith(".json")]:
            src_file_path = os.path.join(dirpath, filename)
            # Rename files from .jpg.json to .json
            if filename.endswith("jpg.json"):
                filename = filename[:-9]

            if format == "json":
                if dest_path:
                    dest_file_path = os.path.join(
                        dest_path, filename + ".json"
                    )
                    shutil.copyfile(src_file_path, dest_file_path)
                else:
                    print("With format=json and out=False, prepare method does nothing!")
                    break
                continue
            else:
                with open(src_file_path) as json_file:
                    json_data = json.load(json_file)
                    new_label = convert_labels(json_data, format)
                if dest_path:
                    # Create new .txt file and write down output string
                    dest_file_path = os.path.join(dest_path, filename + ".txt")
                    with open(dest_file_path, "w") as out_txt:
                        out_txt.write(new_label)
            # Save label in data
            data[filename]["raw"]["label"] = new_label
    return data


def prepare_images(data, src_path, dest_path=None):
    """Prepare image by moving them to the same destination folder
    and set the "raw""image" fields in data.

    Args:
        data (dict): The datastructure used throughout the pipeline.
        src_path (string): Path to the raw data set, containing .jpg images.
        dest_path (string): If set save the images to this path.
            Defaults to None.

    Returns:
        dict: The datastructure used throughout the pipeline.
            Now the "raw""image" fields are set.
            See init_datastructure for precise structure format.
    """
    for dirpath, dirnames, filenames in os.walk(src_path):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            # Save img to data
            src_file_path = os.path.join(dirpath, filename)
            data[filename[:-4]]["raw"]["image"] = cv2.imread(src_file_path)
            # Optional image output
            if dest_path:
                dest_file_path = os.path.join(dest_path, filename)
                shutil.copyfile(src_file_path, dest_file_path)
    return data


def convert_labels(json_data, format):
    """ Convert the original .json labels to a different .txt format

    Args:
        json_data (dict): A label in .json format.
            Assumes the supervisely format.
        format (string): The resulting label format.
            Choose between "up_left" and "yolo".
            Defaults to "yolo".

    Returns:
        string: Label in given format.
    """
    output_string = ""

    img_h = json_data["size"]["height"]
    img_w = json_data["size"]["width"]

    # walk through all objects, get relevant data
    for obj in json_data["objects"]:
        class_label = obj["classTitle"]
        class_label = str(int(class_label[:2]))
        x1 = obj["points"]["exterior"][0][0]
        y1 = obj["points"]["exterior"][0][1]
        x2 = obj["points"]["exterior"][1][0]
        y2 = obj["points"]["exterior"][1][1]

        w = x2 - x1
        h = y2 - y1

        # Format: x1 y1 width height class_label
        # x1,y1 are coords of upper left BB edge
        # Values as int in pixel position
        if format == "up_left":
            output_string += (
                str(x1)
                + " "
                + str(y1)
                + " "
                + str(w)
                + " "
                + str(h)
                + " "
                + class_label
                + "\n"
            )

        # Format: class_label x_center y_center width height
        # Values in float relative to image width & height
        elif format == "yolo":
            x_center_rel = (x1 + 0.5 * w) / img_w
            y_center_rel = (y1 + 0.5 * h) / img_h
            w_rel = w / img_w
            h_rel = h / img_h

            output_string += (
                class_label
                + " "
                + str(x_center_rel)
                + " "
                + str(y_center_rel)
                + " "
                + str(w_rel)
                + " "
                + str(h_rel)
                + "\n"
            )

    return output_string


"""Below is legacy code, it was used to randomly split the data into train/test
We don't need it since we have designated train and test sets"""
# # Random split data
# # Create train.txt and test.txt
# def random_split(path):

#     # if not pre-splitted, split at random
#     train_split = 0.8
#     path_json = os.path.join(path, "Images")

#     # get paths to imgs, shuffle and random split
#     imgs = np.array(os.listdir(path_json))
#     np.random.shuffle(imgs)
#     train_imgs = imgs[0 : int(train_split * imgs.shape[0])]
#     test_imgs = imgs[int(train_split * imgs.shape[0]) : -1]

#     format_and_write_split_string(train_imgs, os.path.join(path, "train.txt"))
#     format_and_write_split_string(test_imgs, os.path.join(path, "test.txt"))


# # Format the strings so theres a single relative path to an image in every line
# # Write/save string to .txt file
# def format_and_write_split_string(arr, path):
#     out_string = ""
#     for a in arr:
#         out_string += "data/obj/" + a + "\n"

#     with open(path, "w") as out_txt:
#         out_txt.write(out_string)
