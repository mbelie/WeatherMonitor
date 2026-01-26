class WeatherDataPublisher:
    def publish(self, weatherData: str):
        print(f"Publishing weather data: {weatherData}")
        #TODO: Send to SNS