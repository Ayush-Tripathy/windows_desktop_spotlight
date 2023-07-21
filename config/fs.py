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
