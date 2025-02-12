from abc import ABC, abstractmethod
import subprocess
import os
import time
import host_system

from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

# Create keyboard and mouse controllers
keyboard = Controller()
mouse = MouseController()

def create_game_handler(manifest_data):
    return HANDLERS[manifest_data['GameHandler']](manifest_data['HandlerData'])

class Handler(ABC):
    '''Base class of a Game Handler Object'''

    @abstractmethod
    def __init__(self, handler_data:dict):
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
    def update(self):
        '''Read the IO pins and handle appropriatly (e.g. press keys)'''
        ...
        

class CommandHandler(Handler):
    def __init__(self, handler_data: dict):
        '''Initialize the Game Handler with the handler_data data (from the manifest json file).'''
        self.handler_data = handler_data
        self.window = None # will be set on startup to the current open window
    
    def start(self):
        '''Start the game.'''
        print('Starting game.')
        # Run the exe from its own directory
        self.process = subprocess.Popen(
            self.handler_data['command'],
            # cwd=exe_dir,  # Set working directory
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture errors
            text=True  # Ensure text mode for output
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

    def update(self):
        '''Read the IO pins and handle appropriatly (e.g. press keys)'''
        keyboard.press(Key.up)
        time.sleep(.1)
        keyboard.release(Key.up)



HANDLERS = {
    # 'exe': ExeHandler,
    'command':CommandHandler
}

if __name__ == '__main__':
    # test = ExeHandler({"filename": "gamedata/main.exe"})
    # test.start()
    ...