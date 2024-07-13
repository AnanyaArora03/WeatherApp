def extract_weather_info(weather_data):
    city = weather_data['name']
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    return city, temperature, description
