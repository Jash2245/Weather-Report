from typing import List, Dict
from collections import defaultdict, Counter
from datetime import datetime, date
from src.models.weather_data import WeatherData
from src.api.weather_api import WeatherAPI
from config.config import Config

class WeatherDataProcessor:
    def __init__(self):
        self.api = WeatherAPI()
        self.daily_data = defaultdict(list)  # Store data by date
        self.alert_counts = defaultdict(int)  # Track consecutive alerts
        
    def fetch_current_weather(self) -> List[WeatherData]:
        """Fetch weather data for all configured cities."""
        weather_data = []
        for city in Config.CITIES:
            try:
                raw_data = self.api.get_weather_data(city)
                weather_data.append(WeatherData.from_api_response(city, raw_data))
            except Exception as e:
                print(f"Error fetching data for {city}: {e}")
        return weather_data
    
    def process_weather_data(self, data: WeatherData):
        """Process incoming weather data and store for daily summaries."""
        current_date = data.timestamp.date()
        self.daily_data[current_date].append(data)
        self.check_alerts(data)
    
    def check_alerts(self, data: WeatherData):
        """Check if weather conditions trigger any alerts."""
        if data.temperature > Config.TEMPERATURE_THRESHOLD:
            self.alert_counts[data.city] += 1
            if self.alert_counts[data.city] >= Config.CONSECUTIVE_ALERTS:
                self.trigger_alert(data)
        else:
            self.alert_counts[data.city] = 0
    
    def trigger_alert(self, data: WeatherData):
        """Trigger an alert for extreme weather conditions."""
        alert_msg = (
            f"ALERT: High temperature detected in {data.city}!\n"
            f"Temperature: {data.temperature:.1f}°C\n"
            f"Condition: {data.weather_condition}\n"
            f"Time: {data.timestamp}"
        )
        print(alert_msg)
    
    def calculate_daily_summary(self, day: date) -> Dict:
        """Calculate daily weather summary for a specific date."""
        if day not in self.daily_data:
            return None
            
        day_data = self.daily_data[day]
        temperatures = [d.temperature for d in day_data]
        conditions = [d.weather_condition for d in day_data]
        
        # Calculate dominant weather condition using Counter
        condition_counts = Counter(conditions)
        dominant_condition = condition_counts.most_common(1)[0][0]
        total_conditions = len(conditions)
        
        return {
            'date': day,
            'avg_temperature': sum(temperatures) / len(temperatures),
            'max_temperature': max(temperatures),
            'min_temperature': min(temperatures),
            'dominant_condition': dominant_condition,
            'condition_frequency': f"{(condition_counts[dominant_condition] / total_conditions) * 100:.1f}%",
            'samples_count': len(day_data)
        }
