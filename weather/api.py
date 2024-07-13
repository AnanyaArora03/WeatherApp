import unittest
import os
import json
import requests
from datetime import datetime, timedelta
from api import Api, get_cached_weather_data

CACHE_DIR = 'cache'
CACHE_EXPIRATION = timedelta(hours=1)  # Cache expiration time (1 hour)

logging.basicConfig(level=logging.INFO, filename='api.log', format='%(asctime)s %(levelname)s: %(message)s')

class TestApi(unittest.TestCase):
    def setUp(self):
        self.api_key = 'your_api_key'
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'
        self.cache_dir = 'cache'
        self.cache_expiration = timedelta(hours=1)
        self.api = Api()

    def test_get_weather_data(self):
        city = 'London'
        expected_weather_data = {
            'name': 'London',
            'main': {'temp': 10},
            'weather': [{'description': 'Clouds'}]
        }
        response = requests.get(self.base_url, params={'q': city, 'appid': self.api_key, 'units': 'metric'})
        response.json = lambda: expected_weather_data
        actual_weather_data = self.api.get_weather_data(city)
        self.assertEqual(actual_weather_data, expected_weather_data)





    def test_get_cached_weather_data(self):
        city = 'London'
        expected_weather_data = {
            'name': 'London',
            'main': {'temp': 10},
            'weather': [{'description': 'Clouds'}]
        }
        
        # Mock the cache file
        cache_file = os.path.join(self.cache_dir, f"{city.lower()}.json")
        with open(cache_file, 'w') as file:
            json.dump({'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'weather_data': expected_weather_data}, file)
        
        # Call the function under test
        actual_weather_data = get_cached_weather_data(city)
        
        # Assert the result
        self.assertEqual(actual_weather_data, expected_weather_data)

def get_cached_weather_data(city):
    """
    Retrieve cached weather data for the given city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: The cached weather data, or None if the cache is not available or expired.
    """
    cache_file = os.path.join(CACHE_DIR, f"{city.lower()}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as file:
                cache_data = json.load(file)
            
            cache_time = datetime.strptime(cache_data['timestamp'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time < CACHE_EXPIRATION:
                logging.info(f"Using cached weather data for {city}")
                return cache_data['weather_data']
        except (IOError, ValueError) as e:
            logging.error(f"Error reading cache for {city}: {e}")
    
    return None

def save_to_cache(city, weather_data):
    """
    Save weather data to the cache for the given city.

    Args:
        city (str): The name of the city.
        weather_data (dict): The weather data to be cached.
    """
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
        logging.info(f"Saved cache for {city}")
    except IOError as e:
        logging.error(f"Error saving cache for {city}: {e}")

def get_weather_data(city):
    """
    Fetch weather data for the given city, using cached data if available.

    Args:
        city (str): The name of the city.

    Returns:
        dict: The weather data for the given city.
    """
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
            logging.info(f"Successfully fetched weather data for {city}")
            return weather_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {e}")
            raise e
        except Exception as e:
            logging.error(f"An unexpected error occurred for {city}: {e}")
            raise e
    else:
        return weather_data

if __name__ == '__main__':
    unittest.main() 
