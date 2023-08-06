import logging
import os

import numpy as np
from ruamel.yaml import YAML
from aicsimageio import AICSImage, writers
from skimage.filters import threshold_otsu
from tqdm import tqdm

from aics_tf_registration.core import alignment, preprocessing


class Image_Aligner:
    ###############################################################################
    # Main Functions
    ###############################################################################

    def __init__(self, config_path: str):
        """Load settings and file paths from configuration file

        Parameters
        ------------
            - config_path: path to yaml file with settings and file paths

        """
        # Load configuration file
        logger = logging.getLogger("Aligner.init")
        logger.setLevel(logging.DEBUG)
        logger.debug("Reading settings from config file")

        yaml = YAML(typ="safe")
        config = yaml.load(open(config_path, "r"), Loader=yaml.FullLoader)

        # Load input/output settings
        self.source_path = config["source_path"]
        self.target_path = config["target_path"]
        out_path = config["output_path"]
        self.source_output = os.path.join(out_path, "source")
        self.target_output = os.path.join(out_path, "target")
        self.save_composite = config["save_alignment_composite"]

        # Make sure input/output folders are valid and create output folders
        try:
            assert os.path.isdir(self.source_path)
        except AssertionError:
            logger.critical(f"Source path '{self.source_path}' is invalid")
            raise
        try:
            assert os.path.isdir(self.target_path)
        except AssertionError:
            logger.critical(f"Target path '{self.target_path}' is invalid")
            raise
        try:
            assert os.path.isdir(out_path)
        except AssertionError:
            try:
                os.mkdir(out_path)
            except (RuntimeError, TypeError, ValueError):
                logger.critical(f"Output path '{out_path}' is invalid")
                raise

        if not os.path.exists(self.source_output):
            os.mkdir(self.source_output)
        if not os.path.exists(self.target_output):
            os.mkdir(self.target_output)
        if self.save_composite:
            self.composite_path = os.path.join(out_path, "alignment_composite")
            if not os.path.exists(self.composite_path):
                os.mkdir(self.composite_path)
        else:
            self.composite_path = None

        # List images in source and target folders and check they are not empty
        # and equal in length
        self.source_files = self.get_image_list(self.source_path)
        self.target_files = self.get_image_list(self.target_path)
        try:
            assert self.source_files is not None
        except AssertionError:
            logger.critical("Source folder is empty of valid image files")
            raise
        try:
            assert self.target_files is not None
        except AssertionError:
            logger.critical("Target folder is empty of valid image files")
            raise
        try:
            assert len(self.source_files) == len(self.target_files)
        except AssertionError:
            logger.warning(
                f"Source folder has {len(self.source_files)} images while target folder has {len(self.target_files)}. Some images might be missing."  # noqa
            )

        # Load alignment parameters and check validity
        self.scale_factor_xy = config["scale_factor_xy"]
        self.scale_factor_z = config["scale_factor_z"]
        self.transforms = config["transforms"]
        self.source_crop = config["source_crop"]
        self.target_crop = config["target_crop"]
        self.smaller_fov_modality = config["smaller_fov_modality"]
        self.prealign_z = config["prealign_z"]
        self.use_refinement = config["use_refinement"]
        self.denoise_z = config["denoise_z"]
        try:
            self.pad_z = config["pad_z"]
        except KeyError:
            self.pad_z = False
        try:
            self.pad_size = config["pad_size"]
        except KeyError:
            self.pad_size = 10
        try:
            assert self.smaller_fov_modality in ["source", "target"]
        except AssertionError:
            logger.critical(
                f"'smaller_fov_modatlity' must be 'source' or 'target', not {self.smaller_fov_modality}"  # noqa
            )
            raise
        valid_transforms = ["flip_lr", "flip_ud", "rotate_90", "rotate_180"]
        for transform in self.transforms:
            try:
                assert transform in valid_transforms
            except AssertionError:
                logger.critical(
                    f"{transform} is not a valid option. Valid transforms are: {valid_transforms}"  # noqa
                )
                raise

        self.source_alignment_channel = config["source_alignment_channel"]
        self.target_alignment_channel = config["target_alignment_channel"]

        self.source_output_channel = config["source_output_channel"]
        self.target_output_channel = config["target_output_channel"]

        if not isinstance(self.source_output_channel, list):
            self.source_output_channel = [self.source_output_channel]
        if not isinstance(self.target_output_channel, list):
            self.target_output_channel = [self.target_output_channel]

    def align_images(self):
        """Run alignment algorithm on image pairs in dataset"""

        logger = logging.getLogger("Aligner.run")
        logger.setLevel(logging.DEBUG)
        logger.info("Beginning alignments on dataset")
        for i, (source_file) in enumerate(tqdm(self.source_files)):
            logger.info(
                "--------------------------------------------------------------------"
            )
            logger.info(
                f"Beginning alignment of image pair {i} with filename '{source_file}'"
            )
            logger.info(
                "--------------------------------------------------------------------"
            )

            # Check if the source image has a match in the list of target images
            try:
                assert source_file in self.target_files
            except AssertionError:
                logger.warning(
                    f"File with name '{source_file}' not found among target files. Skipping this image pair."  # noqa
                )
                continue

            if os.path.isfile(
                os.path.join(self.source_output, source_file.replace(".czi", ".tiff"))
            ):
                logger.warning(
                    f"File with name '{source_file.replace('.czi', '.tiff')}' already exists in output folder. Skipping this image pair."  # noqa
                )
                continue

            # Load and preprocess images
            target_file = source_file
            source = np.array(
                AICSImage(os.path.join(self.source_path, source_file)).data
            ).squeeze()
            target = np.array(
                AICSImage(os.path.join(self.target_path, target_file)).data
            ).squeeze()

            if source.ndim == 4:
                if np.argmin(source.shape) != 0:
                    logger.debug(
                        f"Rearranging channels in source image. Current shape is {source.shape}"  # noqa
                    )
                    source = preprocessing.rearrange_multichannel_image(source)
                    logger.debug(f"New shape is {source.shape}")
            if target.ndim == 4:
                if np.argmin(target.shape) != 0:
                    logger.debug(
                        f"Rearranging channels in target image. Current shape is {target.shape}"  # noqa
                    )
                    target = preprocessing.rearrange_multichannel_image(target)
                    logger.debug(f"New shape is {target.shape}")

            if self.pad_z:
                # estimate background threshold of each channel
                source_bg = [threshold_otsu(source[c]) for c in range(source.shape[0])]
                target_bg = [threshold_otsu(target[c]) for c in range(target.shape[0])]

                # determine mean and standard deviation of background signal
                source_means = [
                    np.mean(source[c][source[c] < thresh], axis=None)
                    for c, (thresh) in enumerate(source_bg)
                ]
                source_stds = [
                    np.std(source[c][source[c] < thresh], axis=None)
                    for c, (thresh) in enumerate(source_bg)
                ]
                target_means = [
                    np.mean(target[c][target[c] < thresh], axis=None)
                    for c, (thresh) in enumerate(target_bg)
                ]
                target_stds = [
                    np.std(target[c][target[c] < thresh], axis=None)
                    for c, (thresh) in enumerate(target_bg)
                ]

                # generate synthetic background layers as gaussian noise
                source_pad = None
                target_pad = None
                for _, (mean, std) in enumerate(zip(source_means, source_stds)):
                    temp = np.random.normal(
                        mean, std, (1, self.pad_size, source.shape[2], source.shape[3])
                    ).astype(np.uint16)
                    if source_pad is None:
                        source_pad = temp
                    else:
                        source_pad = np.concatenate((source_pad, temp), axis=0)
                for _, (mean, std) in enumerate(zip(target_means, target_stds)):
                    temp = np.random.normal(
                        mean, std, (1, self.pad_size, target.shape[2], target.shape[3])
                    ).astype(np.uint16)
                    if target_pad is None:
                        target_pad = temp
                    else:
                        target_pad = np.concatenate((target_pad, temp), axis=0)

                # create channel labeling padding in source and target images
                source_pad_label = np.expand_dims(np.zeros_like(source_pad[0]), axis=0)
                source_content_label = (
                    np.expand_dims(np.ones_like(source[0]), axis=0) * 255
                )
                source_label = np.concatenate(
                    (source_pad_label, source_content_label, source_pad_label), axis=1
                )

                target_pad_label = np.expand_dims(np.zeros_like(target_pad[0]), axis=0)
                target_content_label = (
                    np.expand_dims(np.ones_like(target[0]), axis=0) * 255
                )
                target_label = np.concatenate(
                    (target_pad_label, target_content_label, target_pad_label), axis=1
                )

                # pad images with synthetic layers
                source = np.concatenate((source_pad, source, source_pad), axis=1)
                target = np.concatenate((target_pad, target, target_pad), axis=1)
                logger.debug(f"New source shape is {source.shape}")
                logger.debug(f"New target shape is {target.shape}")

                # add content label channels and add to output channel list
                source = np.concatenate((source, source_label), axis=0)
                target = np.concatenate((target, target_label), axis=0)

                sh_source = source.shape
                sh_target = target.shape

                self.source_output_channel.append(sh_source[0] - 1)
                self.target_output_channel.append(sh_target[0] - 1)

            logger.debug("Cropping source image")
            source = preprocessing.precrop_image(source, self.source_crop)
            logger.debug("Cropping target image")
            target = preprocessing.precrop_image(target, self.target_crop)

            if self.smaller_fov_modality == "source":
                logger.debug("Applying image transforms to source")
                source = preprocessing.apply_transforms(source, self.transforms)
            if self.smaller_fov_modality == "target":
                logger.debug("Applying transforms to target")
                target = preprocessing.apply_transforms(target, self.transforms)

            logger.debug("Beginning alignment process")
            a_src, a_tgt, composite = alignment.perform_alignment(
                source,
                target,
                self.smaller_fov_modality,
                self.scale_factor_xy,
                self.scale_factor_z,
                self.source_alignment_channel,
                self.target_alignment_channel,
                self.source_output_channel,
                self.target_output_channel,
                self.prealign_z,
                self.denoise_z,
                self.use_refinement,
                self.save_composite,
            )

            if (a_src is not None) and (
                (self.save_composite and composite is not None)
                or (not self.save_composite and composite is None)
            ):

                logger.info(f"Alignment #{i} succeeded")
                if ".czi" in source_file:
                    source_file = source_file.replace(".czi", ".tiff")
                    target_file = target_file.replace(".czi", ".tiff")

                logger.debug(f"final shape of source image is: {a_src.shape}")
                logger.debug(f"final shape of target image is: {a_tgt.shape}")
                try:
                    with writers.OmeTiffWriter(
                        os.path.join(self.source_output, source_file),
                        overwrite_file=True,
                    ) as writer:
                        writer.save(a_src, dimension_order="CZYX")
                    with writers.OmeTiffWriter(
                        os.path.join(self.target_output, target_file),
                        overwrite_file=True,
                    ) as writer:
                        writer.save(a_tgt, dimension_order="CZYX")
                except RuntimeError:
                    logger.warning("Error in saving images")
                    composite = None
                if self.save_composite and composite is not None:
                    logger.debug("Saving composite of alignment")
                    composite = np.transpose(composite, axes=(3, 0, 1, 2))
                    with writers.OmeTiffWriter(
                        os.path.join(self.composite_path, source_file),
                        overwrite_file=True,
                    ) as writer:
                        writer.save(composite, dimension_order="CZYX")
            else:
                logger.warning(f"Alignment #{i}  failed")

    ##############################################################################
    # Support Functions
    ##############################################################################

    def get_image_list(self, path):
        dir_list = os.listdir(path)
        im_files = [
            f for f in dir_list if ((".tif" in f) or (".tiff" in f) or (".czi" in f))
        ]
        im_files.sort()

        return im_files
