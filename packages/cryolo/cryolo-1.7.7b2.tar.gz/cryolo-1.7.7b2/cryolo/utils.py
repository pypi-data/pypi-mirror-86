"""
Abitary Utils for crYOLO
"""
#
# COPYRIGHT
#
# All contributions by Ngoc Anh Huyn:
# Copyright (c) 2017, Ngoc Anh Huyn.
# All rights reserved.
#
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#
import numpy as np
import sys

from . import imagereader
import urllib.request, json
from sklearn import mixture

class Filament:
    """
    Filament object
    """

    def __init__(self, boxes=None):
        """
        Constructor
        :param boxes: Boxes of the filament
        """

        if boxes is None:
            self.boxes = []
        else:
            self.boxes = boxes

    def add_box(self, box):
        """
        Appends a box to the filament box list.
        :param box: box to append
        :return: filament object
        """
        self.boxes.append(box)
        return self

    def get_num_boxes(self):
        """
        :return: Number of boxes that belong the filament

        """
        return len(self.boxes)

    def does_overlap(self, box, threshold):
        """
        Compares a box with all other boxes in the filament box list and calculates the IOU overlap.
        This overlap if compared to a threshold.
        :param box: Box to compare
        :param threshold: IOU Threshold
        :return: True if IOU >= threshold
        """

        for filbox in self.boxes:
            if bbox_iou(filbox, box) >= threshold:
                return True
        return False


