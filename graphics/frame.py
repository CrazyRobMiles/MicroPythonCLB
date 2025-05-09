from graphics.colours import Colour, BLACK
from graphics.sprite import Sprite
from graphics.led import Leds

class Frame:
    def __init__(self, width, height, show_fn, set_pixel_fn):
        self.width = width
        self.height = height
        self.leds = Leds(width, height, show_fn, set_pixel_fn)
        self.sprites = []

    def clear(self):
        self.leds.clear(BLACK)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def render(self):
        self.clear()
        for sprite in self.sprites:
            if sprite.enabled:
                self.leds.render_light(sprite.x, sprite.y, sprite.colour, sprite.brightness, sprite.opacity)

    def display(self, brightness=1.0):
        self.leds.display(brightness)

    def get_pixel_data(self):
        # Optional: flatten LED matrix if needed
        return [led.colour for row in self.leds.leds for led in row]
