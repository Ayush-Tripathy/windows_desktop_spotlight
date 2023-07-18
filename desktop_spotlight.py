#!/usr/bin/env python

import os
import sys
import ctypes
import time
import shutil
import getpass
from PIL import Image as Img

USER_NAME = getpass.getuser()
CURRENT_DIRECTORY = os.getcwd()
DATA_PATH = r"C:\Users\%s\AppData\Local\DesktopSpotlight" % USER_NAME
STORE_PATH = os.path.join(DATA_PATH, "store")
SCRIPT_PATH_FILE = os.path.join(STORE_PATH, "script_path.txt")
SCRIPT_DIRECTORY = ""
SPOTLIGHT_ASSETS_PATH = r"C:\Users\%s\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets" % USER_NAME
IMAGES_PATH = os.path.join(DATA_PATH, "images")
SPI_SETDESKWALLPAPER = 20
SLIDE_SHOW = 1
STATIC = 2

# Choose what to apply i.e. slideshow (1) or latest image (2)
choice = STATIC

# Create data directory if not present
if not os.path.isdir(DATA_PATH):
    os.mkdir(DATA_PATH)

# Create store directory if not present
if not os.path.isdir(STORE_PATH):
    os.mkdir(STORE_PATH)

# Create images directory if not present
if not os.path.isdir(IMAGES_PATH):
    os.mkdir(IMAGES_PATH)

# Check if script path file exists in store directory
if not os.path.isfile(SCRIPT_PATH_FILE):
    with open(SCRIPT_PATH_FILE, "w+") as sp_file:
        sp_file.write(CURRENT_DIRECTORY)
        SCRIPT_DIRECTORY = CURRENT_DIRECTORY
else:
    with open(SCRIPT_PATH_FILE, "r") as sp_file:
        SCRIPT_DIRECTORY = sp_file.readline()

SCRIPT_PATH = os.path.join(SCRIPT_DIRECTORY, "desktop_spotlight.py")


def add_to_startup(file_path="", file_name="open_ds.bat"):
    """
    Function to add a file to windows startup folder.

    Creates a bat file to start the specified file at the
    windows startup path, the file is then called at everytime windows starts.

    @:parameter file_path: path to the file to be added\n
    @:parameter file_name: name of the .bat file to create\n
    @:return None
    """
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    if os.path.isfile(bat_path + '\\' + file_name):
        return None
    with open(bat_path + '\\' + file_name, "w+") as bat_file:
        content = f"python {file_path}\nexit"
        bat_file.write(content)


# Add this script to startup folder in windows
add_to_startup(SCRIPT_PATH, "open_ds.bat")

print("Current working directory:", os.getcwd())

# Get all filenames present in spotlight assets path
spotlight_assets = os.listdir(SPOTLIGHT_ASSETS_PATH)

possible_wallpapers = []
# Check for all possible wallpapers and add them to 'possible_wallpapers' list
for asset in spotlight_assets:
    asset_size = os.path.getsize(SPOTLIGHT_ASSETS_PATH + f"\\{asset}") / 1024
    if asset_size > 400:
        possible_wallpapers.append(SPOTLIGHT_ASSETS_PATH + f"\\{asset}")

print(f"Possible wallpapers found: {len(possible_wallpapers)}")

# Change current directory to 'images' directory
os.chdir(IMAGES_PATH)

wallpapers = []
# Copy all possible wallpapers to 'images' directory and append each image
# absolute path to 'wallpapers' list
for wallpaper in possible_wallpapers:
    shutil.copy2(wallpaper, IMAGES_PATH)
    wallpapers.append(IMAGES_PATH + wallpaper.split(SPOTLIGHT_ASSETS_PATH)[1])

# Convert all unidentified wallpapers into jpg format
# by renaming each wallpaper
for wallpaper in wallpapers:
    name = "\\".join(wallpaper.split("\\"))
    shutil.move(name, f"{name}.jpg")

# Get all file names from 'images' directory
images = os.listdir(os.getcwd())

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

if choice == SLIDE_SHOW:
    print("Starting a slideshow...")
    # Iterate through all images
    for idx, wallpaper in enumerate(filtered_wallpapers):
        # Set image to its absolute path
        wallpaper_to_set = os.path.abspath(wallpaper)

        # Use user32.dll to set desktop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_to_set, 0)
        print(f"current wallpaper - {wallpaper_to_set}")

        # Exit if no more images left
        if idx == len(filtered_wallpapers) - 1:
            sys.exit(0)

        # Wait for 10 seconds
        time.sleep(10)

elif choice == STATIC:
    print("Setting latest found wallpaper...")
    wallpaper_idx = 0
    wallpaper_to_set = filtered_wallpapers[wallpaper_idx]

    # Check if history file exits in store directory
    # if exists read it content to decide which wallpaper to set
    if os.path.isfile(STORE_PATH + "\\history.txt"):
        with open(STORE_PATH + "\\history.txt", "r+") as store:
            w_list = []
            w_list_len = int(store.readline())
            for i in range(w_list_len):
                w_list.append(store.readline().split("\n")[0])
            prev_wallpaper = store.readline()
            if prev_wallpaper in w_list:
                wallpaper_idx = w_list.index(prev_wallpaper)

                if wallpaper_idx < len(w_list) - 1:
                    wallpaper_idx += 1
                if wallpaper_idx == len(w_list) - 1:
                    print("At end of list")

    wallpaper_to_set = filtered_wallpapers[wallpaper_idx]

    # Use user32.dll to set desktop wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_to_set, 0)

    # Update contents of history file in store directory
    with open(STORE_PATH + "\\history.txt", "w+") as store:
        cur_wallpaper_list_str = ""
        store.write(str(len(filtered_wallpapers)) + "\n")
        for fw in filtered_wallpapers:
            cur_wallpaper_list_str += (fw.split("\\")[-1] + "\n")
        store.write(cur_wallpaper_list_str)
        set_wallpaper = wallpaper_to_set.split("\\")[-1]
        store.write(set_wallpaper)
    print(f"current wallpaper - {wallpaper_to_set}")
