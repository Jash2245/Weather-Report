# Weather-Report
This application is a real-time data processing system designed to monitor weather conditions across major Indian metros (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad) and provide insightful summaries using rollups and aggregates. It utilizes data from the OpenWeatherMap API (https://openweathermap.org/).

Features:

- Continuous retrieval of weather data from OpenWeatherMap API at configurable intervals
- Conversion of temperature values to Celsius (configurable)
  
Calculation of daily weather summaries:
- Average temperature
- Maximum temperature
- Minimum temperature
- Dominant weather condition

- Storage of daily summaries in a database or persistent storage
- User-configurable thresholds for temperature or weather conditions (e.g., temperature alerts)
- Alert triggering upon threshold breaches (implementation details open-ended)
- Visualization of daily summaries, historical trends, and triggered alerts (future implementation)

### Creating the Project Structure:

- Create a new directory named weather_monitoring.
- Create subdirectories within weather_monitoring as specified in the structure.
- Create empty Python files (__init__.py) in each directory to initialize modules.
- Start populating the files with the appropriate code based on the README.md and your implementation details.

### Sub Directories:
- **config/config.py:**

  Stores configuration settings like the OpenWeatherMap API key and other adjustable parameters.
- **src/api/weather_api.py:**

  Handles interaction with the OpenWeatherMap API, fetching weather data for the specified locations.
- **src/models/weather_data.py:**

  Defines data structures to represent weather data, including temperature, weather condition, and other relevant parameters.
- **src/processors/data_processor.py:**

  Contains the core logic for processing incoming weather data, calculating daily summaries, and triggering alerts.
- **src/utils/helpers.py:**

  Provides helper functions for tasks like temperature conversion and other common operations.
- **tests/test_weather.py:**

  Includes unit tests to verify the correctness of weather-related functionality.
- **.env:**

  Stores the OpenWeatherMap API key as an environment variable for security.
- **requirements.txt:**

  Lists the project's dependencies, making it easy to install them using pip install -r requirements.txt.
- **README.md:**

  Provides a detailed description of the project, its features, installation instructions, and usage guidelines.
- **main.py:**

  Serves as the application's entry point, initiating the data retrieval, processing, and alerting processes.
- **test_api.py:**

  (Optional) Contains unit tests specifically for API interaction, ensuring proper communication with the OpenWeatherMap API.

## Installation:

- Create a virtual environment to manage dependencies:

```bash
python -m venv venv
venv\Scripts\activate #windows
```

- Install dependencies:

```Bash
pip install -r requirements.txt
```

### Configure API key:
- Create a **.env** file in the project root directory and add this line, replacing **YOUR_API_KEY** with your actual **OpenWeatherMap API key**:
```
OPENWEATHERMAP_API_KEY=YOUR_API_KEY
```
### Usage:

- Start the application:

```Bash
python main.py
```
- (Optional) Run unit tests:

```Bash
python -m unittest tests
```

## Configuration:

- Adjust the weather data retrieval interval (currently configurable in config.py) to your desired frequency.
- Set user-defined thresholds for temperature and weather conditions in config.py.
- Configure database or persistent storage for daily summaries (future implementation).

## Notes:
- OpenWeatherMap API key is required and stored in a separate **.env file** for security.
- Alert implementation and visualization of summaries are planned for future development.
