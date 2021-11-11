"""Set pipeline parameters and manage your paths"""
# Import standard packages
import os

# Import project modules
import utility


PATHS = {
    # NOTE: Set this path to your main project directory
    #"project_path": r"E:\Uni\IGD\react-flask-medErkennung\backend",
    "project_path": r"C:\react-flask-medErkennung\backend",
}

# Create and set paths all I/O paths
project_path = PATHS["project_path"]
io_path = utility.create_path(os.path.join(project_path, "data", "io"))
io_raw_box_path = utility.create_path(os.path.join(io_path, "raw", "box"))
io_raw_med_path = utility.create_path(os.path.join(io_path, "raw", "med"))
io_preprocessed_box_path = utility.create_path(os.path.join(io_path, "preprocessed", "box"))
io_preprocessed_med_path = utility.create_path(os.path.join(io_path, "preprocessed", "med"))
io_files_box_path = utility.create_path(os.path.join(io_path, "files", "box"))
io_files_med_path = utility.create_path(os.path.join(io_path, "files", "med"))
io_result_path = utility.create_path(os.path.join(io_path, "result"))
in_path = utility.create_path(os.path.join(io_path, "in"))
in_box_path = utility.create_path(os.path.join(in_path, "box"))
in_med_path = utility.create_path(os.path.join(in_path, "med"))
in_test_path = utility.create_path(os.path.join(in_path, "test"))
out_path = utility.create_path(os.path.join(io_path, "result"))
out_box_path = utility.create_path(os.path.join(out_path, "box"))
out_med_path = utility.create_path(os.path.join(out_path, "med"))

PATHS["io_path"] = io_path
PATHS["io_raw_box_path"] = io_raw_box_path
PATHS["io_raw_med_path"] = io_raw_med_path
PATHS["io_preprocessed_box_path"] = io_preprocessed_box_path
PATHS["io_preprocessed_med_path"] = io_preprocessed_med_path
PATHS["io_files_box_path"] = io_files_box_path
PATHS["io_files_med_path"] = io_files_med_path
PATHS["in_path"] = in_path
PATHS["in_box_path"] = in_box_path
PATHS["in_med_path"] = in_med_path
PATHS["in_test_path"] = in_test_path
PATHS["io_result_path"] = io_result_path
PATHS["io_result_box_path"] = out_box_path
PATHS["io_result_med_path"] = out_med_path


# Parameters used across the pipeline
PARAMS = {
    "mode": "test",  # Set pipeline mode; "train" or "test"
    # These params are used for center cropping
    "translation_x": -100,
    "translation_y": 100,
    "crop_width": 0.65,
    "crop_height": 0.4,
}


# Original colors of the supervisely bounding boxes
# class: (B, G , R) NOTE: Yes it's BGR, cv2 uses this color coding.
CLASS_COLORS = {
    0: (155, 155, 155),
    1: (88, 161, 246),
    2: (35, 166, 245),
    3: (28, 231, 248),
    4: (27, 2, 208),
    5: (226, 144, 74),
    6: (224, 16, 189),
    7: (73, 119, 173),
    8: (79, 212, 58),
    9: (11, 39, 71),
    10: (194, 227, 80),
    11: (0, 0, 0),
    12: (5, 117, 41),
    13: (254, 19, 144),
    14: (33, 211, 126),
}


# Original class names and their according number
# Box and meds are handed separately that's why there are two 0 classes.
CLASS_NAMES = {
    "box": 0,
    "weichkapsel_transparent": 0,
    "weichkapsel_braun": 1,
    "kapsel_weiss_gelb_orange": 2,
    "kapsel_weiss_gelb": 3,
    "kapsel_weiss": 4,
    "dragee_blau": 5,
    "dragee_pink": 6,
    "tablette_beige_oval": 7,
    "tablette_weiss_oval": 8,
    "tablette_braun_rund": 9,
    "tablette_blau_rund": 10,
    "tablette_weiss_zink": 11,
    "tablette_weiss_10mm": 12,
    "tablette_weiss_8mm": 13,
    "tablette_weiss_7mm": 14,
}
