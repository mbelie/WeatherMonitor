import urllib.request
import json
import os

from sensor_result import SensorResult

class WeatherService:
    DEFAULT_LATITUDE = 33.28977940
    DEFAULT_LONGITUDE = -96.55522600
    WEATHER_API_METRICS = '&current=temperature_2m,relative_humidity_2m,surface_pressure&temperature_unit=fahrenheit'
    CURRENT_KEY = "current"
    TEMPERATURE_KEY = "temperature_2m"
    HUMIDITY_KEY = "relative_humidity_2m"
    PRESSURE_KEY = "surface_pressure"
    
    def __init__(self):
        self.WEATHER_API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={os.getenv('SITE_LATITUDE', self.DEFAULT_LATITUDE)}&longitude={os.getenv('SITE_LONGITUDE', self.DEFAULT_LONGITUDE)}{self.WEATHER_API_METRICS}"

    def fetch_conditions(self):
        try:
            with urllib.request.urlopen(self.WEATHER_API_URL) as response:
                jsonValue=response.read().decode()
                data = json.loads(jsonValue)

                temperature = float(data[f'{self.CURRENT_KEY}'][f'{self.TEMPERATURE_KEY}'])
                humidity = float(data[f'{self.CURRENT_KEY}'][f'{self.HUMIDITY_KEY}'])
                pressure = float(data[f'{self.CURRENT_KEY}'][f'{self.PRESSURE_KEY}'])
                return SensorResult(temperature=temperature, humidity=humidity, pressure=pressure, errorMessage=None)
        except Exception as error:
            return SensorResult(None, None, None, f"Error fetching weather data: {error}")