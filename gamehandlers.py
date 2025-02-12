from abc import ABC, abstractmethod
import subprocess
import time

from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

# Create keyboard and mouse controllers
keyboard = Controller()
mouse = MouseController()

def create_game_handler(manifest_data):
    handler = GAME_HANDLERS[manifest_data['GameHandler']](
        handler_data=manifest_data['GameHandlerData'],
        button_handler_data=manifest_data['ButtonHandlerData']
    )
    return handler

class GameHandler(ABC):
    '''Base class of a Game Handler Object'''

    @abstractmethod
    def __init__(self, handler_data:dict, button_handler=object):
        '''Initialize the Game Handler with the handler_data data (from the manifest json file).'''
        ...
    
    @abstractmethod
    def start(self):
        '''Start the game.'''
        ...
    
    @abstractmethod
    def stop(self):
        '''End the game.'''
        ...

    @abstractmethod
    def handle_button_event(self, event: dict):
        '''Read the IO pins and handle appropriatly (e.g. press keys)'''
        keyboard.press(Key.up)
        time.sleep(.1)
        keyboard.release(Key.up)
        

class CommandHandler(GameHandler):
    def __init__(self, handler_data: dict, button_handler: object):
        '''Initialize the Game Handler with the handler_data data (from the manifest json file).'''
        self.handler_data = handler_data
        self.window = None # will be set on startup to the current open window
        self.button_handler = button_handler
    
    def start(self):
        '''Start the game.'''
        print('Starting game.')
        # Run the exe from its own directory
        self.process = subprocess.Popen(
            self.handler_data['command'],
            # cwd=exe_dir,  # Set working directory
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture errors
            text=True,  # Ensure text mode for output
            shell=True # This is necessary for some games
        )
        print('Game succesfully started up!')

    def stop(self):
        '''End the game.'''
        # Read output in real time
        try:
            for line in self.process.stdout:
                print(line, end="")  # Print without adding extra newlines
        except KeyboardInterrupt:
            print("Stopping process")
            self.process.terminate()  # Terminate the process safely
            self.process.wait()  # Wait for it to fully stop
            print("Process stopped.")




GAME_HANDLERS = {
    # 'exe': ExeHandler,
    'command':CommandHandler
}

###################
# BUTTON HANDLERS #
###################

if __name__ == '__main__':
    # test = ExeHandler({"filename": "gamedata/main.exe"})
    # test.start()
    ...