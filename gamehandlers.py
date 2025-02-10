from abc import ABC, abstractmethod
import subprocess
import os
from pywinauto import Application
import random

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
    
    def start(self):
        print('Starting exe file.')
        # Path to the exe file
        exe_path = "installed/tetris/Tetris.exe"
        exe_dir = os.path.dirname(exe_path)  # Extract directory

        # Run the exe from its own directory
        self.process = subprocess.Popen(
            exe_path,
            cwd=exe_dir,  # Set working directory
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture errors
            text=True  # Ensure text mode for output
        )
        # Get the active window
        # Attach to the running application
        app = Application().connect(process=self.process.pid)  # Attach by PID
        self.window = app.top_window()  # Get the main window
        print('Exe file succesfully started up!')

    def stop(self):
        # Read output in real time
        # try:
        #     for line in process.stdout:
        #         print(line, end="")  # Print without adding extra newlines
        # except KeyboardInterrupt:
        #     print("\nStopping process...")
        #     process.terminate()  # Terminate the process safely
        #     process.wait()  # Wait for it to fully stop
        pass

    def update(self):
        self.window.wrapper_object().move_mouse_input(coords=(random.randint(0, 1920), random.randint(0, 1080)))


HANDLERS = {
    'exe': ExeHandler
}

if __name__ == '__main__':
    test = ExeHandler({"filename": "gamedata/main.exe"})
    test.start()