import time
import machine
import neopixel
import random

from graphics.colours import colour_name_lookup
from graphics.sprite import Sprite
from graphics.frame import Frame

# Setup NeoPixel matrix (24×8 = 192 pixels), connected to GP18
pixel_pin = machine.Pin(18, machine.Pin.OUT)
num_pixels = 24 * 16
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# Callbacks for the Leds system
def show():
    pixels.write()

def set_pixel(p, r, g, b):
    pixels[p]=(int(r*255),int(g*255),int(b*255))

from graphics.coord_map import CoordMap

map = CoordMap()

# Create the Frame with callbacks
frame = Frame(width=map.width, height=map.height, show_fn=show, set_pixel_fn=set_pixel,coord_map_fn=map.get_offset)

# Create and configure a sprite
for i in range (30):
    sprite = Sprite(frame)
    sprite.x = random.randint(0, map.width)
    sprite.y = random.randint(0, map.height)
    sprite.setColour((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    sprite.brightness = 1.0
    sprite.opacity = 1.0
    sprite.enabled = True
    sprite.startWrap(random.uniform(-0.2,0.2), random.uniform(-0.2,0.2))
    frame.add_sprite(sprite)


# Run test at 30 FPS for 1 second
while True:
    frame.update()
    frame.render()
    frame.display()
#    time.sleep(1 / 30)
