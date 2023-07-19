import os
import shutil
import constants
from PIL import Image as Img


def add_to_startup(file_path, file_name="open_ds.bat", force=False):
    """
    Function to add a batch file to windows startup folder.
    this batch file is used to run the script (desktop_spotlight.py)

    Creates a bat file to start the specified file at the
    windows startup path, the file is then called at everytime windows starts.

    @:parameter file_path: path to the file to be added
    @:parameter file_name: name of the .bat file to create
    @:return None
    """
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % constants.USER_NAME
    if not force and os.path.isfile(bat_path + '\\' + file_name):
        return None
    with open(bat_path + '\\' + file_name, "w+") as bat_file:
        content = f"python \"{file_path}\"\nexit"
        bat_file.write(content)


def verify_files(argv) -> bool:
    # Create data directory if not present
    if not os.path.isdir(constants.DATA_PATH):
        os.mkdir(constants.DATA_PATH)

    # Create store directory if not present
    if not os.path.isdir(constants.STORE_PATH):
        os.mkdir(constants.STORE_PATH)

    # Create images directory if not present
    if not os.path.isdir(constants.IMAGES_PATH):
        os.mkdir(constants.IMAGES_PATH)

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


def scan_wallpapers() -> list:
    # Get all filenames present in spotlight assets path
    spotlight_assets = os.listdir(constants.SPOTLIGHT_ASSETS_PATH)

    possible_wallpapers = []

    # Check for all possible wallpapers and add them to 'possible_wallpapers' list
    for asset in spotlight_assets:
        asset_size = os.path.getsize(constants.SPOTLIGHT_ASSETS_PATH + f"\\{asset}") / 1024
        if asset_size > 400:
            possible_wallpapers.append(constants.SPOTLIGHT_ASSETS_PATH + f"\\{asset}")

    print(f"Possible wallpapers found: {len(possible_wallpapers)}")

    return possible_wallpapers


def save_wallpapers(possible_wallpapers) -> list:
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

    return filtered_wallpapers