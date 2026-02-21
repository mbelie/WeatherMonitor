from enums import TemperatureUnit

class SensorResult:
    """Data class for sensor reading results."""
    
    def __init__(self, 
                 temperature: float | None=None, 
                 temperatureUnit: TemperatureUnit | None=TemperatureUnit.Fahrenheit, 
                 humidity: float | None=None, 
                 pressure: float | None=None, 
                 errorMessage: str | None=None, 
                 isRecoverable: bool=True):
        self.temperature = temperature
        self.temperatureUnit = temperatureUnit
        self.humidity = humidity
        self.pressure = pressure
        self.errorMessage = errorMessage
        self.isRecoverable = isRecoverable

    def to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit."""
        if self.temperature is None:
            raise ValueError("Temperature is None, cannot convert")
        if self.temperatureUnit == TemperatureUnit.Fahrenheit:
            return self.temperature
        return self.temperature * 9.0 / 5.0 + 32.0

    def to_celsius(self) -> float:
        """Convert temperature to Celsius."""
        if self.temperature is None:
            raise ValueError("Temperature is None, cannot convert")
        if self.temperatureUnit == TemperatureUnit.Celsius:
            return self.temperature
        return (self.temperature - 32.0) * 5.0 / 9.0

    def __repr__(self) -> str:
        """Return string representation of SensorResult."""
        unit_str = self.temperatureUnit.name[0] if self.temperatureUnit else "?"
        return (f"SensorResult(temp={self.temperature}°{unit_str}, "
                f"humidity={self.humidity}%, pressure={self.pressure}, error={self.errorMessage})")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        if self.has_error:
            return f"Error: {self.errorMessage}"
        unit_str = self.temperatureUnit.name[0] if self.temperatureUnit else "?"
        return f"Temp: {self.temperature}°{unit_str}, Humidity: {self.humidity}%, Pressure: {self.pressure}"

    @property
    def has_error(self) -> bool:
        """Return True if result contains an error."""
        return self.errorMessage is not None