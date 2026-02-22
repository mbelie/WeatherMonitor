import logging
import os
import time
import struct

from bme280_temperature_sensor import Bme280TemperatureSensor
from enums import TemperatureUnit
from led_manager import LedManager
from sensor_result import SensorResult
from weather_data_publisher import WeatherDataPublisher
from weather_service import WeatherService
from datetime import datetime, timezone
from typing import Tuple

temperatureSensor = Bme280TemperatureSensor()
ledManager = LedManager()
weatherService = WeatherService()
weatherDataPublisher = WeatherDataPublisher()

logger = logging.getLogger(__name__)

HEX_COLORS = ["#0D47A1","#1976D2","#29B6F6","#4DD0E1","#80DEEA","#FFE082","#FFB74D","#FF8A65","#F4511E","#BF360C"]
COLORS = []

# Future use (multi-tenancy)
ACCOUNT_ID = "e0d5b845-35be-4c25-8b6d-0097664387e2"
DEVICE_ID = os.getenv("HOSTNAME")

# Validate required environment variables
if not DEVICE_ID:
    logger.warning("HOSTNAME environment variable not set. Device ID will be None.")


def setup_colors() -> None:
    for index in range(len(HEX_COLORS)):
        COLORS.append(hex_to_rgb(HEX_COLORS[index]))

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return struct.unpack('BBB', bytes.fromhex(hex_color))

def setup() -> None:
    setup_colors()
    ledManager.initialize()

def main() -> None:
    try:
        # setup()
        
        while True:
            sensorResult = temperatureSensor.read()

            if (sensorResult.errorMessage is None):
                logger.info(f"Read temperature: {sensorResult.temperature:.2f} F")
            else:
                # Fallback to weather service if sensor read fails
                # TODO: Consider circuit breaker pattern to avoid overwhelming the API with requests if sensor is consistently failing
                logger.warning(f"Error reading temperature sensor: {sensorResult.errorMessage}")
                sensorResult = weatherService.fetch_conditions()
                
            if sensorResult.errorMessage is None:
                logger.info("Processing sensor result...")

                temperature = sensorResult.temperature if sensorResult.temperatureUnit == TemperatureUnit.Fahrenheit else sensorResult.to_fahrenheit()
                
                # Map temperature to color: each 10°F increment corresponds to one color
                # Using / instead of // to handle negative temperatures correctly
                #color_index = max(0, min(int(temperature / 10), len(COLORS) - 1))
                #color = COLORS[color_index]
                #ledManager.set_color(color[0], color[1], color[2])

                payload = {
                    "device_id": DEVICE_ID,
                    "account_id": ACCOUNT_ID,
                    "temperature_f": temperature,
                    "humidity": sensorResult.humidity,
                    "pressure": sensorResult.pressure,
                    "timestamp": f"{datetime.now(timezone.utc).isoformat()}"
                }

                weatherDataPublisher.publish(payload)
            else:
                logger.error(f"Error: {sensorResult.errorMessage}")
                if not sensorResult.isRecoverable:
                    temperatureSensor.dispose()
                    raise SystemExit("Unrecoverable error encountered. Exiting.")

            logger.info(f"Sleeping {SLEEP_SECONDS}s...")
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        logger.info("\nExiting program...")
    finally:
        temperatureSensor.dispose()

if __name__ == "__main__":
    main()