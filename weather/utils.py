def extract_weather_info(weather_data):

 
    try:
        city = weather_data['name']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return city, temperature, description
    except KeyError as e:
        print(f"Error: Missing or unexpected data in API response - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return city, temperature, description
    
