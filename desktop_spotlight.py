#!/usr/bin/env python

import os
import sys
import config
import constants
import shutil


if constants.flags.DEL_FLAG in sys.argv:
    config.fs.rm_from_startup(constants.BAT_FILE_NAME)
    config.scheduler.delete_task(constants.TASK_NAME)
    if os.path.exists(constants.DATA_PATH):
        shutil.rmtree(constants.DATA_PATH)
        print("All Desktop Spotlight files are removed.")
    else:
        print("No Desktop Spotlight files found.")
    sys.exit(0)

if config.fs.verify_files(sys.argv):
    import handlers
    sys.excepthook = handlers.error_handler
    handlers.flags_handler.handle_flags(sys.argv)

    import utils
    from utils import py_logger
else:
    print("Some files are missing or corrupted")
    print("Try to fix it using '-r' flag")
    sys.exit(-1)


log = py_logger.get_logger(__name__, "debug")

# Choose what to apply i.e. slideshow (1) or static (2) or sync (3)
choice = constants.SYNC

SCRIPT_PATH = os.path.join(constants.SCRIPT_DIRECTORY, constants.SCRIPT_NAME)

if constants.STARTUP_WAY == constants.START_BY_BATCH:
    config.scheduler.delete_task(constants.TASK_NAME)

    # Add a batch file to startup folder in windows
    config.fs.add_to_startup(sys.argv, SCRIPT_PATH, constants.BAT_FILE_NAME, force=True)

elif constants.STARTUP_WAY == constants.START_BY_SCHEDULER:
    config.fs.rm_from_startup(constants.BAT_FILE_NAME)

    # Create a task in Task Scheduler
    config.scheduler.create_task(sys.argv, SCRIPT_PATH, constants.TASK_NAME)

    # if "-r" in sys.argv or constants.UPDATE_STARTUP_TASK:
    #     config.scheduler.create_task(sys.argv, SCRIPT_PATH, constants.TASK_NAME)
    # else:
    #     config.scheduler.create_task(sys.argv, SCRIPT_PATH, constants.TASK_NAME)

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

if constants.CHOICE == constants.SLIDE_SHOW:
    utils.ld_wallpapers.start_slideshow(filtered_wallpapers)
elif constants.CHOICE == constants.STATIC:
    utils.ld_wallpapers.set_static(filtered_wallpapers)
elif constants.CHOICE == constants.SYNC:
    utils.ld_wallpapers.sync(filtered_wallpapers)
