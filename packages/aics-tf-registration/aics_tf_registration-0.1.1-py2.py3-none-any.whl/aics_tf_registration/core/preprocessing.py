import logging
from typing import List

import numpy as np
import skimage.transform as tf
from scipy.ndimage import rotate


def rearrange_multichannel_image(image: np.ndarray):
    """Rearrange the order of dimensions so that the channel dimension is first

    Parameters
    ------------
        - image: 4d image

    Return
    -----------
        -image: image with channels rearranged

    """
    logger = logging.getLogger("preprocess.rearrange")
    logger.setLevel(logging.DEBUG)
    try:
        assert image.ndim == 4
    except AssertionError:
        logger.critical("Image must be 4D to rearrange channels")
        return image

    channel_dimension = np.argmin(np.shape(image))
    if channel_dimension == 1:
        image = np.transpose(image, [1, 0, 2, 3])
    if channel_dimension == 2:
        image = np.transpose(image, [2, 0, 1, 3])
    if channel_dimension == 3:
        image = np.transpose(image, [3, 0, 1, 2])

    return image


def precrop_image(image: np.ndarray, scales: np.ndarray):
    """Applies precropping to the image

    Parameters
    ------------
        - image: 3D or 4D image
        - scales: array containing percent of each axis to crop

    Return
    -----------
        - image_cropped: cropped image

    """
    logger = logging.getLogger("preprocess.precrop")
    logger.setLevel(logging.DEBUG)

    logger.debug(f"Cropping parameters: {scales}")
    scales = np.array(scales)

    try:
        assert scales.shape == (3, 1) or scales.shape == (3, 2)
    except AssertionError:
        logger.critical(f"Crop settings must be 3x1 or 3x2, not {scales.shape}")
        raise
    try:
        assert image.ndim == 3 or image.ndim == 4
    except AssertionError:
        logger.critical(f"Image must be 3D or 4D, not {image.ndim}D")

    logger.debug(f"Starting shape: {image.shape}")
    image_shape = np.shape(image)
    if image.ndim == 4:
        crop_z_start = int(image_shape[1] * scales[0, 0])
        crop_z_end = int(image_shape[1] - image_shape[1] * scales[0, -1])

        crop_x_start = int(image_shape[2] * scales[1, 0])
        crop_x_end = int(image_shape[2] - image_shape[2] * scales[1, -1])

        crop_y_start = int(image_shape[3] * scales[2, 0])
        crop_y_end = int(image_shape[3] - image_shape[3] * scales[2, -1])

        image_cropped = image[
            :, crop_z_start:crop_z_end, crop_x_start:crop_x_end, crop_y_start:crop_y_end
        ]
    elif image.ndim == 3:
        crop_z_start = int(image_shape[0] * scales[0, 0])
        crop_z_end = int(image_shape[0] - image_shape[0] * scales[0, -1])

        crop_x_start = int(image_shape[1] * scales[1, 0])
        crop_x_end = int(image_shape[1] - image_shape[1] * scales[1, -1])

        crop_y_start = int(image_shape[2] * scales[2, 0])
        crop_y_end = int(image_shape[2] - image_shape[2] * scales[2, -1])

        image_cropped = image[
            crop_z_start:crop_z_end, crop_x_start:crop_x_end, crop_y_start:crop_y_end
        ]

    logger.debug(f"Cropped shape: {image_cropped.shape}")
    return image_cropped


def apply_transforms(image: np.ndarray, transform_list: List[str]):
    """Apply the transformations from list provided to the moving image

    Parameters
    ------------
        - image: 3D or 4D image
        - transform list: list of transforms to apply in sequence to image

    Returns
    -----------
        - image: transformed image

    """
    logger = logging.getLogger("preprocess.transfrom")
    logger.setLevel(logging.DEBUG)

    for transform in transform_list:
        logger.debug(f"Applying transform: {transform}")
        logger.debug(f"Current shape: {image.shape}")

        if transform == "flip_lr":
            if image.ndim == 3:
                image = np.flip(image, axis=1)
            else:
                image = np.flip(image, axis=2)

        if transform == "flip_ud":
            if image.ndim == 3:
                image = np.flip(image, axis=2)
            else:
                image = np.flip(image, axis=3)

        if transform == "rotate_90":
            if image.ndim == 3:
                image = rotate(image, 90, axes=(1, 2))
            else:
                image = rotate(image, 90, axes=(2, 3))

        if transform == "rotate_180":
            if image.ndim == 3:
                image = rotate(image, 180, axes=(1, 2))
            else:
                image = rotate(image, 180, axes=(2, 3))

        logger.debug(f"New shape: {image.shape}")

    return image


def rescale_image(image: np.ndarray, scale_factor_xy: float, scale_factor_z: float):
    """Upsample/Downsample the image to match voxel dimensions of the other image.

    Parameters
    ------------
        - image: 3D or 4D image to rescale
        - scale_factor_xy: Upsample/downsample rate in x and y
        - scale_factor_z: Upsample/downsample rate in z

    Returns
    ------------
        - image: rescaled image

    """

    if image.ndim == 3:
        return tf.resize(
            image,
            (
                int(round(image.shape[0] * scale_factor_z)),
                int(round(image.shape[1] * scale_factor_xy)),
                int(round(image.shape[2] * scale_factor_xy)),
            ),
            preserve_range=True,
        ).astype(np.uint16)
    if image.ndim == 4:
        return tf.resize(
            image,
            (
                image.shape[0],
                int(round(image.shape[1] * scale_factor_z)),
                int(round(image.shape[2] * scale_factor_xy)),
                int(round(image.shape[3] * scale_factor_xy)),
            ),
            preserve_range=True,
        ).astype(np.uint16)
