import time
import machine
import neopixel
import random

from graphics.colours import find_random_colour,colour_name_lookup
from graphics.sprite import Sprite
from graphics.frame import Frame

WIDTH = 24
HEIGHT = 16

pixel_pin = machine.Pin(18, machine.Pin.OUT)
num_pixels = WIDTH * HEIGHT
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# Callbacks for the Leds system
def show():
    pixels.write()

def set_pixel(i, r, g, b):
    pixels[i] = (int(r*255), int(g*255), int(b*255))

# Create the Frame with callbacks
frame = Frame(width=WIDTH, height=HEIGHT, show_fn=show, set_pixel_fn=set_pixel)

sprite = Sprite(frame)
sprite.x = 2
sprite.y = 2
sprite.setColour((20,0,0))
sprite.brightness = 1.0
sprite.opacity = 1.0
sprite.enabled = True
sprite.startWrap(random.uniform(-0.2,0.2), random.uniform(-0.2,0.2))
frame.add_sprite(sprite)

frame.update()
frame.render()
frame.display()
