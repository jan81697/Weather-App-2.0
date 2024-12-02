import requests

from datetime import datetime, timedelta

def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"  
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].lower()  # ALLY: ADDED .lower()
        }
        return weather
    else:
        return f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"



