# this script will find out if the script is running on windows (dev) or the raspberry pi
import platform

def get_system_version():
    return platform.system()