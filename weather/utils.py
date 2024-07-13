import unittest
import logging

logging.basicConfig(level=logging.INFO, filename='utils.log', format='%(asctime)s %(levelname)s: %(message)s')

def extract_weather_info(weather_data):
    try:
        city = weather_data['name']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        logging.info(f"Extracted weather information for {city}: {temperature}°C, {description}")
        return city, temperature, description
    except KeyError as e:
        logging.error(f"Error: Missing or unexpected data in API response - {e}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e

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
    
