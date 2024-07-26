import requests, stringcase, os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

app = Flask(__name__)

url = f'http://api.openweathermap.org/data/2.5/weather'


def configure():
    load_dotenv()


def meter_per_sec_to_kilo_per_hour(meter_per_sec):
    kil_per_hour = meter_per_sec * 3.6
    return kil_per_hour


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']

        params = {'q': city,
                  'app_id': os.getenv('api_key'),
                  'units': 'metric'}

        response = requests.get(url, params=params)
        data = response.json()

        if data['cod'] != '404':
            current_temperature = int(round(data['main']['temp'], 0))  # round the temperature

            des = data['weather']  # access weather dictionary
            description = des[0]['description']  # access description in dictionary

            min_temp = int(round(data['main']['temp_min'], 0))

            max_temp = int(round(data['main']['temp_max'], 0))

            curr_wind = data['wind']['speed']
            wind = round(meter_per_sec_to_kilo_per_hour(curr_wind), 2)

            wea_icon = des[0]['icon']

            print(data)

            titlecase_city = city.title()

            return render_template('home.html', city=titlecase_city, current_temperature=current_temperature,
                                   description=description, min_temp=min_temp, max_temp=max_temp, wind=wind,
                                   wea_icon=wea_icon)

        else:
            return render_template('home.html', None)

    else:
        return render_template('home.html')


@app.route('/countries')
def countries():
    return render_template('countries.html')


if __name__ == '__main__':
    configure()
    app.run(debug=True)
