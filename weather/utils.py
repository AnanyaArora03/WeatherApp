import unittest
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('utils.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


def extract_weather_info(weather_data):
    try:
        city = weather_data['name']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        logger.info(f"Extracted weather information for {city}: {temperature}°C, {description}")
        return city, temperature, description
    except KeyError as e:
        logger.error(f"Error: Missing or unexpected data in API response - {e}")
        raise ValueError(f"Error: Missing or unexpected data in API response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")
  

class TestUtils(unittest.TestCase):
    def test_extract_weather_info(self):
        weather_data = {
            'name': 'London',
            'main': {'temp': 10},
            'weather': [{'description': 'Clouds'}]
        }
        
        expected_city = 'London'
        expected_temperature = 10
        expected_description = 'Clouds'
        
        # Call the function under test
        actual_city, actual_temperature, actual_description = extract_weather_info(weather_data)
        
        # Assert the result
        self.assertEqual(actual_city, expected_city)
        self.assertEqual(actual_temperature, expected_temperature)
        self.assertEqual(actual_description, expected_description)

if __name__ == '__main__':
    unittest.main()
    
