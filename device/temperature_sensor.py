import board
import adafruit_dht
from sensor_result import SensorResult

class TemperatureSensor:
    def __init__(self):
        self.dht_device = adafruit_dht.DHT11(board.D4)

    def read(self):
        try:
            temperature_c = self.dht_device.temperature
            if temperature_c is None:
                return SensorResult(errorMessage="Failed to read temperature", isRecoverable=True)
            return SensorResult(temperature_c=temperature_c)
        except RuntimeError as error:
            return SensorResult(errorMessage=f"Runtime error reading temperature: {error}", isRecoverable=False)
        except Exception as error:
            return SensorResult(errorMessage=f"Error reading temperature: {error}", isRecoverable=True)
        
    def dispose(self):
        self.dht_device.exit()
