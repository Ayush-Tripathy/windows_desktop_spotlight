#!/usr/bin/env python

from os import chdir, listdir, path, getcwd
import sys
import config
import constants
import shutil


if constants.flags.DEL_FLAG in sys.argv:
    config.fs.rm_from_startup(constants.BAT_FILE_NAME)
    config.scheduler.delete_task(constants.TASK_NAME)
    if path.exists(constants.DATA_PATH):
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

SCRIPT_PATH = path.join(constants.SCRIPT_DIRECTORY, constants.SCRIPT_NAME)

if constants.TAKE_INPUT:
    prompt_text = "Enter wallpaper mode [ sync | static | slideshow ]: "
    choice = input(prompt_text)

    if choice not in constants.CHOICES.keys():
        print("Invalid choice, terminating...")
        sys.exit(-2)
    constants.CHOICE = constants.CHOICES[choice]

    approval = ["y", "yes"]
    denial = ["n", "no"]
    valid_approval_inputs = ["y", "n", "yes", "no"]

    to_save = input("Save your choice? [y/n] : ")
    to_save = to_save.lower()

    if to_save in valid_approval_inputs:
        if to_save in approval:
            with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                pref_file.write(choice)
        elif to_save in denial:
            save_choice = input("\n"
                                "[Specify the mode you want to apply by default \n"
                                "when running DesktopSpotlight from next time]\n"
                                "Enter mode: ")

            if save_choice in constants.CHOICES.keys():
                with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                    pref_file.write(save_choice)
            else:
                print("Invalid choice.")

    else:
        print("Invalid input.")

    to_update_startup_file = input("Use this preference at windows startup? [y/n] : ")
    to_update_startup_file = to_update_startup_file.lower()

    if to_update_startup_file in valid_approval_inputs:
        if to_update_startup_file in approval:
            constants.UPDATE_STARTUP_FILE = True
            with open(constants.STARTUP_FILE, "w+") as pref_file:
                pref_file.write(choice)
        elif to_update_startup_file in denial:
            save_choice = input("\n"
                                "[Specify the mode you want to apply by default \n"
                                "after windows startup]\n"
                                "Enter mode: ")

            if save_choice in constants.CHOICES.keys():
                with open(constants.STARTUP_FILE, "w+") as pref_file:
                    pref_file.write(save_choice)
            else:
                print("Invalid choice.")
    else:
        print("Invalid input.")

if constants.TAKE_INPUT:
    flags = input("Enter any flags (separate with single space): ")
    flags = flags.split(" ")

    ignore_flags = [constants.flags.SYNC_FLAG, constants.flags.STATIC_FLAG, constants.flags.SLIDESHOW_FLAG]
    handlers.flags_handler.handle_flags(flags, exclude=ignore_flags)


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

# print("Current working directory:", os.getcwd())
log.info(f"Current working directory: {getcwd()}")

# Fetch all possible wallpapers
possible_wallpapers = utils.misc.scan_wallpapers()

# Change current directory to 'images' directory
chdir(constants.IMAGES_PATH)

# Save all wallpapers to data path
wallpapers = utils.save_wallpapers(possible_wallpapers)

# Get all file names from 'images' directory
images = listdir(getcwd())

# Filter wallpapers
filtered_wallpapers = utils.misc.filter_wallpapers(wallpapers)

try:
    constants.CHOICE = constants.CHOICES[choice]
except KeyError:
    pass

if constants.CHOICE == constants.SLIDE_SHOW:
    utils.ld_wallpapers.start_slideshow(filtered_wallpapers)
elif constants.CHOICE == constants.STATIC:
    utils.ld_wallpapers.set_static(filtered_wallpapers)
elif constants.CHOICE == constants.SYNC:
    utils.ld_wallpapers.sync(filtered_wallpapers)
