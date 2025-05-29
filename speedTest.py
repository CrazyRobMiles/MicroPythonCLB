import time
import machine
import neopixel
import random

WIDTH = 24
HEIGHT = 16
NUM_PIXELS = WIDTH * HEIGHT
pin = machine.Pin(18, machine.Pin.OUT)

pixels = neopixel.NeoPixel(pin, NUM_PIXELS)

neopixel.NeoPixel(pin, NUM_PIXELS)

def pixel_index(x, y):
    panel = x // 8
    x_in_panel = x % 8
    return panel * 64 + (y * 8) + x_in_panel

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        idx = pixel_index(x, y)
        pixels[idx] = color

# Fill entire screen random colors
def random_frame():
    for i in range(NUM_PIXELS):
        r=random.randint(0, 255)
        g=random.randint(0, 255)        
        b=random.randint(0, 255)
        pixels[i] = (0, 0, 0)

# Benchmark
frames = 100
start = time.ticks_ms()

for _ in range(frames):
    random_frame()
    pixels.write()

end = time.ticks_ms()

total_time = end - start
fps = frames / total_time

print(f"Total time: {total_time:.2f} seconds for {frames} frames")
print(f"Approx FPS: {fps:.2f}")

