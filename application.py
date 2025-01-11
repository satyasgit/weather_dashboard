from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your-api-key-here')

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_weather_forecast(city):
    try:
        # Get coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        logging.debug(f"Calling Geocoding API: {geo_url}")
        geo_response = requests.get(geo_url)
        logging.debug(f"Geocoding Response Status: {geo_response.status_code}")
        logging.debug(f"Geocoding Response: {geo_response.text}")
        geo_data = geo_response.json()
        
        if not geo_data:
            logging.warning("No geocoding data found for city")
            return None
            
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        
        # Get 7-day forecast
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch weather data. Status code: {response.status_code}")
            return None
            
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
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
        
        return {
            'city': geo_data[0]['name'],
            'country': geo_data[0]['country'],
            'forecasts': forecasts
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    logging.debug(f"Received request for city: {city}")
    
    if not city:
        return jsonify({'error': 'City is required'}), 400
        
    weather_data = get_weather_forecast(city)
    if weather_data is None:
        return jsonify({'error': 'Unable to fetch weather data for the specified city'}), 400
        
    return jsonify(weather_data)

if __name__ == '__main__':
    application.run(debug=True)
