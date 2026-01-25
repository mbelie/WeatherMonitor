class WeatherDataPublisher:
    def publish(self, weatherData):
        print(f"Publishing weather data: {weatherData}")
        #TODO: Send to SNS