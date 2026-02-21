import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request

from sensor_result import SensorResult

logger = logging.getLogger(__name__)

class WeatherService:
    """Fetches current weather conditions from Open-Meteo API."""
    
    DEFAULT_LATITUDE = 33.28977940
    DEFAULT_LONGITUDE = -96.55522600
    REQUEST_TIMEOUT = 10
    CURRENT_KEY = "current"
    TEMPERATURE_KEY = "temperature_2m"
    HUMIDITY_KEY = "relative_humidity_2m"
    PRESSURE_KEY = "surface_pressure"
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        """Initialize WeatherService with API URL and configuration."""
        latitude = os.getenv('SITE_LATITUDE', self.DEFAULT_LATITUDE)
        longitude = os.getenv('SITE_LONGITUDE', self.DEFAULT_LONGITUDE)
        
        # Build query parameters
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,surface_pressure',
            'temperature_unit': 'fahrenheit'
        }
        
        query_string = urllib.parse.urlencode(params)
        self.WEATHER_API_URL = f"{self.BASE_URL}?{query_string}"
        logger.debug(f"WeatherService initialized with URL: {self.WEATHER_API_URL}")

    def fetch_conditions(self) -> SensorResult:
        """Fetch current weather conditions from the API.
        
        Returns:
            SensorResult: Contains temperature, humidity, pressure, and any error message.
        """
        try:
            with urllib.request.urlopen(self.WEATHER_API_URL, timeout=self.REQUEST_TIMEOUT) as response:
                jsonValue=response.read().decode()
                data = json.loads(jsonValue)

                # Validate response structure
                if self.CURRENT_KEY not in data:
                    raise KeyError(f"Missing '{self.CURRENT_KEY}' key in API response")
                
                current = data[self.CURRENT_KEY]
                if not all(key in current for key in [self.TEMPERATURE_KEY, self.HUMIDITY_KEY, self.PRESSURE_KEY]):
                    raise KeyError("Missing required weather fields in API response")

                temperature = float(current[self.TEMPERATURE_KEY])
                humidity = float(current[self.HUMIDITY_KEY])
                pressure = float(current[self.PRESSURE_KEY])
                logger.info(f"Successfully fetched weather data: {temperature}°F, {humidity}% humidity, {pressure} mb")
                return SensorResult(temperature=temperature, humidity=humidity, pressure=pressure, errorMessage=None)
        except urllib.error.URLError as error:
            message = f"Network error fetching weather data: {error}"
            logger.error(message)
            return SensorResult(None, None, None, message)
        except json.JSONDecodeError as error:
            message = f"Invalid JSON response from weather API: {error}"
            logger.error(message)
            return SensorResult(None, None, None, message)
        except KeyError as error:
            message = f"Unexpected API response structure: {error}"
            logger.error(message)
            return SensorResult(None, None, None, message)
        except Exception as error:
            message = f"Unexpected error fetching weather data: {error}"
            logger.error(message)
            return SensorResult(None, None, None, message)