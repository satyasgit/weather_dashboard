from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

application = Flask(__name__)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not OPENWEATHER_API_KEY:
    logger.error("OpenWeather API key not found in environment variables")
    raise ValueError("OpenWeather API key is required")

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_weather_forecast(city):
    try:
        # Get coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        logger.debug(f"Calling Geocoding API for city: {city}")
        geo_response = requests.get(geo_url)
        
        if geo_response.status_code != 200:
            logger.error(f"Geocoding API error. Status: {geo_response.status_code}, Response: {geo_response.text}")
            return None, "Failed to get city coordinates. Please check the city name."
            
        geo_data = geo_response.json()
        
        if not geo_data:
            logger.warning(f"No geocoding data found for city: {city}")
            return None, "City not found. Please check the spelling or try a different city."
            
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        logger.debug(f"Got coordinates: lat={lat}, lon={lon}")
        
        # Get 7-day forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        logger.debug("Calling Weather API")
        response = requests.get(forecast_url)
        
        if response.status_code != 200:
            logger.error(f"Weather API error. Status: {response.status_code}, Response: {response.text}")
            return None, "Failed to fetch weather data. Please try again later."
            
        data = response.json()
        
        # Process forecast data
        forecasts = []
        seen_dates = set()
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            if date not in seen_dates and len(seen_dates) < 7:
                seen_dates.add(date)
                forecasts.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%A, %B %d'),
                    'temp': kelvin_to_celsius(item['main']['temp']),
                    'feels_like': kelvin_to_celsius(item['main']['feels_like']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon']
                })
        
        return {
            'city': geo_data[0]['name'],
            'country': geo_data[0]['country'],
            'forecasts': forecasts
        }, None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        return None, "Network error. Please check your internet connection."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None, "An unexpected error occurred. Please try again later."

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    logger.debug(f"Received request for city: {city}")
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
        
    weather_data, error_message = get_weather_forecast(city)
    
    if weather_data is None:
        return jsonify({'error': error_message or 'Unable to fetch weather data'}), 400
        
    return jsonify(weather_data)

if __name__ == '__main__':
    application.run(debug=True)
