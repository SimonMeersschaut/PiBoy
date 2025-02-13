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
        try:
            with open('config.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.warn('No config json file found! Continuing with empty json data.')
            self.data = {}

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
        if host_system.get_system_version() == 'Linux':
            # Linux (Raspberry Pi)
            print('Press the OK button to continue')
            while GPIO.input(16) == GPIO.LOW:
                time.sleep(.1) # wait
        else:
            # Windows (dev)
            input('Press enter to continue...')
    
    def startup(self):
        self.clear()
        tprint('PiBoy')

        # Setup GPIO pins (Linux only)
        if host_system.get_system_version() == 'Linux':
            self.log('[GPIO] initializing...')
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            
            button_pins = [16, 20]
            for button_pin in button_pins:
                GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self.log('[GPIO] Done')
        else:
            self.log('[GPIO] skipped')

        # Perform system checks
        self.host_os = host_system.get_system_version()
        if self.host_os == 'Windows':
            self.log('[HOST] windows')
        elif self.host_os == 'Linux':
            self.log('[HOST] Linux')
        else:
            self.warn(f'[HOST] Operating sytem {self.host_os} is not recognized!')

        # Update software version
        self.log('[VERSION] Starting version control')
        if host_system.get_system_version() == 'Windows':
            self.log('[VERSION] skipping git update (windows host)')
        else:
            self.log('[VERSION] Updating software')
            rc = os.system('git stash') # remove any edits to the code
            if rc == 0:
                # (Nothing to stash)
                pass
            else:
                self.warn(f'[VERSION] Status code: {rc}!')
            rc = os.system('git pull')
            if rc == 0:
                # Up to date | 'Successfully rebased and updated ...'
                pass
            else:
                self.warn(f'[VERSION] Status code: {rc}!')

        # Read USB
        # self.log('Checking USB...')
        # ...
        # self.log('USB (not) found.')

        time.sleep(2)
        # check for auto-start
        try:
            if self.data['auto-start']['enabled']:
                # do auto start
                self.log('auto starting '+self.data['auto-start']['folder'])
                self.run_game(self.data['auto-start']['folder'])
        except KeyError:
            self.warn('KeyError during reading auto-start config!')
        # Show Main menu
        self.show_main_menu()
    
    def run_game(self, folder_name):
        '''
        Start the game and handle button presses.
        This function ends only if the game quits.
        '''
        self.log("Starting game")
        # Read manifest data and create a GameHandler
        try:
            with open(folder_name+'/manifest.json', 'r') as f:
                manifest_data = json.load(f)
        except FileNotFoundError:
            self.warn('The wanted game was not found!')
            return
        self.clear()
        tprint(manifest_data['name']) # print the game's title
        try:
            self.handler = gamehandlers.create_game_handler(manifest_data)
        except Exception as e:
            self.warn('Unexpected error: '+e.__repr__())
            return
        # Start handler
        self.handler.start()
        # Handler mainloop
        self.log('Starting game mainloop')
        while self.handler.running:
            self.handler.update() # read GPIO and press keys
            # time.sleep(.05) # timout
        self.log('Ended game mainloop')

    def show_main_menu(self):
        '''This function shows a main menu and will run game-handlers.'''
        cursor = 1
        while True:
            # Set cursor bounds: 1 <= cursor <= len(...)
            if cursor > len(list(self.get_installed_games())):
                cursor = 1
            elif cursor < 1:
                cursor = len(list(self.get_installed_games()))
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
                        folder_name = list(self.get_installed_games())[cursor-1][0]
                        self.run_game(folder_name) # blocking 
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