class BoundBox:
    """
    A bounding box of a particle
    """

    def __init__(self, x, y, w, h, c=None, classes=None):
        """
        Creates a BoundBox
        :param x: x coordinate of the center
        :param y: y coordinate of the center
        :param w: width of box
        :param h: height of the box
        :param c: confidence of the box
        :param classes: Class of the BoundBox object
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.meta = {}

        self.c = c
        self.classes = classes

        self.label = -1
        self.score = -1
        self.info = None  # helping data during processing

    def get_label(self):
        """

        :return: Class with highest probability
        """
        if self.label == -1:
            self.label = np.argmax(self.classes)

        return self.label

    def get_score(self):
        """
        :return: Probability of the class
        """
        # if self.score == -1:
        self.score = self.classes[self.get_label()]

        return self.score

from enum import Enum
class CryoloMode(Enum):

    FIXED_SIZE=1
    MIXED_ASPECT_RATIO=2
    SQUARE=3
    NON_SQUARE=4


def getEquidistantBoxes(box1, box2, num_boxes):
    """
    Create multiple boxes between box1 and box2 with equdistant boxes
    :param box1: First box
    :param box2: Second box
    :param num_boxes: number of boxes
    :return: List of N=num_boxes equidistant boxes between box1 and box2
    """
    points = zip(
        np.linspace(box1.x, box2.x, num_boxes + 1, endpoint=True),
        np.linspace(box1.y, box2.y, num_boxes + 1, endpoint=True),
    )
    new_boxes = []
    if box1.c is None or box2.c is None:
        c = 1
    else:
        c = (box1.c + box2.c) / 2
    classes = ""
    if box1.classes:
        classes = box1.classes
    w = box1.w
    h = box2.w
    for point in points:
        b = BoundBox(x=point[0], y=point[1], w=w, h=h, c=c, classes=classes)
        new_boxes.append(b)
    return new_boxes


def resample_filaments(new_filaments, box_distance):
    """
    Resample a list of filaments
    :param new_filaments: List of filament
    :param box_distance: Target distance between two boxes
    :return: List of resampled filaments
    """
    resamples_filaments = [
        resample_filament(fil, box_distance) for fil in new_filaments
    ]
    resamples_filaments = [fil for fil in resamples_filaments if fil.boxes]
    return resamples_filaments


def resample_filament(filament, distance):
    """
    Resamples a filament. The new filament will have a specified distance between the boxes.
    :param filament: Target filament
    :param distance: Distance between two adjacent boxes.
    :return: Resampeld filament
    """
    # Find two boxes with maximum distance
    boxes = filament.boxes
    max_distance = 0
    max_boxa = None

    for i in range(len(boxes)):
        for j in range(len(boxes)):
            if i == j:
                continue
            dist = box_squared_distance(boxes[i], boxes[j])
            if dist > max_distance:
                max_boxa = i
    if max_boxa is not None:
        # Construct a polyline, start from max_boxa
        polyline = []
        polyline.append(boxes[max_boxa])
        assigned_boxes = []
        assigned_boxes.append(max_boxa)
        last_appended_box = boxes[max_boxa]
        last_appended_index = max_boxa
        added_new = True

        while added_new:
            min_distance = 99999999
            nearest_box_index = None
            added_new = False
            for i in range(len(boxes)):
                if i == last_appended_index:
                    continue
                if i in assigned_boxes:
                    continue

                measured_distance = box_squared_distance(last_appended_box, boxes[i])

                if measured_distance < min_distance:
                    nearest_box_index = i
                    min_distance = measured_distance

            if nearest_box_index is not None:
                polyline.append(boxes[nearest_box_index])
                assigned_boxes.append(nearest_box_index)
                last_appended_box = boxes[nearest_box_index]
                last_appended_index = nearest_box_index
                added_new = True

        # Create new boxes based on the polyline
        new_boxes_candidates = []
        sqdistance = distance * distance

        for i in range(len(polyline) - 1):
            eq_boxes = getEquidistantBoxes(polyline[i], polyline[i + 1], num_boxes=100)
            new_boxes_candidates.extend(eq_boxes)
        new_boxes = []
        dist = -1
        for box in new_boxes_candidates:
            if dist == -1:
                new_boxes.append(box)
                dist = 0
            else:
                dist = box_squared_distance(new_boxes[len(new_boxes) - 1], box)
                if dist > sqdistance:
                    new_boxes.append(box)

        new_filament = Filament()
        for box in new_boxes:
            new_filament.add_box(box)

        return new_filament
    return None

def get_cryolo_mode(size_distr, config_input_size):
    square_data_available = any([size[0] == size[1] for size in size_distr])
    non_square_data_available = any([size[0] != size[1] for size in size_distr])

    if type(config_input_size) == list:
        return CryoloMode.FIXED_SIZE

    if (square_data_available and non_square_data_available) or \
            (non_square_data_available and len(size_distr)>1):
        return CryoloMode.MIXED_ASPECT_RATIO

    if square_data_available and not non_square_data_available:
        return CryoloMode.SQUARE

    if not square_data_available and non_square_data_available and len(size_distr)==1:
        return CryoloMode.NON_SQUARE

def get_anchors(config, path_weights=None, image_sizes=None):
    '''
    Calculates the anchors.
    When fixed size mode ...
    When non-square mode...
    When square-mode ...
    When mixed-size mode

    :param config:
    :param path_weights:
    :param image_size:
    :return:
    '''
    import cryolo.config_tools as config_tools

    is_single_anchor = len(config["model"]["anchors"]) == 2
    num_patches = 1
    if "num_patches" in config["model"]:
        num_patches = config["model"]["num_patches"]

    grid_w, grid_h = config_tools.get_gridcell_dimensions(config)
    anchors = None

    if path_weights:
        import h5py

        with h5py.File(path_weights, mode="r") as f:
            try:
                anchors = list(f["anchors"])
            except KeyError:
                anchors = None

    if is_single_anchor and anchors is None:

        # if single size, use the it as given
        # if multi-size, use the average length of the short side
        #
        if len(image_sizes) == 1:
            img_width = float(image_sizes[0][1]) / num_patches
            img_height = float(image_sizes[0][0]) / num_patches
        else:
            sum_size = 0
            sum_num_images = 0
            for img_info in image_sizes:
                if img_info[0]>img_info[1]:
                    sum_size += img_info[1] * img_info[2]
                else:
                    sum_size += img_info[0] * img_info[2]
                sum_num_images += img_info[2]
            mean_size = int(sum_size/sum_num_images)
            img_width = mean_size
            img_height = mean_size

        #if image_sizes:

        #    img_width = float(image_size[0]) / num_patches
        #    img_height = float(image_size[1]) / num_patches
        #else:
        #    img_width = 4096.0 / num_patches
        #    img_height = 4096.0 / num_patches
        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        box_width, box_height = config_tools.get_box_size(config)

        anchor_width = 1.0 * box_width / cell_w
        anchor_height = 1.0 * box_height / cell_h
        anchors = [anchor_width, anchor_height]
    elif anchors is None:
        img_width = 4096.0 / num_patches
        img_height = 4096.0 / num_patches
        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        anchors = np.array(config["model"]["anchors"], dtype=float)
        anchors[::2] = anchors[::2] / cell_w
        anchors[1::2] = anchors[1::2] / cell_h

    return anchors


def box_squared_distance(boxa, boxb):
    """
    calculates the squared distance between the center of two boxes.
    :param boxa: First box
    :param boxb: Second box
    :return: Squared distance between boxa and boxb
    """
    return np.square(boxa.x - boxb.x) + np.square(boxa.y - boxb.y)

def get_normalization_func(normalization):
    if normalization == "STANDARD":
        norm_func = normalize
    elif normalization == "GMM":
        norm_func = normalize_gmm
    else:
        print("Normalization option ", normalization, "unknown. Check your config file.")
        import sys
        sys.exit(1)
    return norm_func

def normalize_gmm(image, margin_size=0):


    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]

    clf = mixture.GaussianMixture(n_components=2, covariance_type='diag')
    clf.fit(np.expand_dims(image[mask].ravel()[::15], axis=1))
    mean = None
    var = None
    if (clf.means_[1, 0]>clf.means_[0, 0]):
        mean = clf.means_[1, 0]
        var = clf.covariances_[1, 0]
    else:
        mean = clf.means_[0, 0]
        var = clf.covariances_[0, 0]
    #print(mean,var,np.sqrt(var))
    image = (image - mean) / (2*3*np.sqrt(var))

    return image

def normalize(image, margin_size=0):
    """
    Normalize an image. If wanted, a specified relative margin can be ignored.
    :param image: Image to normalize
    :param margin_size: Relative size of the margin to be ignored during normalization. Number between 0 - 1.
    :return: Normalized image
    """
    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]
    img_mean = np.mean(image[mask])
    img_std = np.std(image[mask])

    image = (image - img_mean) / (3 * 2 * img_std+0.000001)

    return image


def bbox_iou(box1, box2):
    """
    Calculates the intersection of union for two boxes.
    :param box1: First box
    :param box2: Second box
    :return: Intersection of union
    """
    x1_min = box1.x - box1.w / 2
    x1_max = box1.x + box1.w / 2
    y1_min = box1.y - box1.h / 2
    y1_max = box1.y + box1.h / 2

    x2_min = box2.x - box2.w / 2
    x2_max = box2.x + box2.w / 2
    y2_min = box2.y - box2.h / 2
    y2_max = box2.y + box2.h / 2

    intersect_w = interval_overlap([x1_min, x1_max], [x2_min, x2_max])
    intersect_h = interval_overlap([y1_min, y1_max], [y2_min, y2_max])

    intersect = intersect_w * intersect_h

    union = box1.w * box1.h + box2.w * box2.h - intersect

    return float(intersect) / union


def interval_overlap(interval_a, interval_b):
    """
    Calculates the overlap between two intervals
    :param interval_a: Tuple with two elements (lower and upper bound)
    :param interval_b: Tuple with two elements (lower and upper bound)
    :return: Overlap between two intervals
    """
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2, x4) - x1
    else:
        if x2 < x3:
            return 0
        else:
            return min(x2, x4) - x3


def sigmoid(x):
    """
    Sigmoid function
    :param x: argument
    :return: sigmoid of x
    """
    return 1.0 / (1.0 + np.exp(-x))


def get_num_fine_tune_layers(path_weights):
    import h5py

    with h5py.File(path_weights, mode="r") as f:
        try:
            num_free_layers = int(list(f["num_free_layers"])[0])
        except KeyError:
            num_free_layers = None
    return num_free_layers


def filter_image_noise2noise(img_path, model_path, padding=15, batch_size=4):
    """
    Filters an images using JANNI (noise2noise implementation)
    :param img_path: Input image
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :return: Denoised image
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    image = imagereader.image_read(img_path)
    fitlered_img = janni_predict.predict_np(
        model, image, patch_size=(1024, 1024), padding=padding, batch_size=batch_size
    )

    return fitlered_img


