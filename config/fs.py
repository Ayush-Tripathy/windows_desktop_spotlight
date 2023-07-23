import sys

import constants
import os


def verify_files(argv: list) -> bool:
    """
    UNDER WORK
    """
    print("Verifying....")
    # Create data directory if not present
    if not os.path.isdir(constants.DATA_PATH):
        os.mkdir(constants.DATA_PATH)

    # Create store directory if not present
    if not os.path.isdir(constants.STORE_PATH):
        os.mkdir(constants.STORE_PATH)

    # Create logs directory if not present
    if not os.path.isdir(constants.LOGS_DIRECTORY):
        os.mkdir(constants.LOGS_DIRECTORY)

    # Create images directory if not present
    if not os.path.isdir(constants.IMAGES_PATH):
        os.mkdir(constants.IMAGES_PATH)

    # Check if log files are present
    if not os.path.isfile(constants.STDOUT_LOG_FILE):
        with open(constants.STDOUT_LOG_FILE, "w+") as stdout_file:
            pass
    if not os.path.isfile(constants.STDERR_LOG_FILE):
        with open(constants.STDERR_LOG_FILE, "w+") as stderr_file:
            pass

    # Check if preference file exists
    if not os.path.isfile(constants.PREFERENCE_FILE):
        with open(constants.PREFERENCE_FILE, "w+") as preference_file:
            pass

    # Check if preference file exists
    if not os.path.isfile(constants.STARTUP_FILE):
        with open(constants.STARTUP_FILE, "w+") as startup_file:
            pass

    # Check if script path file exists in store directory
    if not os.path.isfile(constants.SCRIPT_PATH_FILE):
        with open(constants.SCRIPT_PATH_FILE, "w+") as sp_file:
            sp_file.write(constants.CURRENT_DIRECTORY)
            constants.SCRIPT_DIRECTORY = constants.CURRENT_DIRECTORY
    else:
        if "-r" in argv:
            with open(constants.SCRIPT_PATH_FILE, "w+") as sp_file:
                sp_file.write(constants.CURRENT_DIRECTORY)
                constants.SCRIPT_DIRECTORY = constants.CURRENT_DIRECTORY
        else:
            with open(constants.SCRIPT_PATH_FILE, "r") as sp_file:
                constants.SCRIPT_DIRECTORY = sp_file.readline()

    return True


def add_to_startup(argv, file_path, file_name="open_ds.bat", force=False):
    """
    Adds a batch file to windows startup folder.
    this batch file is used to run the script (desktop_spotlight.py)

    Creates a bat file to start the specified file at the
    windows startup path, the file is then called at everytime windows starts.

    :parameter file_path: path to the file to be added
    :parameter file_name: name of the .bat file to create
    :return None
    """
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % constants.USER_NAME
    if not force and os.path.isfile(bat_path + '\\' + file_name):
        return None
    with open(bat_path + '\\' + file_name, "w+") as bat_file:

        with open(constants.STARTUP_FILE, "r") as startup_file:
            choice = startup_file.readline()
            if choice in constants.CHOICES:
                if argv[0].split("/")[-1] == "desktop_spotlight.py":
                    content = f"@echo off\n" \
                              f"set \"flags=-{choice} {constants.flags.NOSAVE_FLAG}\"\n" \
                              f"{sys.executable} \"{os.path.join(constants.SCRIPT_DIRECTORY, 'desktop_spotlight.py')}\" %flags%"
                else:
                    content = f"@echo off\n" \
                            f"set \"flags=-{choice} {constants.flags.NOSAVE_FLAG}\"\n" \
                            f"start \"DesktopSpotlight\" \"{os.path.join(constants.SCRIPT_DIRECTORY, 'desktop_spotlight.exe')}\" %flags%"
            else:
                if argv[0].split("/")[-1] == "desktop_spotlight.py":
                    content = f"{sys.executable} \"{os.path.join(constants.SCRIPT_DIRECTORY, 'desktop_spotlight.py')}\""
                else:
                    content = f"start \"DesktopSpotlight\" \"{os.path.join(constants.SCRIPT_DIRECTORY, 'desktop_spotlight.exe')}\""
        bat_file.write(content)


def rm_from_startup(file_name="open_ds.bat") -> None:
    """
    Removes a batch file to windows startup folder.

    :parameter file_name: name of the .bat file to remove
    :return None
    """
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % constants.USER_NAME
    if os.path.isfile(bat_path + '\\' + file_name):
        os.remove(os.path.join(bat_path, file_name))
        return None
