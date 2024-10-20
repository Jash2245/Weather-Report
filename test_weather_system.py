# tests/test_weather_system.py
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from src.models.weather_data import WeatherData
from src.processors.data_processor import WeatherDataProcessor
from src.database.weather_db import WeatherDatabase
from config.config import Config

class TestWeatherSystem(unittest.TestCase):
    def setUp(self):
        self.processor = WeatherDataProcessor()
        self.mock_api_response = {
            'main': {
                'temp': 308.15,  # 35°C
                'feels_like': 310.15,  # 37°C
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [{'main': 'Clear'}],
            'wind': {'speed': 5.5},
            'dt': int(datetime.now().timestamp())
        }

    def test_temperature_conversion(self):
        """Test temperature conversion from Kelvin to preferred unit."""
        data = WeatherData.from_api_response('Delhi', self.mock_api_response)
        self.assertAlmostEqual(data.temperature, 35.0, places=1)
        
        # Test Fahrenheit conversion
        Config.TEMP_UNIT = Config.TemperatureUnit.FAHRENHEIT
        data = WeatherData.from_api_response('Delhi', self.mock_api_response)
        self.assertAlmostEqual(data.temperature, 95.0, places=1)
        
        # Reset to Celsius
        Config.TEMP_UNIT = Config.TemperatureUnit.CELSIUS

    @patch('src.api.weather_api.WeatherAPI.get_weather_data')
    def test_data_retrieval(self, mock_get_weather):
        """Test weather data retrieval and processing."""
        mock_get_weather.return_value = self.mock_api_response
        weather_data = self.processor.fetch_current_weather()
        
        self.assertTrue(len(weather_data) > 0)
        self.assertIsInstance(weather_data[0], WeatherData)
        self.assertEqual(weather_data[0].weather_condition, 'Clear')

    def test_alert_threshold(self):
        """Test alert triggering for threshold violations."""
        # Create test data exceeding temperature threshold
        test_data = WeatherData(
            city='Delhi',
            temperature=36.0,
            feels_like=38.0,
            weather_condition='Clear',
            timestamp=datetime.now(),
            humidity=65,
            wind_speed=5.5,
            pressure=1013
        )
        
        # Process data twice to trigger consecutive alert
        self.processor.process_weather_data(test_data)
        self.processor.process_weather_data(test_data)
        
        self.assertEqual(self.processor.alert_counts['Delhi'], 2)

    def test_daily_summary(self):
        """Test daily summary calculation."""
        test_date = datetime.now().date()
        test_data = [
            WeatherData(
                city='Delhi',
                temperature=temp,
                feels_like=temp + 2,
                weather_condition='Clear',
                timestamp=datetime.now(),
                humidity=65,
                wind_speed=5.5,
                pressure=1013
            )
            for temp in [32.0, 34.0, 36.0]
        ]
        
        for data in test_data:
            self.processor.process_weather_data(data)
        
        summary = self.processor.calculate_daily_summary(test_date)
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['samples_count'], 3)
        self.assertAlmostEqual(summary['avg_temperature'], 34.0)
        self.assertEqual(summary['max_temperature'], 36.0)
        self.assertEqual(summary['min_temperature'], 32.0)
        self.assertEqual(summary['dominant_condition'], 'Clear')

if __name__ == '__main__':
    unittest.main()