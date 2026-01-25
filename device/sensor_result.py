class SensorResult:
    def __init__(self, temperature_c=None, humidity=None, pressure=None, errorMessage=None, isRecoverable=True):
        self.temperature_c = temperature_c
        self.humidity = humidity
        self.pressure = pressure
        self.errorMessage = errorMessage
        self.isRecoverable = isRecoverable

    def to_fahrenheit(self):
        return self.temperature_c * 9.0 / 5.0 + 32.0