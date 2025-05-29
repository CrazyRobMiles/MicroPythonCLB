from managers.base import CLBManager
import machine
import neopixel
import time
import math
import random
import sys
from graphics.colours import find_random_colour,colour_name_lookup
from graphics.sprite import Sprite
from graphics.frame import Frame
from graphics.coord_map import CoordMap

class Manager(CLBManager):
    version = "1.0.0"
    dependencies = []

    STATE_DISABLED = "disabled"
    STATE_CONNECTING = "connecting"
    STATE_RUNNING = "running"
    STATE_ERROR = "error"

    def __init__(self):
        super().__init__(defaults={
            "pixelpin": 18,
            "panel_width": 8,
            "panel_height": 8,
            "x_panels": 3,
            "y_panels": 2,
            "brightness": 1.0,
            "pixeltype": "GRB"
        })
        self.pixels = None
        self.state = self.STATE_CONNECTING
        self.pixel_count = 0
        self.last_update = time.ticks_ms()
        self.anim_step = 0

    def setup(self, settings):

        super().setup(settings)

        if not self.enabled:
            self.state = self.STATE_DISABLED
            return

        try:
            pin_number = settings["pixelpin"]
            pin = machine.Pin(pin_number, machine.Pin.OUT)

            self.map = CoordMap(
                panel_width=self.settings["panel_width"],
                panel_height=self.settings["panel_height"],
                x_panels=self.settings["x_panels"],
                y_panels=self.settings["y_panels"])

            if self.map.pixels == 0:
                self.state = self.STATE_DISABLED
                self.set_status(4000, "No pixels configured")
                return

            self.pixels = neopixel.NeoPixel(pin, self.map.pixels)

            self.frame = Frame(width=self.map.width, height=self.map.height, show_fn=self.show, set_pixel_fn=self.set_pixel,coord_map_fn=self.map.get_offset)

            self.frame.background_manager.start_transitions(((20,0,0),(0,20,0),(0,0,20)),100)

            for i in range (30):
                sprite = Sprite(self.frame)
                sprite.x = random.randint(0, self.map.width)
                sprite.y = random.randint(0, self.map.height)
                sprite.setColour((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                sprite.brightness = 1.0
                sprite.opacity = 1.0
                sprite.enabled = True
                sprite.startWrap(random.uniform(-0.2,0.2), random.uniform(-0.2,0.2))
                self.frame.add_sprite(sprite)

            self.state = self.STATE_RUNNING
            self.set_status(4001, f"Pixel strip started with {self.map.pixels} pixels")

        except Exception as e:
            self.state = self.STATE_ERROR
            sys.print_exception(e)
            self.set_status(4002, f"Pixel init error: {e}")

    # Callbacks for the Leds system
    def show(self):
        self.pixels.write()

    def set_pixel(self,p, col):
        self.pixels[p]=col

    def update(self):
        
        if self.state != self.STATE_RUNNING:
            return

        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update) > 33:
            self.frame.update()
            self.frame.render()
            self.frame.display()
            self.last_update = now
        else:
            print("+")

    def teardown(self):
        if self.pixels:
            self.clear_pixels()
            self.pixels = None
            self.set_status(4012, "Pixel manager torn down")

    def get_commands(self):
        return [
            ("pixels-on", self.command_enable, "Enable pixel animation"),
            ("pixels-off", self.command_disable, "Disable pixel animation")
        ]

    def command_enable(self):
        self.enabled = True
        self.set_status(4010, "Pixels manually enabled")
        self.setup(self.settings)

    def command_disable(self):
        self.enabled = False
        self.set_status(4011, "Pixels manually disabled")
        self.state = self.STATE_DISABLED
