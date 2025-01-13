# Weather Dashboard

A Flask-based weather dashboard application that provides 7-day weather forecasts using the OpenWeatherMap API.

## Features

- City-based weather search
- 7-day weather forecast
- Temperature in Celsius
- Humidity information
- Weather conditions with icons
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/satyasgit/weather_dashboard.git
cd weather_dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your OpenWeather API key:
```
OPENWEATHER_API_KEY=your_api_key_here
```

5. Run the application:
```bash
flask run
```

## Technologies Used

- Flask
- OpenWeatherMap API
- Bootstrap
- JavaScript
- HTML/CSS

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
