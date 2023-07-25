import getpass
import os
import constants.flags

USER_NAME = getpass.getuser()
CURRENT_DIRECTORY = os.getcwd()
DATA_PATH = r"C:\Users\%s\AppData\Local\DesktopSpotlight" % USER_NAME
STORE_PATH = os.path.join(DATA_PATH, "store")
SCRIPT_PATH_FILE = os.path.join(STORE_PATH, "script_path.txt")
SCRIPT_DIRECTORY = ""
SCRIPT_NAME = "desktop_spotlight.py"
SPOTLIGHT_ASSETS_PATH = r"C:\Users\%s\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets" % USER_NAME
IMAGES_PATH = os.path.join(DATA_PATH, "images")
LOGS_DIRECTORY = os.path.join(STORE_PATH, "logs")
PREFERENCE_FILE = os.path.join(STORE_PATH, "preference.txt")
STDOUT_LOG_FILE = os.path.join(LOGS_DIRECTORY, "stdout.log")
STDERR_LOG_FILE = os.path.join(LOGS_DIRECTORY, "stderr.log")
HISTORY_FILE = os.path.join(STORE_PATH, "history.txt")
STARTUP_FILE = os.path.join(STORE_PATH, "startup.txt")
SLIDE_SHOW = 1
STATIC = 2
SYNC = 3
CHOICES = {"sync": SYNC, "static": STATIC, "slideshow": SLIDE_SHOW}
CHOICE = SYNC
FLAGS = ["-r", "-f", "-clear", "-sync", "-slideshow", "-static"]
BAT_FILE_NAME = "open_ds.bat"
UPDATE_STARTUP_FILE = False
START_BY_BATCH = 100
START_BY_SCHEDULER = 101
STARTUP_WAY = None
UPDATE_SCHEDULER_TASK = False
TASK_NAME = "DesktopSpotlightStart"
TAKE_INPUT = True
