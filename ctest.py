import time
import machine
import neopixel
import random

from graphics.colours import Colour,find_random_colour,colour_name_lookup
from graphics.sprite import Sprite
from graphics.frame import Frame

pixel_pin = machine.Pin(18, machine.Pin.OUT)
num_pixels = 24 * 16
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

from graphics.panel_map import PanelMap

map = PanelMap()

print(map.get_offset(0,0))

panel_width=8
panel_height=8

x_panels = 3
y_panels = 2
panel_row_pixels = (panel_width*panel_height)*x_panels

top_left = panel_row_pixels*(y_panels-1) + panel_height-1  

print(top_left)

pixels[top_left]= (0,20,0)

pixels.write()

def set_pixel(x, y, colour):
    """Set a pixel at (x, y) to the specified colour."""
    row_no = y//panel_height
    p = top_left - (row_no*panel_row_pixels)
    y = y - (row_no*panel_height)
    p=p+(panel_width*x)-y
    pixels[p] = colour

for x in range(0,16):
    p = map.get_offset(x,x)
    pixels[p]=(20,0,0)
pixels.write()  # Write the changes to the NeoPixel strip]
time.sleep(0.1)  # Delay to see the effect
