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
Description=Start the Piboy User Interface
After=graphical.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/1000
ExecStart=/usr/bin/lxterminal --geometry=250x100 -e "cd ~/Desktop/PiBoy && source env/bin/activate && python3 main.py; bash"
WorkingDirectory=/home/pi/Desktop/PiBoy
User=pi
Group=pi
KillMode=process
TimeoutSec=infinity

[Install]
WantedBy=graphical.target
```
(lxterminal is used to open a visible terminal instead of running in the background. The geometry is set to open in fullscreen. Full paths are used as aliasses might not be resolved yet. 'bash' will make sure that the screen dus not close when an error occurs in the terminal (might not work).)
After that, run 
```
sudo systemctl daemon-reload
sudo systemctl enable piboy.service
sudo systemctl start piboy.service
```

3. Create venv `python3 -m venv env` and `source env/bin/activate`

<!-- 4. Install `pip install pynput`, `pip install art` and `pip install rpi-gpio`. -->

4. **Set key mapping**
edit `/boot/firmware/config.txt` and add these lines:

```
dtoverlay=gpio-key,gpio=26,keycode=103,label="Up"
gpio=26=pd
dtoverlay=gpio-key,gpio=19,keycode=106,label="Right"
gpio=19=pd
dtoverlay=gpio-key,gpio=13,keycode=108,label="Down"
gpio=13=pd
dtoverlay=gpio-key,gpio=5,keycode=105,label="Left"
gpio=5=pd
```

using `cat config.txt | sudo tee ~/../../boot/firmware/config.txt`
source: https://unix.stackexchange.com/questions/130656/how-to-get-all-my-keys-to-send-keycodes
![alt text](docs/Raspberry-Pi-5-Pinout--1210x642.jpg)

And reboot `sudo reboot`; test using `evtest`


`sudo apt install triggerhappy` voor repetitions

### Adding a game

(Nintendo games: https://www.emulatorgames.net/roms/nintendo-ds/new-super-mario-bros-psyfer/)
NintendoDS online emulator: gamesfrog.com/games/nds
GameBoy Advance emulator: https://gba.js.org/

The following section will explain how to add a Unity game to the raspberry pi.

1. **Build**: Build the game via `File > Build Settings > Linux x86_64`, then click Build.

2. **Convert C# to C++**: IL2CPP

3. **Cross-compile for aarch64 (ARM64)**: ...

( I dont know the rest, it never worked...)

### Example: Supertux2

install using `sudo apt install supertux` and run using
`~/../../usr/games/supertux2`.

## Hardware

The hardware will mostly be 3D printed and soldered. The GPIO pins of the raspberry will be connected to the connections of the buttons.

### Design

![Version1](https://github.com/user-attachments/assets/8de142db-0275-4dfa-b569-f32158f20b45)


### Screen

**Name**: Waveshare 4.3 inch LCD Capacitive Touch Display for Raspberry Pi 4B/3B+/3A+/3B/2B/B+/A+ 800×480 IPS Wide Angle MIPI DSI Interface Screen 

**Distributer**: Amazon

**Link**: https://www.amazon.com.be/-/en/dp/B083Q8YLVP?ref=ppx_yo2ov_dt_b_fed_asin_title

|  Type | Value |
|---|---|
| Brand |  Waveshare |
| Screen size  |  4.3 Inches |
| Resolution | SVGA  |
| Resolution | 800×480 |
| Aspect ratio  |  16:9 |
| Screen surface description  | Matte  |
| Refresh rate  | 60  |
| Power consumption  | 15 Watts  |
| Special feature  | Touchscreen  |
| Connectivity technology  |  DSI |
| Display type  | LCD  |

![Dimensions screen](docs/Dimensions_screen.png)

### Buttons

**Name**: 24pcs 16mm Assorted Red Green Yellow Blue White Black Momentary Push Button Switch 3A 250V AC 2 Pin Auto Reset Mini Round Switch

**Link**: https://www.amazon.com.be/-/en/gp/product/B09MBQSM44/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1

| Type | Value |
|------|-------|
| Operation mode | Automatic |
|Current rating |	3 Amps |
|Operating voltage |	250 Volts |
|Contact type |	Normally Open |
|Connector type |	2 Pin |
|Brand 	| Lewttyer |
|Switch type | 	push button, ignition switch |
|Terminal  |	brooches |
|Material |	Alloy Steel |
|Mounting type | Surface Mount |
| Diameter | 19 mm |

![Dimensions Buttons](docs/Dimensions_buttons.png)
