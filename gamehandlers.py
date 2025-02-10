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
        

class ExeHandler(Handler):
    def __init__(self, handler_data: dict):
        '''Initialize the Game Handler with the handler_data data (from the manifest json file).'''
        self.handler_data = handler_data
        self.window = None # will be set on startup to the current open window
    
    def start(self):
        print('Starting exe file.')
        # Path to the exe file
        exe_path = "installed/tetris/Tetris.exe"
        exe_dir = os.path.dirname(exe_path)  # Extract directory
        
        if host_system.get_system_version() == 'Windows':
            command = exe_path
        elif host_system.get_system_version() == 'Linux':
            # On Raspberry pi, use the wine emulator
            command = ["wine", exe_path]
        else:
            raise RuntimeError('Host Operating System not recognized.')

        # Run the exe from its own directory
        self.process = subprocess.Popen(
            command,
            cwd=exe_dir,  # Set working directory
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture errors
            text=True  # Ensure text mode for output
        )
        print('Exe file succesfully started up!')

    def stop(self):
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
        keyboard.press(Key.up)
        time.sleep(.1)
        keyboard.release(Key.up)


HANDLERS = {
    'exe': ExeHandler
}

if __name__ == '__main__':
    test = ExeHandler({"filename": "gamedata/main.exe"})
    test.start()