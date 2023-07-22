# import shutil
# import os
import os.path
import shutil
import sys
import config
import constants


def handle_flags(argv: list):
    if "-f" in argv:
        pass

    if "-clear" in argv:
        config.fs.rm_from_startup(constants.BAT_FILE_NAME)
        remove_files()
        print("Exit")
        sys.exit(0)

    if "-r" in argv:
        reset(argv, verify=True)

    if "-sync" in argv:
        constants.CHOICE = constants.SYNC
        with open(constants.PREFERENCE_FILE, "w+") as pref_file:
            pref_file.write("sync")

        with open(constants.STARTUP_FILE, "w+") as pref_file:
            pref_file.write("sync")
    elif "-static" in argv:
        constants.CHOICE = constants.STATIC
        with open(constants.PREFERENCE_FILE, "w+") as pref_file:
            pref_file.write("static")

        with open(constants.STARTUP_FILE, "w+") as pref_file:
            pref_file.write("static")
    elif "-slideshow" in argv:
        constants.CHOICE = constants.SLIDE_SHOW
        with open(constants.PREFERENCE_FILE, "w+") as pref_file:
            pref_file.write("slideshow")

        with open(constants.STARTUP_FILE, "w+") as pref_file:
            pref_file.write("slideshow")
    else:
        take_input = True
        with open(constants.PREFERENCE_FILE, "r") as pref_file:
            choice = pref_file.readline()
            if choice in constants.CHOICES.keys():
                take_input = False
                constants.CHOICE = constants.CHOICES[choice]

        if take_input:
            prompt_text = "Enter wallpaper mode [ sync | static | slideshow ]: "
            choice = input(prompt_text)

            if choice not in constants.CHOICES.keys():
                print("Invalid choice, terminating...")
                sys.exit(-2)
            constants.CHOICE = constants.CHOICES[choice]

            to_save = input("Save your choice? [y/n] : ")
            to_save_valid_inputs = ["y", "n", "yes", "no"]
            to_save = to_save.lower()

            approval = ["y", "yes"]

            if to_save in to_save_valid_inputs:
                if to_save in approval:
                    with open(constants.PREFERENCE_FILE, "w+") as pref_file:
                        pref_file.write(choice)

            else:
                print("Invalid input.")

            to_update_batch_file = input("Use this preference at windows startup? [y/n] : ")
            to_update_batch_file_valid_inputs = ["y", "n", "yes", "no"]
            to_update_batch_file = to_update_batch_file.lower()

            if to_update_batch_file in to_update_batch_file_valid_inputs:
                if to_update_batch_file in approval:
                    constants.UPDATE_BATCH_FILE = True
                    with open(constants.STARTUP_FILE, "w+") as pref_file:
                        pref_file.write(choice)
            else:
                print("Invalid input.")


def reset(argv: list, verify=False) -> None:
    with open(constants.PREFERENCE_FILE, "w+") as pref_file:
        pref_file.write("")
    # shutil.rmtree(constants.DATA_PATH)

    with open(constants.STDOUT_LOG_FILE, "w+") as stdout_file:
        stdout_file.write("")

    with open(constants.STDERR_LOG_FILE, "w+") as stderr_file:
        stderr_file.write("")

    with open(constants.SCRIPT_PATH_FILE, "w+") as sp_file:
        sp_file.write(constants.CURRENT_DIRECTORY)
        constants.SCRIPT_DIRECTORY = constants.CURRENT_DIRECTORY

    if verify:
        config.fs.verify_files(argv)


def remove_files() -> None:
    shutil.rmtree(constants.IMAGES_PATH)

    if os.path.exists(constants.PREFERENCE_FILE):
        os.remove(constants.PREFERENCE_FILE)

    if os.path.exists(constants.SCRIPT_PATH_FILE):
        os.remove(constants.SCRIPT_PATH_FILE)

    if os.path.exists(constants.HISTORY_FILE):
        os.remove(constants.HISTORY_FILE)
