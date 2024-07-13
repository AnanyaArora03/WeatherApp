import os
import requests

def get_weather_data(city):
    api_key = os.getenv('WEATHER_API_KEY')
    base_url = os.getenv('WEATHER_API_BASE_URL')
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()
