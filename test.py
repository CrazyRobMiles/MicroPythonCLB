import time
import machine
import neopixel
import random

from graphics.colours import Colour,find_random_colour,colour_name_lookup
from graphics.sprite import Sprite
from graphics.frame import Frame

# Setup NeoPixel matrix (24×8 = 192 pixels), connected to GP18
pixel_pin = machine.Pin(18, machine.Pin.OUT)
num_pixels = 24 * 8
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# Callbacks for the Leds system
def show():
    pixels.write()

def set_pixel(i, r, g, b):
    pixels[i] = (int(r*255), int(g*266), int(b*255))

# Create the Frame with callbacks
frame = Frame(width=24, height=8, show_fn=show, set_pixel_fn=set_pixel)

# Create and configure a sprite
for i in range (30):
    sprite = Sprite(frame)
    sprite.x = random.randint(0, 23)
    sprite.y = random.randint(0, 7)
    sprite.setColour(Colour(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)))
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
    time.sleep(1 / 30)
