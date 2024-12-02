from flask import Flask, render_template, request, redirect, url_for
import requests
import weather

app = Flask(__name__)

API_KEY = 'c613f5fe08ec7f312fc6f6e3e1de2f8e'

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        if request.form.get('userLocation') == 'userLocation':
            return redirect(url_for('ipSafety'))
        else:
            city = request.form.get('city')
            return weather_page(city)
    return render_template('location.html')

@app.route('/ipSafety', methods=['GET', 'POST'])
def ipSafety():
    if request.method == 'POST':
        consent = request.form.get('approved')
        try:
            response = requests.post(
                'http://127.0.0.1:5003/ipSafety',
                json={"approved": consent}
            )
            if response.status_code == 200:
                consent_data = response.json()
                if consent_data.get("consent") == "yes":
                    city_response = requests.get('http://127.0.0.1:5002/get_userCity')
                    if city_response.status_code == 200:
                        city_data = city_response.json()
                        if city_data.get("success"):
                            city = city_data.get("city")
                            return weather_page(city)
                        else:
                            error_message = city_data.get("error", "Failed to determine your location.")
                    else:
                        error_message = "Error communicating with location service."
                else:
                    error_message = "User declined consent."
            else:
                error_message = f"Microservice error: {response.status_code}"
        except Exception as e:
            error_message = f"An error occurred: {e}"
        return render_template('ipSafety.html', error=error_message)
    return render_template('ipSafety.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather_page(city=None):
    weather_data = None
    weather_image = None  # Variable for storing image URL
    if city:
        weather_data = weather.get_weather(city, API_KEY)
        if isinstance(weather_data, dict):
            # Call the image microservice if weather data is available
            response = requests.get('http://127.0.0.1:5001/get_image', params={'description': weather_data["description"]})
            if response.status_code == 200:
                weather_image = response.json().get('image_url')

    return render_template('index.html', weather_data=weather_data, weather_image=weather_image)


@app.route('/Expect_Weather', methods=['GET', 'POST'])
def expected_weather():
    city = request.args.get('city')
    days = request.args.get('days', 1)
    if city:
        try:
            forecast_response = requests.get(
                f'http://127.0.0.1:5004/get_forecast?city={city}&api_key={API_KEY}&days={days}'
            )
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json().get('forecast', [])
                return render_template('expected.html', forecast_data=forecast_data, city=city)
            else:
                error_message = f"Error fetching forecast: {forecast_response.status_code}"
        except Exception as e:
            error_message = f"An error occurred: {e}"
        return render_template('expected.html', forecast_data=None, city=city, error=error_message)
    return render_template('expected.html', forecast_data=None, city=None)

if __name__ == '__main__':
    app.run(debug=True)
