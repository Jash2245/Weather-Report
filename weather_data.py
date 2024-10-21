from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherData:
    city: str
    temperature: float
    feels_like: float
    weather_condition: str
    timestamp: datetime

    @classmethod
    def from_api_response(cls, city: str, data: dict):
        return cls(
            city=city,
            temperature=data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
            feels_like=data['main']['feels_like'] - 273.15,
            weather_condition=data['weather'][0]['main'],
            timestamp=datetime.fromtimestamp(data['dt'])
        )