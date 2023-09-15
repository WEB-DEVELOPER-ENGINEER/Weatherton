# Weatherton

Welcome to the Weatherton, a Python Flask application that automatically detects local weather based on the user's external IP address.

## Table of Contents
- Setup
- Functionality
- Usage

## Setup
To get started with Weatherton, follow these steps:
1. Clone the repository
2. Add environment variables
 - secret_key="###"
 - weather_key="#####";. The weather_key is the API key received from registering at https://developer.accuweather.com/
3. Run the application: `python3 app.py`
4. Open a web browser and visit http://localhost:5000 to access the application.

### Or you can just visit the website: https://weatherton.pythonanywhere.com/
## Functionality
Weatherton provides the following functionality:
- Automatically detects the user's external IP address.
- Uses the IP address to retrieve location information using ip-api.com.
- Retrieves weather information, including the current temperature and precipitation probability, using the AccuWeather API.
- Displays the weather information along with an appropriate weather icon based on the current weather conditions. The app uses this library to get the weather icons: https://erikflowers.github.io/weather-icons/

## Usage
1. Visit the Weatherton web application in your browser.
2. Weatherton will automatically detect your location based on your IP address.
3. You will be redirected to a page displaying the current weather for your location, including temperature and a description of the weather conditions.
4. Depending on the weather conditions, you will see an appropriate weather icon to visually represent the current weather.
###Note that you can see the weather data for another city by changing the city and the countrycode in the url
