# main.py
import time
from datetime import datetime
import traceback
import schedule
from src.processors.data_processor import WeatherDataProcessor
from config.config import Config  # Add this import
from dotenv import load_dotenv   # Add this import

def update_weather(processor):
    """Function to update weather data with error handling"""
    try:
        print(f"\nFetching weather data at {datetime.now()}")
        weather_data = processor.fetch_current_weather()
        
        if not weather_data:
            print("No weather data received. Check your API key and internet connection.")
            return
            
        for data in weather_data:
            processor.process_weather_data(data)
            print(f"{data.city}: {data.temperature:.1f}°C, {data.weather_condition}")
        
        # Calculate and display daily summary for current date
        today = datetime.now().date()
        summary = processor.calculate_daily_summary(today)
        if summary:
            print("\nDaily Summary:")
            print(f"Average Temperature: {summary['avg_temperature']:.1f}°C")
            print(f"Max Temperature: {summary['max_temperature']:.1f}°C")
            print(f"Min Temperature: {summary['min_temperature']:.1f}°C")
            print(f"Dominant Weather: {summary['dominant_condition']} "
                  f"({summary['condition_frequency']} of the day)")
    except Exception as e:
        print(f"Error in update_weather: {str(e)}")
        print("Detailed error:")
        print(traceback.format_exc())

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if API key is configured
        if not Config.API_KEY:
            raise ValueError("API key is not configured. Please check your .env file.")
            
        processor = WeatherDataProcessor()
        
        # Schedule regular updates
        schedule.every(Config.UPDATE_INTERVAL).seconds.do(update_weather, processor)
        
        print("Weather monitoring system started...")
        print(f"Monitoring cities: {', '.join(Config.CITIES)}")
        print(f"Update interval: {Config.UPDATE_INTERVAL} seconds")
        
        # Initial update
        update_weather(processor)
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print("Detailed error:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()