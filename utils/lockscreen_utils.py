import win32security
import winreg
import getpass
from utils import py_logger

err_log = py_logger.get_logger(__name__, "error")


def get_lockscreen_wallpaper() -> str:
    """
    Returns the path of the current lockscreen wallpaper
    """

    sid = win32security.LookupAccountName(None, getpass.getuser())[0]
    sid_str = win32security.ConvertSidToStringSid(sid)

    a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    a_key = winreg.OpenKey(a_reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Creative\%s' % sid_str)

    a_value_name, o_key, s_value = "", "", ""
    for i in range(1024):
        try:
            a_value_name = winreg.EnumKey(a_key, i)
            o_key = winreg.OpenKey(a_key, a_value_name)
            s_value = winreg.QueryValueEx(o_key, "landscapeImage")
        except EnvironmentError:
            print("ENV_ERR")
            err_log.error("Env error")

            break
    return s_value[0]
