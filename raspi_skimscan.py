# file: raspi_skimscan.py
# auth: Tyler Winegarner (twinegarner@gmail.com)
# desc: scans for local bluetooth devices with names matching the description of those
#       used in cas pump credit card skimmers. This software is directly derived from 
#       the research done by Nathan Seidle as documented in this article:
#       https://learn.sparkfun.com/tutorials/gas-pump-skimmers
#

import time
import bluetooth
import sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = None # I2C

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

time.sleep(3)

disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
ellipsis = ".   "
phase = 0
found = 0

while True:
    print("scanning" + ellipsis)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 24), "scanning" + ellipsis, font=font, fill=255)
    draw.text((0, 36), str(found) + " BT found", font=font, fill=255)
    disp.image(image)
    disp.display()

    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

    found = len(nearby_devices)
    print("found %d devices" % found)

    for addr, name in nearby_devices:
        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((0, 12), "Potential skimmer", font=font, fill=255)
            draw.text((0, 24), name + " found.", font=font, fill=255)
            draw.text((0, 36), "Skip this pump.", font=font, fill=255)

            disp.image(image)
            disp.display()
            time.sleep(5)

    phase += 1
    if phase == 1:
        ellipsis = "..  "
    elif phase == 2:
        ellipsis = "... "
    elif phase == 3:
        ellipsis = "...."
    else:
        ellipsis = ".   "
        phase = 0

