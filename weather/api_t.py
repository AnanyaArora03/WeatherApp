import logging
import os
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('api.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

CACHE_DIR = 'cache'
CACHE_EXPIRATION = timedelta(hours=1)  # Cache expiration time (1 hour)

class Api:
    def get_weather_data(self, city):
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
                logger.info(f"Successfully fetched weather data for {city}")
                return weather_data
            except requests.exceptions.Timeout:
                logger.error(f"Error: The API request timed out for {city}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logger.error(f"Error: API rate limit exceeded for {city}")
                else:
                    logger.error(f"Error: HTTP error occurred for {city}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error: Network error occurred for {city}")
            except KeyError:
                logger.error(f"Error: Invalid weather data format for {city}")
            except Exception as e:
                logger.error(f"An unexpected error occurred for {city}: {e}")
        else:
            logger.info(f"Using cached weather data for {city}")
            return weather_data

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
                logger.info(f"Using cached weather data for {city}")
                return cache_data['weather_data']
        except (IOError, ValueError) as e:
            logger.error(f"Error reading cache for {city}: {e}")
    
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
        logger.info(f"Saved cache for {city}")
    except IOError as e:
        logger.error(f"Error saving cache for {city}: {e}")
