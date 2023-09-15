import requests
from flask import Flask, session, render_template, redirect, url_for, request
import os

app = Flask(__name__)


app.secret_key = os.environ['secret_key']


@app.route('/')
def location():
    if (session and session['ip_info']):
        data = session['ip_info']
        return redirect(
            url_for('weather', city=data['city'], state=data['state'])
        )
    else:
        data = get_ip_info()
        if data['success']:
            session['ip_info'] = data
            return redirect(
                url_for('weather', city=data['city'], state=data['state'])
            )
        else:
            return redirect(url_for('error_page'))


@app.route('/weather/<city>/<state>')
def weather(city, state):
    weather_key = os.environ['weather_key']
    if 'ip_info' in session:
        data = session['ip_info']
        ip_coords = data['ip_coords']
        url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={weather_key}&q={ip_coords}'
        resp = requests.get(url)
        data = resp.json()
        geo_info = data.get("Key")
    else:
        geo_info = get_geo_loc(city, state)
    if geo_info is None:
        return error_page('GEO info Missing!')
    url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{geo_info}?apikey={weather_key}&metric=true'
    response = requests.get(url)
    data = response.json()
    weather_icon = str(data[0]["IconPhrase"])
    temperature = str(int(data[0]["Temperature"]["Value"]))
    RAIN_WARNING = data[0]["PrecipitationProbability"]
    rain_level = {
                    0:  "there is a slight chance of rain. " \
                        "You might want to grab an umbrella ☔",
                    1:  "High chance of rain, even the fish are getting their scuba gear ready! " \
                        "Grab an umbrella on your way out and make your grand entrance in style! ☔",
                    2:  "it is raining right now!",
                    3:  "Rain, rain, go away? Not today! It is definitely going to rain! " \
                        "GRAB YOUR UMBRELLA. ☔"
                }
    if RAIN_WARNING == 0:
        rain_commentary = weather_commentary(temperature)
    elif 0 < RAIN_WARNING <= .5:
        rain_commentary = rain_level[0]
    elif .5 < RAIN_WARNING < .75:
        rain_commentary = rain_level[1]
    elif RAIN_WARNING == 1:
        rain_commentary = rain_level[2]
    else:
        rain_commentary = rain_level[3]
    location = {'city': city, 'state': state}
    weather_info = {'temperature': temperature, 'rain': rain_commentary}
    return render_template(
        'weather.html',
        location=location,
        weather_info=weather_info,
        weather_icon=weather_icon
    )
@app.errorhandler(404)
def error_page(error):
    return render_template('404.html'), 404


def get_ip_info():
    if 'X-Forwarded-For' in request.headers:
        user_ip = str(request.headers['X-Forwarded-For'])
    else:
        user_ip = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    if user_ip == '127.0.0.1':
        user_ip = requests.get('http://ip.42.pl/raw').text
    url = 'http://ip-api.com/json/' + user_ip
    response = requests.get(url)
    js = response.json()
    return {
        'success': js['status'] == 'success',
        'city': js['city'],
        'state': js['countryCode'],
        'ip_coords': get_geo_str(js['lat'], js['lon'])
    }


def get_geo_info():
    weather_key = os.environ['weather_key']
    geopar = get_ip_info()
    ip_coords = geopar['ip_coords']
    url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={weather_key}&q={ip_coords}'
    resp = requests.get(url)
    data = resp.json()
    location_key = data.get("Key")
    return location_key

def get_geo_loc(city, state):
    weather_key = os.environ['weather_key']
    url = f'http://dataservice.accuweather.com/locations/v1/cities/{state}/search?apikey={weather_key}&q={city}'
    response = requests.get(url)
    data = response.json()
    location_key = data[0]["Key"]
    return location_key

def get_geo_str(lat, lon):
    return str(lat) + "," + str(lon)

def weather_commentary(temperature):
    temperature = int(temperature)
    temperature_level = {
                0:  "The sun is scorching today. Stay cool and hydrated!",
                1:  "It's a beautiful, hot and sunny day. Remember your sunscreen!",
                2:  "The weather today is like your favorite cozy blanket—just right!",
                3:  "A hot cappuccino would be delightful right now.",
                4:  "Get ready, it's going to be chilly. Bundle up to stay warm!",
                5:  "Winter is here, and it's crisp and cool outside.",
                6:  "It's so freezing that even polar bears are considering moving south!"
    }
    if temperature >= 35:
        return temperature_level[0]
    elif 26.7 <= temperature < 35:
        return temperature_level[1]
    elif 20.6 <= temperature < 26.7:
        return temperature_level[2]
    elif 15 <= temperature < 20.6:
        return temperature_level[3]
    elif 4.4 <= temperature < 15:
        return temperature_level[4]
    elif -3.9 <= temperature < 4.4:
        return temperature_level[5]
    elif temperature < -3.9:
        return temperature_level[6]


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
