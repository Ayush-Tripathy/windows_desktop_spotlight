# import shutil
# import os
import os.path
import shutil
import sys
import config
import constants
import pyuac


def handle_flags(argv: list, exclude=None):
    if exclude is None:
        exclude = []

    if "-f" in argv:
        pass

    if constants.flags.CLEAR_FLAG in argv and constants.flags.CLEAR_FLAG not in exclude:
        config.fs.rm_from_startup(constants.BAT_FILE_NAME)
        config.scheduler.delete_task(constants.TASK_NAME)

        remove_files()
        print("Exit")
        sys.exit(1)

    if constants.flags.RESET_FLAG in argv and constants.flags.RESET_FLAG not in exclude:
        reset(argv, verifyfiles=True)

    if constants.flags.SAVE_TASK_FLAG in argv and constants.flags.SAVE_TASK_FLAG not in exclude:
        if not pyuac.isUserAdmin():
            print("Admin rights required: please open with admin rights.")
            if constants.flags.NOSAVE_FLAG not in sys.argv:
                input("Press enter to exit.\n")
                sys.exit(-2)

        constants.STARTUP_WAY = constants.START_BY_SCHEDULER

    if constants.flags.SAVE_BAT_FLAG in argv and constants.flags.SAVE_BAT_FLAG  not in exclude:
        constants.STARTUP_WAY = constants.START_BY_BATCH

    if constants.flags.SYNC_FLAG in argv and constants.flags.SYNC_FLAG not in exclude:
        constants.CHOICE = constants.SYNC
        constants.TAKE_INPUT = False

        if constants.flags.NOSAVE_FLAG not in argv:
            with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                pref_file.write("sync")

            with open(constants.STARTUP_FILE, "w+") as pref_file:
                pref_file.write("sync")

    elif constants.flags.STATIC_FLAG in argv and constants.flags.STATIC_FLAG not in exclude:
        constants.CHOICE = constants.STATIC
        constants.TAKE_INPUT = False

        if constants.flags.NOSAVE_FLAG not in argv:
            with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                pref_file.write("static")

            with open(constants.STARTUP_FILE, "w+") as pref_file:
                pref_file.write("static")

    elif constants.flags.SLIDESHOW_FLAG in argv and constants.flags.SLIDESHOW_FLAG not in exclude:
        constants.CHOICE = constants.SLIDE_SHOW
        constants.TAKE_INPUT = False

        if constants.flags.NOSAVE_FLAG not in argv:
            with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                pref_file.write("slideshow")

            with open(constants.STARTUP_FILE, "w+") as pref_file:
                pref_file.write("slideshow")

    else:
        with open(constants.PREFERENCE_FILE, "r") as pref_file:
            choice = pref_file.readline()
            if choice in constants.CHOICES.keys():
                constants.TAKE_INPUT = False
                constants.CHOICE = constants.CHOICES[choice]


def reset(argv: list, verifyfiles=False) -> None:
    with open(constants.PREFERENCE_FILE, "w+") as pref_file:
        pref_file.write("")
    # shutil.rmtree(constants.DATA_PATH)

    with open(constants.STARTUP_FILE, "w+") as startup_file:
        startup_file.write("")

    with open(constants.STDOUT_LOG_FILE, "w+") as stdout_file:
        stdout_file.write("")

    with open(constants.STDERR_LOG_FILE, "w+") as stderr_file:
        stderr_file.write("")

    with open(constants.SCRIPT_PATH_FILE, "w+") as sp_file:
        sp_file.write(constants.CURRENT_DIRECTORY)
        constants.SCRIPT_DIRECTORY = constants.CURRENT_DIRECTORY

    if verifyfiles:
        config.fs.verify_files(argv)


def remove_files() -> None:
    shutil.rmtree(constants.IMAGES_PATH)

    if os.path.exists(constants.PREFERENCE_FILE):
        os.remove(constants.PREFERENCE_FILE)

    if os.path.exists(constants.SCRIPT_PATH_FILE):
        os.remove(constants.SCRIPT_PATH_FILE)

    if os.path.exists(constants.HISTORY_FILE):
        os.remove(constants.HISTORY_FILE)
