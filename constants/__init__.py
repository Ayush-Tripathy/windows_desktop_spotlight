import getpass
import os

USER_NAME = getpass.getuser()
CURRENT_DIRECTORY = os.getcwd()
DATA_PATH = r"C:\Users\%s\AppData\Local\DesktopSpotlight" % USER_NAME
STORE_PATH = os.path.join(DATA_PATH, "store")
SCRIPT_PATH_FILE = os.path.join(STORE_PATH, "script_path.txt")
SCRIPT_DIRECTORY = ""
SCRIPT_NAME = "desktop_spotlight.py"
SPOTLIGHT_ASSETS_PATH = r"C:\Users\%s\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets" % USER_NAME
IMAGES_PATH = os.path.join(DATA_PATH, "images")
STDOUT_LOG_FILE = os.path.join(STORE_PATH, "stdout.log")
STDERR_LOG_FILE = os.path.join(STORE_PATH, "stderr.log")
SLIDE_SHOW = 1
STATIC = 2
SYNC = 3
