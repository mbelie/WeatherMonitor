import board
import adafruit_bme280
import logging

from sensor_result import SensorResult
from enums import TemperatureUnit

logger = logging.getLogger(__name__)

SENSOR_ADDRESS = 0x76

class Bme280TemperatureSensor:
    """Reads temperature, humidity, and pressure from BME280 sensor via I2C."""
    
    def __init__(self):
        try:
            self.i2c = board.I2C()
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, address=SENSOR_ADDRESS)
        except Exception as e:
            logger.error(f"Failed to initialize BME280 sensor: {e}")
            raise

    def read(self) -> SensorResult:
        """Read sensor data and return SensorResult."""
        try:
            temperature = self.bme280.temperature
            humidity = self.bme280.humidity
            pressure = self.bme280.pressure

            logger.info(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %, Pressure: {pressure:.2f} hPa")

            return SensorResult(temperature=float(temperature), humidity=float(humidity), pressure=float(pressure), 
                                temperatureUnit=TemperatureUnit.Celsius, errorMessage=None)
        
        except Exception as error:
            return SensorResult(errorMessage=f"Error reading temperature: {error}", isRecoverable=True, temperatureUnit=None)

    def dispose(self):
        """Clean up I2C resources."""
        try:
            if hasattr(self, 'i2c') and self.i2c:
                self.i2c.deinit()
        except Exception as e:
            logger.warning(f"Error disposing I2C: {e}")
