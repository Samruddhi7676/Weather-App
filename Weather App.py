from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "40f747571070bff88358710aeb271349"  # Your API Key

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

            try:
                response = requests.get(url)
                data = response.json()

                if data["cod"] == "200":
                    weather_data = []
                    for i in range(0, 40, 8):  # Get approx. one entry per day
                        day = data["list"][i]
                        date_obj = datetime.strptime(day["dt_txt"].split()[0], "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%d %B %Y")

                        day_data = {
                            "date": formatted_date,
                            "temp": day["main"]["temp"],
                            "description": day["weather"][0]["description"].title(),
                            "humidity": day["main"]["humidity"]
                        }
                        weather_data.append(day_data)
                else:
                    error = f"City '{city}' not found. Please check the spelling."
            except Exception:
                error = "Unable to fetch weather data. Please try again later."
        else:
            error = "Please enter a city name."

    return render_template("templates.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
