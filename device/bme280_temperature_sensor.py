import board
import adafruit_bme280

from sensor_result import SensorResult
from enums import TemperatureUnit

class Bme280TemperatureSensor:
    def __init__(self):
        self.i2c = board.I2C()
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

    def read(self):
        try:
            temperature = self.bme280.temperature
            humidity = self.bme280.humidity
            pressure = self.bme280.pressure

            print(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %, Pressure: {pressure:.2f} hPa")

            return SensorResult(temperature=float(temperature), humidity=float(humidity), pressure=float(pressure), 
                                temperatureUnit=TemperatureUnit.Celsius, errorMessage=None)
        
        except Exception as error:
            return SensorResult(errorMessage=f"Error reading temperature: {error}", isRecoverable=True, temperatureUnit=None)

    def dispose(self):
        pass
