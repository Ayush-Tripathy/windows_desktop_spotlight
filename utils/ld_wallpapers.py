import os
import constants
import utils
import sys
import time
from utils import py_logger

log = py_logger.get_logger(__name__, "debug")


def start_slideshow(filtered_wallpapers: list) -> (str, None):
    """
    Starts a slideshow of all wallpapers with 10s gap
    """

    print("Starting a slideshow...")
    # Iterate through all images
    for idx, wallpaper in enumerate(filtered_wallpapers):
        # Set image to its absolute path
        wallpaper_to_set = os.path.abspath(wallpaper)

        utils.desktop_utils.set_desktop_wallpaper(wallpaper_to_set)
        print(f"current wallpaper - {wallpaper_to_set}")
        log.info(f"current wallpaper - {wallpaper_to_set}")

        # Exit if no more images left
        if idx == len(filtered_wallpapers) - 1:
            sys.exit(0)

        # Wait for 10 seconds
        time.sleep(10)


def set_static(filtered_wallpapers: list) -> (str, None):
    """
    Selects a wallpaper from all wallpapers a set it as desktop wallpaper

    Stores history of last set wallpaper and selects next one on the list
    """
    print("Setting a wallpaper...")
    wallpaper_idx = 0
    wallpaper_to_set = filtered_wallpapers[wallpaper_idx]

    # Check if history file exits in store directory
    # if exists read it content to decide which wallpaper to set
    if os.path.isfile(constants.STORE_PATH + "\\history.txt"):
        with open(constants.STORE_PATH + "\\history.txt", "r+") as store:
            w_list = []
            w_list_len = int(store.readline())

            for i in range(w_list_len):
                w_list.append(store.readline().split("\n")[0])

            prev_wallpaper = store.readline()
            if prev_wallpaper in w_list:
                wallpaper_idx = w_list.index(prev_wallpaper)

                if wallpaper_idx < len(w_list):
                    wallpaper_idx += 1
                if wallpaper_idx == len(w_list) - 1:
                    print("At end of list")
    try:
        wallpaper_to_set = filtered_wallpapers[wallpaper_idx]
    except IndexError:
        wallpaper_to_set = filtered_wallpapers[0]

    utils.desktop_utils.set_desktop_wallpaper(wallpaper_to_set)

    # Update contents of history file in store directory
    with open(constants.STORE_PATH + "\\history.txt", "w+") as store:
        cur_wallpaper_list_str = ""
        store.write(str(len(filtered_wallpapers)) + "\n")
        for fw in filtered_wallpapers:
            cur_wallpaper_list_str += (fw.split("\\")[-1] + "\n")
        store.write(cur_wallpaper_list_str)
        set_wallpaper = wallpaper_to_set.split("\\")[-1]
        store.write(set_wallpaper)

    print(f"current wallpaper - {wallpaper_to_set}")

    log.info(f"current wallpaper - {wallpaper_to_set}")
    return wallpaper_to_set


def sync(wallpapers: list) -> (str, None):
    """
    Set desktop wallpaper same as lockscreen wallpaper

    :parameter wallpapers: list of wallpapers
    """

    current_lockscreen_wallpaper_name = utils.get_lockscreen_wallpaper().split("\\")[-1]
    wallpaper_to_set = wallpapers[0]

    for idx, fw in enumerate(wallpapers):
        fw_n = fw.split("\\")[-1].rstrip(".jpg")
        if fw_n == current_lockscreen_wallpaper_name:
            wallpaper_to_set = fw

    utils.desktop_utils.set_desktop_wallpaper(wallpaper_to_set)
    print(f"current wallpaper - {wallpaper_to_set}")

    log.info(f"current wallpaper - {wallpaper_to_set}")
    return wallpaper_to_set
