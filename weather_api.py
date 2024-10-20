import requests
from typing import Dict, Any
from config.config import Config

class WeatherAPI:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self):
        self.api_key = Config.API_KEY
        
    def get_weather_data(self, city: str) -> Dict[str, Any]:
        """Fetch weather data for a specific city."""
        params = {
            'q': f"{city},IN",
            'appid': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()