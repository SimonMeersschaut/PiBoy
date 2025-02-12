import os
import json
import glob
import time
from host_system import get_system_version
# import gamehandlers
from button_handler import button_handler, EventType


if get_system_version() == 'Linux':
    import RPi.GPIO as GPIO # module can not be imported in Windows



class UserInterface:
    def __init__(self):
        self.host_os = None
        self.title = '''
 ___   _   ___              
| _ \ (_) | _ )  ___   _  _ 
|  _/ | | | _ \ / _ \ | || |
|_|   |_| |___/ \___/  \_, |
                        |__/ 
        '''
        button_handler.connect(self.button_handler)
        self.cursor = 1
        
        # initialize GPIO pins
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        
        button_pins = [16]
        for button_pin in button_pins:
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def clear(self):
        if self.host_os == 'windows':
            os.system('cls')
        elif self.host_os == 'Linux':
            os.system('clear')
        else:
            pass
    
    def log(self, msg):
        print(msg)
    
    def warn(self, msg):
        print(msg)
        input('Press enter to continue...')
        # TODO: add confirmation button (and optionally red text)
    
    def button_handler(self, pin: int, event_type:EventType):
        if event_type == EventType.RISING:
            # Update window
            self.cursor += 1
            self.print_main_menu()
        else:
            ...
    
    def startup(self):
        self.clear()
        self.log(self.title)

        # Perform system checks
        self.log('Running system checks...')
        self.host_os = host_system.get_system_version()
        if self.host_os == 'Windows':
            self.log('Running on windows pc (dev mode).')
        elif self.host_os == 'Linux':
            self.log('Running on Linux pc.')
        else:
            self.warn(f'Operating sytem {self.host_os} is not recognized')

        # Update software version
        self.log('Updating software')
        rc = os.system('git stash') # remove any edits to the code
        if rc == 0:
            self.log('Git ok')
        else:
            self.warn(f'Status code of git was: {rc}. Press Enter to continue.')
        rc = os.system('git pull')
        if rc == 0:
            self.log('Git ok')
        else:
            self.warn(f'Status code of git was: {rc}. Press Enter to continue.')

        self.log('System checks done.')
        # Read USB
        self.log('Checking USB...')
        ...
        self.log('USB (not) found.')

        # Show Main menu
        self.show_main_menu()

    def show_main_menu(self):
        cursor = 1
        while True:
            if GPIO.input(16) == GPIO.HIGH:
                cursor += 1
            os.system('cls')
            print(self.title)
            for i, (_, name) in enumerate(self.get_installed_games()):
                if self.cursor == i+1:
                    print(f'>>{i+1}) {name}<<')
                else:
                    print(f'{i+1}) {name}')
                # # TODO: replace by button interactions
                # resp = input('press enter to refresh')
                # if resp == 'run':
                #     self.log("Starting game")
                #     # Create new game handler
                #     folder = list(self.get_installed_games())[cursor-1][0]
                #     with open(folder+'/manifest.json', 'r') as f:
                #         manifest_data = json.load(f)
                #     self.handler = gamehandlers.create_game_handler(manifest_data)
                #     # Start handler
                #     self.handler.start()
    
    def get_installed_games(self) -> list:
        folders = glob.glob('installed/*')
        for folder in folders:
            with open(folder+'/manifest.json', 'r') as f:
                data = json.load(f)
            yield (folder, data['name'])
    
if __name__ == '__main__':
    ui = UserInterface()
    ui.startup()