import json
import os
import time
import struct

from device.led_manager import LedManager
from device.sensor_result import SensorResult
from device.temperature_sensor import TemperatureSensor
from device.weather__data_publisher import WeatherDataPublisher
from device.weather_service import WeatherService

temperatureSensor = TemperatureSensor()
ledManager = LedManager()
weatherService = WeatherService()
weatherDataPublisher = WeatherDataPublisher()

#  Old DHT11 sensors?
CALIBRATION_OFFSET_F = 35.0
SLEEP_SECONDS = 60

# Future use (multitenancy)
USER_ID = "e0d5b845-35be-4c25-8b6d-0097664387e2"
DEVICE_ID = os.getenv("HOSTNAME")

# Predefined colors for unicorn hat. It's a gradient that goes from blue (cold) to red (hot)
HEX_COLORS = ["#0D47A1","#1976D2","#29B6F6","#4DD0E1","#80DEEA","#FFE082","#FFB74D","#FF8A65","#F4511E","#BF360C"]
COLORS = []

def setup_colors():
    for value in range(len(HEX_COLORS)):
        COLORS.append(hex_to_rgb[value])

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return struct.unpack('BBB', bytes.fromhex(hex_color))

def setup():
    setup_colors()
    ledManager.initialize()
    temperatureSensor.initialize()

def main():
    try:
        setup()
        
        while True:
            temperature_f = 0.0
            sensorResult = temperatureSensor.read()

            if (sensorResult.errorMessage is None):
                temperature_f = sensorResult.to_fahrenheit()
            else:
                sensorResult = weatherService.fetch_conditions()
                temperature_f = sensorResult
    
            if sensorResult.errorMessage is None:
                print(f"Temperature: {temperature_f:.1f} F  Humidity: {sensorResult.humidity:.1f}%")

                color = COLORS[min(max(0, int(temperature_f // 10)), len(COLORS) - 1)]
                ledManager.set_color(color[0], color[1], color[2])

                payload = {
                    "device_id": DEVICE_ID,
                    "user_id": USER_ID,
                    "temperature_f": temperature_f,
                    "humidity": sensorResult.humidity,
                    "pressure": sensorResult.pressure,
                }

                weatherDataPublisher.publish(json.dumps(payload))
            else:
                
                print(f"Error: {sensorResult.errorMessage}")
                if not result.isRecoverable:
                    dht_device.exit()
                    raise SystemExit("Unrecoverable error encountered. Exiting.")

            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        temperatureSensor.dispose()

if __name__ == "__main__":
    main()
