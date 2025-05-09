from managers.base import CLBManager
import machine
import neopixel
import time
import math
import graphics.colours
import graphics.sprite
import graphics.frame


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
            "numpixels_x": 12,
            "numpixels_y": 1,
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
            self.pixel_count = self.settings["numpixels_x"] * self.settings["numpixels_y"]
            if self.pixel_count == 0:
                self.state = self.STATE_DISABLED
                self.set_status(4000, "No pixels configured")
                return

            self.pixels = neopixel.NeoPixel(pin, self.pixel_count)
            self.clear_pixels()
            self.state = self.STATE_RUNNING
            self.set_status(4001, f"Pixel strip started with {self.pixel_count} pixels")

        except Exception as e:
            self.state = self.STATE_ERROR
            self.set_status(4002, f"Pixel init error: {e}")

    def clear_pixels(self):
        if self.pixels:
            for i in range(self.pixel_count):
                self.pixels[i] = (0, 0, 0)
            self.pixels.write()

    def update(self):
        if self.state != self.STATE_RUNNING:
            return

        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update) > 33:
            for i in range(self.pixel_count):
                r = int((math.sin(i + self.anim_step) + 1) * 127)
                g = int((math.sin(i + self.anim_step + 2) + 1) * 127)
                b = int((math.sin(i + self.anim_step + 4) + 1) * 127)
                self.pixels[i] = (r, g, b)
            self.pixels.write()
            self.anim_step += 2
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
        self.clear_pixels()
