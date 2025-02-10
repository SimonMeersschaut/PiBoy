# PiBoy
## About

The PiBoy is a game console, inspired by the Nintendo GameBoy. The project aims to 
recreate the feeling of retro games, with modern technology. It seperates itself from
other projects like RetroPi as it will run any game, instead of a specific selection of games. This is necessary as the project will be used in a future game jam. For this reason, the possibility of quick updates on the games will be crucial.

## Software

The software shall start upon booting the Raspberry Pi. The startup procedure consists of four steps:
1) **Reading a USB**: check if a USB is present and, if so, copy the data from the USB onto the raspberry pi. This USB will be used to carry updates on games. The specific data-structure of that USB is yet to be decided.
2) **Show main menu**: Show a terminal-based user interface where the user can see exactle what the raspberry is doing on startup. After the startup is completed, the user can select a game to play.
3) **Start game**: When the user selected a game, the program will use the appropriate, game-specific steps to startup the game. This could be via an emulator or via a website.
4) **Button presses**: When buttons are pressed, it will be translated to keyboard presses.

### Instalation

1. **Clone git repository**: ```git clone github.com/SimonMeersschaut/PiBoy.git```
2. **Auto start script**: (source: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-3-systemd).
Create a new service file using ```sudo nano /lib/systemd/system/piboy.service```
and add the following content: 
```
[Unit]
Description=Start de Piboy User Interface
After=graphical.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/1000
ExecStart=/usr/bin/lxterminal --geometry=250x100 -e /usr/bin/python3 /home/pi/Desktop/PiBoy/main.py
WorkingDirectory=/home/pi/Desktop/PiBoy
User=pi
Group=pi
KillMode=process
TimeoutSec=infinity

[Install]
WantedBy=graphical.target
```
(lxterminal is used to open a visible terminal instead of running in the background. The geometry is set to open in fullscreen. Full paths are used as aliasses might not be resolved yet.)
After that, run 
```
sudo systemctl daemon-reload
sudo systemctl enable piboy.service
sudo systemctl start piboy.service
```

3. Install pynput using ```sudo apt install python-pynput```

4. Install wine using ```sudo apt install wine```

## Hardware

The hardware will mostly be 3D printed and soldered. The GPIO pins of the raspberry will be connected to the connections of the buttons.