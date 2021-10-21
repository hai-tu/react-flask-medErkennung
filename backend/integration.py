"""This module integrates YOLO to detect given images"""
# Import third party packages
import cv2

# Import project modules
from network import darknet
from params import CLASS_NAMES


def detect_image(image, network_type):
    """Load custom files to create YOLO network and then run detection on it.

    Args:
        image (numpy.ndarray): The image to detect.
            It's a 3D array (2D image with RBG colors) containing integers.
        network_type (string): Use "box" or "med" to load
            the corresponding custom files. It's just to find the right paths.

    Returns:
        string: The resulting label in YOLO format with appended probabilities
    """
    if network_type == "box":
        network, classes, colors = darknet.load_network(
            "network/box/box.cfg",
            "network/box/box.data",
            "network/box/box.weights",
        )
    elif network_type == "med":
        network, classes, colors = darknet.load_network(
            "network/med/med.cfg",
            "network/med/med.data",
            "network/med/med.weights",
        )
    else:
        print(
            "The networky type ",
            network_type,
            ' doesn\'t exist. Choose "box" or "med".',
        )

    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(
        image_rgb, (width, height), interpolation=cv2.INTER_LINEAR
    )
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    darknet_out = darknet.detect_image(network, classes, darknet_image)
    darknet.free_image(darknet_image)

    return transform_to_label(darknet_out, scale=[width, height])


def transform_to_label(darknet_out, scale):
    """Transforms the darknet output format in YOLO label format
    with appended probabilities per line.

    Args:
        darknet_out ([type]): The original YOLO network output.
        scale ([int, int]): The width and height of the YOLO network,
        which is used to rescale the labels.

    Returns:
        string: Formatted label in YOLO format with appended probabilities
    """
    label = ""
    for det in darknet_out:
        lbl = det[0]
        probability = det[1]
        width = det[2][2] / scale[0]
        height = det[2][3] / scale[1]
        x_center = det[2][0] / scale[0]
        y_center = det[2][1] / scale[1]

        label += (
            str(CLASS_NAMES[lbl])
            + " "
            + str(x_center)
            + " "
            + str(y_center)
            + " "
            + str(width)
            + " "
            + str(height)
            + " "
            + str(probability)
            + " "
            + "\n"
        )
    return label
