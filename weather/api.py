import os
import json
from datetime import datetime, timedelta
import requests

CACHE_DIR = 'cache'
CACHE_EXPIRATION = timedelta(hours=1)  # Cache expiration time (1 hour)

def get_cached_weather_data(city):
    cache_file = os.path.join(CACHE_DIR, f"{city.lower()}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as file:
                cache_data = json.load(file)
            
            cache_time = datetime.strptime(cache_data['timestamp'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time < CACHE_EXPIRATION:
                print(f"Using cached weather data for {city}")
                return cache_data['weather_data']
        except (IOError, ValueError):
            pass
    
    return None

def save_to_cache(city, weather_data):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    cache_file = os.path.join(CACHE_DIR, f"{city.lower()}.json")
    cache_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'weather_data': weather_data
    }
    
    try:
        with open(cache_file, 'w') as file:
            json.dump(cache_data, file)
    except IOError:
        print(f"Error: Failed to save cache for {city}")

def get_weather_data(city):
    weather_data = get_cached_weather_data(city)
    if weather_data is None:
        try:
            api_key = os.getenv('WEATHER_API_KEY')
            base_url = os.getenv('WEATHER_API_BASE_URL')
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            save_to_cache(city, weather_data)
            return weather_data
        except Timeout:
            print("Error: The API request timed out. Please try again later.")
        except HTTPError as e:
            if e.response.status_code == 429:
                print("Error: API rate limit exceeded. Please try again later.")
            else:
                print(f"Error: HTTP error occurred - {e}")
        except RequestException as e:
            print(f"Error: Network error occurred - {e}")
        except KeyError:
            print("Error: Invalid weather data format")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        return weather_data
