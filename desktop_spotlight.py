#!/usr/bin/env python

import os
import sys
import constants
import utils
from utils import py_logger

log = py_logger.get_logger(__name__, "debug")

# Choose what to apply i.e. slideshow (1) or latest image (2)
choice = constants.SYNC

utils.misc.verify_files(sys.argv)

SCRIPT_PATH = os.path.join(constants.SCRIPT_DIRECTORY, constants.SCRIPT_NAME)

# Add a batch file to startup folder in windows
if "-r" in sys.argv:
    utils.misc.add_to_startup(SCRIPT_PATH, "open_ds.bat", force=True)
else:
    utils.misc.add_to_startup(SCRIPT_PATH, "open_ds.bat", force=False)

print("Current working directory:", os.getcwd())
log.info(f"Current working directory: {os.getcwd()}")

# Fetch all possible wallpapers
possible_wallpapers = utils.misc.scan_wallpapers()

# Change current directory to 'images' directory
os.chdir(constants.IMAGES_PATH)

# Save all wallpapers to data path
wallpapers = utils.save_wallpapers(possible_wallpapers)

# Get all file names from 'images' directory
images = os.listdir(os.getcwd())

# Filter wallpapers
filtered_wallpapers = utils.misc.filter_wallpapers(wallpapers)

if choice == constants.SLIDE_SHOW:
    utils.ld_wallpapers.start_slideshow(filtered_wallpapers)
elif choice == constants.STATIC:
    utils.ld_wallpapers.set_static(filtered_wallpapers)
elif choice == constants.SYNC:
    utils.ld_wallpapers.sync(filtered_wallpapers)
