import ctypes

SPI_SETDESKWALLPAPER = 20
SPI_GETDESKWALLPAPER = 115


def set_desktop_wallpaper(wallpaper_path) -> None:
    # Use user32.dll to set desktop wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 0)
