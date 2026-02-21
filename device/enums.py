from enum import Enum

class TemperatureUnit(Enum):
    """Enumeration of supported temperature units."""
    Fahrenheit = 1
    Celsius = 2

    def to_string(self) -> str:
        return self.name