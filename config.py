# config/config.py
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Cities to monitor (Indian metros)
    CITIES: List[str] = [
        "Delhi", "Mumbai", "Chennai", 
        "Bangalore", "Kolkata", "Hyderabad"
    ]
    
    # Update interval in seconds (5 minutes)
    UPDATE_INTERVAL = 300
    
    # Temperature thresholds (in Celsius)
    TEMPERATURE_THRESHOLD = 35.0
    CONSECUTIVE_ALERTS = 2
    
    # Temperature unit preferences
    class TemperatureUnit:
        CELSIUS = "celsius"
        FAHRENHEIT = "fahrenheit"
        KELVIN = "kelvin"
    
    TEMP_UNIT = TemperatureUnit.CELSIUS
    
    # Database configuration
    DB_PATH = "weather_data.db"
    
    # Additional weather parameters to track
    EXTENDED_PARAMETERS = {
        "humidity": "percentage",
        "wind_speed": "m/s",
        "pressure": "hPa"
    }
    
    # Alert configuration
    ALERT_CONFIG = {
        "temperature": {
            "high": 35.0,
            "low": 10.0
        },
        "humidity": {
            "high": 80.0
        },
        "wind_speed": {
            "high": 20.0  # m/s
        }
    }