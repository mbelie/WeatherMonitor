from enums import TemperatureUnit

class SensorResult:
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

    def to_fahrenheit(self):
        return self.temperature * 9.0 / 5.0 + 32.0

    def to_celsius(self):
        return (self.temperature - 32.0) * 5.0 / 9.0