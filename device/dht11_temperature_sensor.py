import board
import adafruit_dht
import logging
from sensor_result import SensorResult
from enums import TemperatureUnit

logger = logging.getLogger(__name__)

class Dht11TemperatureSensor:
    """Reads temperature from DHT11 sensor."""
    
    SENSOR_PIN = board.D4
    
    def __init__(self):
        try:
            self.dht_device = adafruit_dht.DHT11(SENSOR_PIN)
            self.logger.info("DHT11 sensor initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize DHT11 sensor: {e}")
            raise

    def read(self) -> SensorResult:
        """Read sensor data and return SensorResult."""
        try:
            temperature_c = self.dht_device.temperature
            if temperature_c is None:
                return SensorResult(errorMessage="Failed to read temperature", isRecoverable=True, temperatureUnit=None)
            self.logger.info(f"Temperature: {temperature_c:.2f}°C")
            return SensorResult(temperature=float(temperature_c), temperatureUnit=TemperatureUnit.Celsius, errorMessage=None)
        except RuntimeError as error:
            return SensorResult(errorMessage=f"Runtime error reading temperature: {error}", isRecoverable=False, temperatureUnit=None)
        except Exception as error:
            return SensorResult(errorMessage=f"Error reading temperature: {error}", isRecoverable=True, temperatureUnit=None)

    def dispose(self) -> None:
        try:
            self.dht_device.exit()
        except Exception as e:
            self.logger.warning(f"Error disposing DHT11 sensor: {e}")
