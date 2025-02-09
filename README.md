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

## Hardware

The hardware will mostly be 3D printed and soldered. The GPIO pins of the raspberry will be connected to the connections of the buttons.