def filter_images_noise2noise_dir(
    img_paths,
    output_dir_filtered_imgs,
    model_path,
    padding=15,
    batch_size=4,
    resize_to=None,
):
    """
    Filters multiple images using JANNI (noise2noise implementation) and save it to disk
    :param img_paths: List of images paths
    :param output_dir_filtered_imgs: Path to write denoised images
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :param resize_to: Size to which to output is resized
    :return:
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    filtered_paths = janni_predict.predict_list(
        image_paths=img_paths,
        output_path=output_dir_filtered_imgs,
        model=model,
        patch_size=patch_size,
        padding=padding,
        batch_size=batch_size,
        output_resize_to=resize_to,
    )

    return filtered_paths


def write_command(filename, txt):
    try:
        import os

        os.makedirs(os.path.dirname(filename))
    except Exception:
        pass

    text_file = open(filename, "w")
    text_file.write(txt)
    text_file.close()


def check_for_updates():
    """
    Checks if cryolo updates are available
    :return: None
    """
    try:
        import cryolo

        with urllib.request.urlopen(
            url="https://pypi.org/pypi/cryolo/json", timeout=5
        ) as url:
            data = json.loads(url.read().decode())
            from distutils.version import LooseVersion as V

            current_version = cryolo.__version__
            latest_version = current_version
            for ver in data["releases"].keys():
                vers = V(ver)
                if vers > V(latest_version) and len(vers.version) == 3:
                    latest_version = ver
            if V(latest_version) > V(current_version):
                print("###############################################")
                print("New version of crYOLO available")
                print("Local version:\t\t", current_version)
                print("Latest version:\t\t", latest_version)
                print(
                    "More information here:\n",
                    "https://cryolo.readthedocs.io/en/latest/changes.html",
                )
                print("###############################################")
    except Exception as e:
        print("###############################################")
        print("Skip version check, as it failed with the following error:")
        print(e)
        print("###############################################")
        pass
