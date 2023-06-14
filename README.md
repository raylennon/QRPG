# QRPG - A QR-Code Powered Role-Playing Game
Framework for a simple RPG, hosted on a local waitress / flask backend

Includes several functionalities. Abilities are broken into python files - 

- `Scripts/graphics`: for creating and sending graphics arrays to the LED matrix, based on player position, overlays, etc.
- `Scripts/createqr`: dynamically generates a QR Code from a raspberry pi's IPv4 address, to display when game isn't running
- `Scripts/server`: for managing network requests, including from AJAX user interaction (motion controls)

This framework is intended to be highly scalable, allowing for:
- Multiple levels with walls, doors, portals
- NPC and environment interaction + UI overlays
- Cutscenes, optimized for a limited 64x32 LED panel


Getting started with QRPG is easy. Demo images (more in the works) are included so a working game comes out of the box. 

```bash
git clone https://github.com/raylennon/QRPG.git
sudo python3 QRCode/Scripts/main.py
```
Note that the [server script](https://github.com/raylennon/QRPG/blob/main/Scripts/server.py) assumes that you're using the [adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/2345), though this can be customized in the matrix options at the top of the file. 


<img src="https://i.ibb.co/4ZYXjK0/qrcode-big.png" height=160 width=320 />
