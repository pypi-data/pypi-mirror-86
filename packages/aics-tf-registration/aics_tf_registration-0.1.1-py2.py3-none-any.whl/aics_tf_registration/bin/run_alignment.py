#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from aics_tf_registration.core import image_aligner
from datetime import datetime
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", required=True)
    args = parser.parse_args()

    config_name = os.path.basename(args.config_path)
    config_name = config_name.replace(".yaml", "").replace("_config", "")

    now = datetime.now()
    start_time = now.strftime("%d-%m-%y_%H:%M")
    fh = logging.FileHandler(f"{config_name}__{start_time}.log")
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[fh, sh],
    )
    logger = logging.getLogger("main")

    logger.debug(f"Configuration file: {args.config_path}")
    try:
        assert os.path.exists(args.config_path)
    except AssertionError:
        logger.critical("Configuration file path is invalid")
        raise

    aligner = image_aligner.Image_Aligner(args.config_path)
    aligner.align_images()


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
