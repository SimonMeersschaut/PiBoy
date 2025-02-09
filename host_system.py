# this script will find out if the script is running on windows (dev) or the raspberry pi
import platform

system_name = None

def get_system_version():
    global system_name
    system_name = platform.system()
    if system_name == 'Windows':
        print('Running on windows pc (dev mode).')
    elif system_name == 'Linux':
        print('Running on Linux pc.')
    else:
        print(f'Operating sytem {system_name} is not recognized')