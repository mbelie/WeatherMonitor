import logging
import random

from sensor_result import SensorResult
from enums import TemperatureUnit

logger = logging.getLogger(__name__)

class DummyTemperatureSensor:
    """Mock temperature sensor for testing purposes."""
    
    def __init__(self):
        pass

    def read(self) -> SensorResult:
        """Read sensor data and return SensorResult."""
        try:
            errorMessage = "Something bad happened"

            return SensorResult(temperatureUnit=TemperatureUnit.Celsius, errorMessage=errorMessage)
        
        except Exception as error:
            return SensorResult(errorMessage=f"Error reading temperature: {error}", isRecoverable=True, temperatureUnit=None)

    def dispose(self) -> None:
        """Clean up I2C resources."""
        try:
            if hasattr(self, 'i2c') and self.i2c:
                self.i2c.deinit()
        except Exception as e:
            logger.warning(f"Error disposing I2C: {e}")
