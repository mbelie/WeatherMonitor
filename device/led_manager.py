import unicornhat as unicorn
import logging

logger = logging.getLogger(__name__)

class LedManager:
    """Controls Unicorn HAT LEDs.
    
    Note: The consuming program must be run with sudo for LEDs to function properly.
    """

    DEFAULT_BRIGHTNESS = 0.5
    DEFAULT_ROTATION = 0
    MIN_RGB = 0
    MAX_RGB = 255

    def initialize(self) -> None:
        """Initialize the LED display."""
        try:
            unicorn.set_layout(unicorn.AUTO)
            unicorn.rotation(self.DEFAULT_ROTATION)
            unicorn.brightness(self.DEFAULT_BRIGHTNESS)
            unicorn.clear()
            unicorn.show()
        except Exception as e:
            logger.error(f"Failed to initialize Unicorn HAT: {e}")
            raise

    def set_color(self, r: int, g: int, b: int) -> None:
        """Set all LEDs to specified RGB color."""
        if not all(self.MIN_RGB <= val <= self.MAX_RGB for val in [r, g, b]):
            raise ValueError(f"RGB values must be {self.MIN_RGB}-{self.MAX_RGB}, got R:{r} G:{g} B:{b}")
        
        logger.info(f"Setting LED color to R:{r} G:{g} B:{b}")
        
        width, height = unicorn.get_shape()
        
        for x in range(width):
            for y in range(height):
                unicorn.set_pixel(x, y, r, g, b)
        
        unicorn.show()

    def turn_off(self) -> None:
        """Turn off all LEDs."""
        self.set_color(0, 0, 0)

    def dispose(self) -> None:
        """Clean up LED resources."""
        try:
            unicorn.clear()
            unicorn.show()
            logger.info("LED manager disposed")
        except Exception as e:
            logger.warning(f"Error disposing LEDs: {e}")

