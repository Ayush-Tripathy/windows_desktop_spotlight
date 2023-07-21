import os
import shutil
import constants
from PIL import Image as Img
from utils import py_logger

log = py_logger.get_logger(__name__, "debug")


def add_to_startup(file_path, file_name="open_ds.bat", force=False):
    """
    Function to add a batch file to windows startup folder.
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
        content = f"python \"{file_path}\"\nexit"
        bat_file.write(content)


def scan_wallpapers() -> list:
    """
    Function to scan for wallpapers in the windows spotlight assets folder.

    It filters out the file that are above 400KB

    :return list: list of possible wallpaper paths
    """

    # Get all filenames present in spotlight assets path
    spotlight_assets = os.listdir(constants.SPOTLIGHT_ASSETS_PATH)

    possible_wallpapers = []

    # Check for all possible wallpapers and add them to 'possible_wallpapers' list
    for asset in spotlight_assets:
        asset_size = os.path.getsize(constants.SPOTLIGHT_ASSETS_PATH + f"\\{asset}") / 1024
        if asset_size > 400:
            possible_wallpapers.append(constants.SPOTLIGHT_ASSETS_PATH + f"\\{asset}")

    print(f"Possible wallpapers found: {len(possible_wallpapers)}")
    log.info(f"Possible wallpapers found: {len(possible_wallpapers)}")
    return possible_wallpapers


def save_wallpapers(possible_wallpapers: list) -> list:
    """
    Function to save wallpapers to data/images directory .

    :parameter possible_wallpapers: list of possible wallpapers to save from
    :return list: list of saved wallpaper paths with extension
    """

    wallpapers = []
    # Copy all possible wallpapers to 'images' directory and append each image
    # absolute path to 'wallpapers' list
    for wallpaper in possible_wallpapers:
        shutil.copy2(wallpaper, constants.IMAGES_PATH)
        wallpapers.append(constants.IMAGES_PATH + wallpaper.split(constants.SPOTLIGHT_ASSETS_PATH)[1])

    # Convert all unidentified wallpapers into jpg format
    # by renaming each wallpaper
    for wallpaper in wallpapers:
        name = "\\".join(wallpaper.split("\\"))
        shutil.move(name, f"{name}.jpg")

    return wallpapers


def filter_wallpapers(wallpapers: list) -> list:
    """
    Function to filter wallpapers that matches the required dimension.

    :parameter wallpapers: list of all wallpapers
    :return list: list of filtered wallpaper paths
    """

    # Filter wallpapers that have 1920*1080 dimension
    filtered_wallpapers = []
    for wallpaper in wallpapers:
        wallpaper = wallpaper + ".jpg"
        img = Img.open(wallpaper)
        width, height = img.size
        if width != 1920 or height != 1080:
            continue
        filtered_wallpapers.append(wallpaper)
    print(f"Filtered wallpapers count: {len(filtered_wallpapers)}")
    log.info(f"Filtered wallpapers count: {len(filtered_wallpapers)}")
    return filtered_wallpapers
