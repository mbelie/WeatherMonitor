# LED Manager for controlling the Unicorn HAT LEDs
# The consuming program must be run with sudo in order for LEDs to function

import unicornhat as unicorn

class LedManager:
    def initialize(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        unicorn.clear()
        unicorn.show()

    def set_color(self, r, g, b):
        print(f"Setting LED color to R:{r} G:{g} B:{b}")
        width, height = unicorn.get_shape()
        for x in range(width):
            for y in range(height):
                unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()

