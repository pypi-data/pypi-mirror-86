""" Utilitary function for Mapillary dataset analysis
"""

import json
import os

import daiquiri
import numpy as np
import pandas as pd
from PIL import Image

from deeposlandia.datasets import GEOGRAPHIC_DATASETS


logger = daiquiri.getLogger(__name__)


def read_config(filename):
    """Read the JSON configuration file.

    Parameters
    ----------
    filename : str
        Path of the configuration file

    Returns
    -------
    dict
        Dataset glossary
    """
    with open(filename) as fobj:
        return json.load(fobj)


def build_labels(filtered_image, label_ids, dataset="mapillary"):
    """Build a list of integer labels that are contained into a candidate
    filtered image; according to its pixels

    Parameters
    ----------
    filtered_image : np.array
        Image to label, under the numpy.array format
    label_ids : list
        List of labels ids contained into the reference classification

    Returns
    -------
    dict
        label ids occur or not in the image
    """
    image_data = np.array(filtered_image)
    available_labels = np.unique(image_data)
    if dataset == "aerial":
        available_labels[available_labels == 255] = 1
    return {i: 1 if i in available_labels else 0 for i in label_ids}


def resize_image(img, base_size):
    """ Resize image `img` such that min(width, height)=base_size; keep image
    proportions

    Parameters:
    -----------
    img: Image
        input image to resize
    base_size: integer
        minimal dimension of the returned image
    """
    old_width, old_height = img.size
    if old_width < old_height:
        new_size = (base_size, int(base_size * old_height / old_width))
    else:
        new_size = (int(base_size * old_width / old_height), base_size)
    return img.resize(new_size)


def mono_crop_image(img, crop_pixel):
    """Crop image `img` so as its dimensions become equal (width=height),
    without modifying its smallest dimension
    """
    if img.width > img.height:
        return img.crop((crop_pixel, 0, crop_pixel + img.height, img.height))
    else:
        return img.crop((0, crop_pixel, img.width, crop_pixel + img.width))


def flip_image(img, proba=0.5):
    """ Flip image `img` horizontally with a probability of `proba`

    Parameters:
    -----------
    img: Image
        input image to resize
    proba: float
        probability of flipping input image (if less than 0.5, no flipping)
    """
    if np.random.sample() < proba:
        return img
    else:
        return img.transpose(Image.FLIP_LEFT_RIGHT)


def list_to_str(seq, sep="-"):
    """Transform the input sequence into a ready-to-print string

    Parameters
    ----------
    seq : list, tuple, dict
        Input sequence that must be transformed
    sep : str
        Separator that must appears between each `seq` items

    Returns
    -------
    str
        Printable version of input list
    """
    return sep.join(str(i) for i in seq)


def prepare_input_folder(datapath, dataset):
    """Data path and repository management; create and return the raw dataset
    path

    Parameters
    ----------
    datapath : str
        Data root directory, contain all used the datasets
    dataset : str
        Dataset name, *e.g.* `mapillary` or `shapes`

    Returns
    -------
    str
        Dataset raw image path

    """
    input_folder = os.path.join(datapath, dataset, "input")
    os.makedirs(input_folder, exist_ok=True)
    return input_folder


