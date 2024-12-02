from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_forecast(city, api_key, days):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        today = datetime.now()
        end_date = today + timedelta(days=days)
        for entry in data["list"]:
            forecast_date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
            if forecast_date.date() <= end_date.date():
                forecast = {
                    "date": forecast_date.strftime("%A, %B %d %Y, %I:%M %p"),
                    "temperature": entry["main"]["temp"],
                    "description": entry["weather"][0]["description"].lower()
                }
                forecast_data.append(forecast)
        return {"success": True, "forecast": forecast_data}
    else:
        return {"success": False, "error": response.json().get("message", "Unknown error")}

@app.route('/get_forecast', methods=['GET'])
def forecast_service():
    city = request.args.get('city')
    api_key = request.args.get('api_key')
    days = int(request.args.get('days', 3))
    if not city or not api_key:
        return jsonify({"success": False, "error": "Missing city or API key."}), 400
    return jsonify(get_forecast(city, api_key, days))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
