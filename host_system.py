# this script will find out if the script is running on windows (dev) or the raspberry pi
import platform

def get_system_version():
    """Returns the current Operating System (Windows or Linux)."""
    return platform.system()