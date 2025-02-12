import os
import json
import glob
import time
import host_system
import gamehandlers
from art import tprint


if host_system.get_system_version() == 'Linux':
    import RPi.GPIO as GPIO # module can not be imported in Windows



class UserInterface:
    def __init__(self):
        self.host_os = None

        # initialize GPIO pins
        if host_system.get_system_version() == 'Linux':
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
    
    def startup(self):
        self.clear()
        tprint('PiBoy')

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
        if host_system.get_system_version() == 'Windows':
            self.warn('Windows system -> skipping git update')
        else:
            self.log('Updating software')
            rc = os.system('git stash') # remove any edits to the code
            if rc == 0:
                # (Nothing to stash)
                self.log('Git ok')
            else:
                self.warn(f'Status code of git was: {rc}. Press Enter to continue.')
            rc = os.system('git pull')
            if rc == 0:
                # Up to date | 'Successfully rebased and updated ...'
                self.log('Git ok')
            else:
                self.warn(f'Status code of git was: {rc}. Press Enter to continue.')
                # TODO: restart script

        self.log('System checks done.')
        # Read USB
        # self.log('Checking USB...')
        # ...
        # self.log('USB (not) found.')

        time.sleep(2)
        # Show Main menu
        self.show_main_menu()

    def show_main_menu(self):
        '''This function shows a main menu and will run game-handlers.'''
        cursor = 1
        while True:
            cursor = max(1, min(cursor, len(list(self.get_installed_games())))) # 1 <= cursor <= len(...)
            # Print screen
            self.clear()
            tprint('PiBoy')
            for i, (_, name) in enumerate(self.get_installed_games()):
                if cursor == i+1:
                    print(f'>>{i+1}) {name}<<')
                else:
                    print(f'{i+1}) {name}')
            # Wait for GPIO interaction
            while True:
                if host_system.get_system_version() == 'Linux':
                    if GPIO.input(16) == GPIO.HIGH:
                        self.log("Starting game")
                        # Read manifest data and create a GameHandler
                        folder = list(self.get_installed_games())[cursor-1][0]
                        with open(folder+'/manifest.json', 'r') as f:
                            manifest_data = json.load(f)
                        self.clear()
                        tprint(manifest_data['name']) # print the game's title
                        self.handler = gamehandlers.create_game_handler(manifest_data)
                        # Start handler
                        self.handler.start()
                        # Handler mainloop
                        self.log('Starting game mainloop')
                        while self.handler.running:
                            self.handler.update() # read GPIO and press keys
                            # time.sleep(.05) # timout
                        self.log('Ended game mainloop')
                        break
                    # elif GPIO.input(16) == GPIO.HIGH:
                    #     cursor += 1
                    #     break # update screen
                    time.sleep(.2)
    
    def get_installed_games(self) -> list:
        folders = glob.glob('installed/*')
        for folder in folders:
            with open(folder+'/manifest.json', 'r') as f:
                data = json.load(f)
            yield (folder, data['name'])
    
if __name__ == '__main__':
    ui = UserInterface()
    ui.startup()