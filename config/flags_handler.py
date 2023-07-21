import constants


def handle_flags(argv):
    if "-f" in argv:
        pass

    if "-sync" in argv:
        constants.CHOICE = constants.SYNC
    elif "-static" in argv:
        constants.CHOICE = constants.STATIC
    elif "-slideshow" in argv:
        constants.CHOICE = constants.SLIDE_SHOW
    else:
        print("Specify a wallpaper mode by using '-sync' or '-static' or '-slideshow'")
        raise Exception("Invalid or no wallpaper mode specified")
