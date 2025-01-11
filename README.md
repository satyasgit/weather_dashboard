# Weather Dashboard

A Flask-based weather dashboard application that displays 7-day weather forecasts for any city. Built for deployment on AWS Elastic Beanstalk.

## Features

- Search weather by city name
- 7-day weather forecast
- Displays temperature, feels like temperature, humidity, and weather conditions
- Responsive design
- Modern UI with animated cards

## Prerequisites

- Python 3.8+
- OpenWeatherMap API key
- AWS Elastic Beanstalk CLI (for deployment)

## Local Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenWeatherMap API key to `.env`

5. Run the application:
   ```bash
   python application.py
   ```

## AWS Elastic Beanstalk Deployment

1. Initialize Elastic Beanstalk application:
   ```bash
   eb init -p python-3.8 weather-dashboard --region us-west-2
   ```

2. Create an environment and deploy:
   ```bash
   eb create weather-dashboard-env
   ```

3. Set environment variables:
   ```bash
   eb setenv OPENWEATHER_API_KEY=your-api-key-here
   ```

## API Key Setup

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from your account
3. Add it to your `.env` file or AWS environment variables

## Technologies Used

- Flask
- Bootstrap 5
- OpenWeatherMap API
- AWS Elastic Beanstalk