def prepare_preprocessed_folder(
    datapath, dataset, image_size
):
    """Data path and repository management; create all the folders needed to
    accomplish the current instance training/testing

    Parameters
    ----------
    datapath : str
        Data root directory, contain all used the datasets
    dataset : str
        Dataset name, *e.g.* `mapillary` or `shapes`
    image_size : int
        Size of the considered images (height and width are equal)

    Returns
    -------
    dict
        All the meaningful folders and dataset configuration file as a
    dictionary
    """
    prepro_folder = os.path.join(
        datapath,
        dataset,
        "preprocessed",
        str(image_size)
    )
    training_filename = os.path.join(prepro_folder, "training.json")
    validation_filename = os.path.join(prepro_folder, "validation.json")
    testing_filename = os.path.join(prepro_folder, "testing.json")
    training_folder = os.path.join(prepro_folder, "training")
    validation_folder = os.path.join(prepro_folder, "validation")
    testing_folder = os.path.join(prepro_folder, "testing")
    os.makedirs(os.path.join(training_folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(training_folder, "labels"), exist_ok=True)
    os.makedirs(os.path.join(validation_folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(validation_folder, "labels"), exist_ok=True)
    os.makedirs(os.path.join(testing_folder, "images"), exist_ok=True)
    return {
        "training": training_folder,
        "validation": validation_folder,
        "testing": testing_folder,
        "training_config": training_filename,
        "validation_config": validation_filename,
        "testing_config": testing_filename,
    }


def prepare_output_folder(datapath, dataset, image_size, model):
    """Dataset and repository management; create and return the dataset output
    path

    Parameters
    ----------
    datapath : str
        Data root directory, contain all used the datasets
    dataset : str
        Dataset name, *e.g.* `mapillary` or `shapes`
    image_size : int
        Size of the considered images (height and width are equal)
    model : str
        Research problem that is tackled, *e.g.* `featdet` or `semseg`

    Returns
    -------
    dict
        Dataset output paths
    """
    output_folder = os.path.join(datapath, dataset, "output", model)
    os.makedirs(output_folder, exist_ok=True)
    checkpoint_folder = os.path.join(output_folder, "checkpoints")
    os.makedirs(checkpoint_folder, exist_ok=True)
    best_model_filename = "best-model-" + str(image_size) + ".h5"
    best_instance_filename = "best-instance-" + str(image_size) + ".json"
    label_folder = os.path.join(output_folder, "predicted_labels")
    os.makedirs(label_folder, exist_ok=True)
    geometry_folder = raster_folder = None
    if dataset in GEOGRAPHIC_DATASETS:
        geometry_folder = os.path.join(output_folder, "predicted_geometries")
        raster_folder = os.path.join(output_folder, "predicted_rasters")
        os.makedirs(geometry_folder, exist_ok=True)
        os.makedirs(raster_folder, exist_ok=True)
    return {
        "best-model": os.path.join(checkpoint_folder, best_model_filename),
        "best-instance": os.path.join(checkpoint_folder, best_instance_filename),
        "checkpoints": checkpoint_folder,
        "geometries": geometry_folder,
        "labels": label_folder,
        "rasters": raster_folder,
    }


def recover_instance(instance_path):
    """Recover instance specification for model design, *i.e.* dropout rate and
    network architecture

    Parameters
    ----------
    instance_path : str
        Path of the instance specifications on the file system

    Returns
    -------
    tuple
        Instance dropout and network architecture
    """
    with open(instance_path) as fobj:
        instance = json.load(fobj)
    return instance["dropout"], instance["network"]


def GetHTMLColor(color):
    """Convert single-channeled colors or (R, G, B) tuples to #RRGGBB.

    If the color has only one channel (grayscale, typically), it is converted
    to a (R, G, B) tuple first.

    Parameters
    ----------
    color : int or list
        Grayscale value or list of red, green, blue pixel values

    Returns
    -------
    str
        HTML-version of color
    """
    rgb_tuple = (color, color, color) if type(color) == int else color
    return "#%02x%02x%02x" % tuple(rgb_tuple)


def build_image_from_config(data, config):
    """Rebuild a labelled image version from dataset configuration

    Parameters
    ----------
    data : numpy.array
        Labelled image as a numpy array of shape (img_size, img_size, 3) ;
    squared-size, shape (imsize, imsize)
    config : dict
        Label definition and description

    Returns
    -------
    np.array
        RGB-version of labelled images, with shape (imsize, imsize, 3)
    """
    result = np.zeros(
        shape=(data.shape[0], data.shape[1], 3), dtype=data.dtype
    )
    for label in range(len(config)):
        mask = data == label
        result[mask] = config[label]["color"]
    return Image.fromarray(result)


def create_symlink(link_name, directory):
    """Create a symbolic link

    Based on
    https://github.com/elemoine/dotfiles/blob/master/install-dotfiles.py

    Parameters
    ----------
    link_name : string
        name of the symbolic link
    directory : string
        Targetted destination for the symbolic link
    """
    if os.path.islink(link_name):
        os.unlink(link_name)
    elif os.path.isfile(link_name):
        logger.error("%s is a file!", link_name)
    elif os.path.isdir(link_name):
        logger.error("%s is a directory!", link_name)
    os.symlink(directory, link_name)
    logger.info("%s now points to %s.", link_name, directory)
