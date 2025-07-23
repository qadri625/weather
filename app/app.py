from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city=None, lat=None, lon=None, units="metric"):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    elif lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
    else:
        return None, None

    w = requests.get(url).json()
    f = requests.get(forecast_url).json()

    if w.get("cod") != 200:
        return None, None

    weather = {
        'city': w['name'],
        'temp': round(w['main']['temp'], 2),
        'description': w['weather'][0]['description'].title(),
        'humidity': w['main']['humidity'],
        'wind': w['wind']['speed'],
        'icon': w['weather'][0]['icon'],
        'units': units
    }

    forecast = []
    for entry in f['list'][:5*8:8]:  # every 8 entries ≈ 1 day
        forecast.append({
            'date': entry['dt_txt'].split(" ")[0],
            'temp': round(entry['main']['temp'], 2),
            'icon': entry['weather'][0]['icon']
        })

    return weather, forecast

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = forecast = None
    units = request.args.get('units', 'metric')

    if request.method == 'POST':
        city = request.form['city']
        weather, forecast = fetch_weather(city=city, units=units)
    elif 'lat' in request.args and 'lon' in request.args:
        lat = request.args['lat']
        lon = request.args['lon']
        weather, forecast = fetch_weather(lat=lat, lon=lon, units=units)

    return render_template('index.html', weather=weather, forecast=forecast, units=units)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

