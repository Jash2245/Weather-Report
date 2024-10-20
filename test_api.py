import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.api.weather_api import WeatherAPI
from src.models.weather_data import WeatherReading
from config.config import Config, City

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.api = WeatherAPI("test_api_key")
        self.test_city = City("TestCity", 12.9716, 77.5946)

    def test_kelvin_to_celsius(self):
        """Test temperature conversion from Kelvin to Celsius."""
        self.assertAlmostEqual(self.api.kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(self.api.kelvin_to_celsius(373.15), 100.0)

    def test_kelvin_to_fahrenheit(self):
        """Test temperature conversion from Kelvin to Fahrenheit."""
        self.assertAlmostEqual(self.api.kelvin_to_fahrenheit(273.15), 32.0)
        self.assertAlmostEqual(self.api.kelvin_to_fahrenheit(373.15), 212.0)

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        """Test successful weather data retrieval."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "weather": [{"main": "Clear"}],
            "main": {
                "temp": 300.15,  # 27°C
                "feels_like": 298.15,  # 25°C
                "humidity": 70
            },
            "wind": {"speed": 5.5},
            "dt": 1635789600  # Example timestamp
        }
        mock_get.return_value = mock_response

        # Test API call
        reading = self.api.get_weather(self.test_city)

        # Verify results
        self.assertIsInstance(reading, WeatherReading)
        self.assertEqual(reading.city, "TestCity")
        self.assertAlmostEqual(reading.temperature, 27.0, places=1)
        self.assertEqual(reading.condition, "Clear")
        self.assertEqual(reading.humidity, 70)
        self.assertEqual(reading.wind_speed, 5.5)

    @patch('requests.get')
    def test_get_weather_error(self, mock_get):
        """Test weather data retrieval with API error."""
        # Mock API error
        mock_get.side_effect = Exception("API Error")

        # Test API call with error
        with self.assertRaises(Exception):
            self.api.get_weather(self.test_city)

    def test_consecutive_readings(self):
        """Test processing of consecutive readings for alerts."""
        readings = [
            WeatherReading("TestCity", datetime.now(), 36.0, 38.0, "Clear", 65, 4.5),
            WeatherReading("TestCity", datetime.now(), 36.5, 39.0, "Clear", 63, 4.2),
            WeatherReading("TestCity", datetime.now(), 37.0, 40.0, "Clear", 60, 4.0)
        ]
        
        from src.processors.data_processor import WeatherDataProcessor
        processor = WeatherDataProcessor()
        
        # Process readings and check for alerts
        alerts = []
        for reading in readings:
            new_alerts = processor.process_reading(reading)
            alerts.extend(new_alerts)
        
        # Verify alerts were generated for high temperature
        self.assertTrue(any(alert.alert_type == 'high_temperature' for alert in alerts))

    def test_daily_summary(self):
        """Test daily summary calculation."""
        readings = [
            WeatherReading("TestCity", datetime.now(), 25.0, 26.0, "Clear", 65, 4.5),
            WeatherReading("TestCity", datetime.now(), 27.0, 28.0, "Clear", 63, 4.2),
            WeatherReading("TestCity", datetime.now(), 26.0, 27.0, "Cloudy", 64, 4.3)
        ]
        
        from src.processors.data_processor import WeatherDataProcessor
        processor = WeatherDataProcessor()
        
        summary = processor.calculate_daily_summary(readings)
        
        # Verify summary calculations
        self.assertEqual(summary.city, "TestCity")
        self.assertAlmostEqual(summary.avg_temp, 26.0)
        self.assertAlmostEqual(summary.max_temp, 27.0)
        self.assertAlmostEqual(summary.min_temp, 25.0)
        self.assertEqual(summary.dominant_condition, "Clear")

if __name__ == '__main__':
    unittest.main()