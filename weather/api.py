import os
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

def get_weather_data(city):
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
        return response.json()

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
