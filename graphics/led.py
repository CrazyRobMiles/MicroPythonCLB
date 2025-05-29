from graphics.colours import BLACK,RED,GREEN,BLUE


class Leds:
    def __init__(self, width, height, show_fn, set_pixel_fn,coord_map_fn):
        self.width = width
        self.height = height
        self.norm_width = 1.0
        self.norm_height = height / width
        self.show = show_fn
        self.set_pixel = set_pixel_fn
        self.xy_to_index = coord_map_fn
        self.leds = [[[0,0,0] for _ in range(height)] for _ in range(width)]

    def clear(self, colour=BLACK):
        for y in range(self.height):
            for x in range(self.width):
                led=self.leds[x][y]
                for i in range(0,3):
                    led[i]= colour[i]

    def wash(self, colour):
        for y in range(self.height):
            for x in range(self.width):
                c = self.leds[x][y]
                if c[RED] == 0 and c[GREEN] == 0 and c[BLUE] == 0:
                    led=self.leds[x][y]
                    for i in range(0,3):
                        led[i]= colour[i]

    def display(self, brightness=1.0):
        i = 0
        for y in range(self.height):
            for x in range(self.width):
                c = self.leds[x][y]
                pos = self.xy_to_index(x, y)
                self.set_pixel(pos, (int(c[RED] * brightness), int(c[GREEN] * brightness), int(c[BLUE] * brightness)))
        self.show()

    def dump(self):
        print(f"Leds width: {self.width} height: {self.height}")
        for y in range(self.height):
            for x in range(self.width):
                c = self.leds[x][y]
                print(f"  r:{c[RED]} g:{c[GREEN]} b:{c[BLUE]}")

    def render_light(self, source_x, source_y, colour, brightness, opacity):
        int_x = int(source_x)
        int_y = int(source_y)
        led = self.leds[int_x][int_y]
        opacity = 1-opacity
        for i in range(0,3):
            led[i]=min(255,(led[i]*opacity) + (colour[i]*brightness))
        return

        for dx in [-1, 0, 1]:
            px = (int_x + dx) % self.width
            for dy in [-1, 0, 1]:
                py = (int_y + dy) % self.height
                dx2 = source_x - (px + 0.5)
                dy2 = source_y - (py + 0.5)
                dist2 = dx2 * dx2 + dy2 * dy2
                if dist2 < 1:
                    factor = 1 - dist2
                    r = colour.r * brightness * factor
                    g = colour.g * brightness * factor
                    b = colour.b * brightness * factor
                    self.leds[px][py].add_colour_values(r, g, b, opacity)
