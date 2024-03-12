import requests

# All the ski resorts and there lat and lon
locations = {
    "Ankara Turkije": {"lat": 39.9334, "lon": 32.8597},
    "Athene Griekeland": {"lat": 37.9838, "lon": 23.7275},
    "La Valette, Malta": {"lat": 35.8992, "lon": 14.5141},
    "Sardinië, Italië": {"lat": 40.1209, "lon": 9.0129},
    "Sicilië, Italië": {"lat": 37.3979, "lon": 14.6588},
    "Nicosia, Cyprus": {"lat": 35.1856, "lon": 33.3823},
    "Mallorca, Spanje": {"lat": 39.6953, "lon": 3.0176},
    "Lagos, Portugal": {"lat": 37.1028, "lon": 8.6730},
    "Mauritius": {"lat": 20.3484, "lon": 57.5522},
    "Boekarest, Roemenië": {"lat": 44.4268, "lon": 26.1025}
}

# Creating the WeatherInfo class to get the Temp of the week and the Snowfall
class WeatherInfo:
    def __init__(self, place, OpenWeatherMap):
        self.place = place
        self.weather_data = [WeatherTime(data) for data in OpenWeatherMap.get("list")]


    # Round the number out
    def round_result(self, r):
        return round(r, 2)

    # get to show to lacation name
    def get_location_name(self):
        return self.place

    # getting the min temp
    def min_temp_week(self):
        min_temp_week = min(WeatherTime.get_min_temperature() for WeatherTime in self.weather_data)
        return self.round_result(min_temp_week)

    def max_temp_week(self):
        max_temp_week = max(WeatherTime.get_max_temperature() for WeatherTime in self.weather_data)
        return self.round_result(max_temp_week)

    # Gets the avg by adding max + min and /2
    def avg_temp_week(self):
        t = 0.0
        for wd in self.weather_data:
            t += wd.get_temperature()
        t = t / len(self.weather_data)
        return self.round_result(t)

    def avg_rain_week(self):
        total_rain = sum(WeatherTime.get_rain() for WeatherTime in self.weather_data)
        avg_rain = total_rain / 5
        return self.round_result(avg_rain)

    def rain_week_no_numb(self):
        if self.avg_rain_week() <= 1:
            return "Very little"
        elif 1 < self.avg_rain_week() < 2:
            return "Less than 2mm"
        elif self.avg_rain_week() >= 2:
            return "More than 2mm"

    # Gets the rating for the ski resort
    def get_rating(self):
        score = 0
        if self.avg_temp_week() - temp_preference <= 2:
            score = 5
        elif self.avg_temp_week() - temp_preference <= 3:
            score = 4
        elif self.avg_temp_week() - temp_preference <= 5:
            score = 3
        elif self.avg_temp_week() - temp_preference <= 7:
            score = 2
        elif self.avg_temp_week() - temp_preference <= 10:
            score = 1

        if self.avg_rain_week() <= 1 and rain_preference == 1:
            score += 4
        elif 1 < self.avg_rain_week() < 2 and rain_preference == 2:
            score += 4
        elif rain_preference == 3:
            score += 4

class WeatherTime:
    def __init__(self, data):
        self.data = data

    def get_date(self):
        return self.data.get("dt_txt")[0:10]

    def get_item(self, name):
        return self.data.get(name, {}).get("3h", 0.0)

    def get_main_item(self, name):
        return self.data.get("main", {}).get(name)

    def get_rain(self):
        return self.get_item("rain")

    def get_min_temperature(self):
        return self.get_main_item("temp_min")

    def get_max_temperature(self):
        return self.get_main_item("temp_max")

    def get_temperature(self):
        return self.get_main_item("temp")

###################################################################"

temp_preference = int(input("What temperature do you want? "))
print("Choose your rain preference:")
print("1. Very little rain.")
print("2. Less than 2mm rain per day.")
print("3. No preference")
rain_preference = input("Choose your preference (1/2/3): ")

weather_data = []
for locations, coordiates in locations.items():
    lat = coordiates.get("lat")
    lon = coordiates.get("lon")
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=45bd72ea28e3d31cd6abd08f17e7d154&units=metric")
    weather_data.append(WeatherInfo(locations, response.json()))

    # HIER CODE VOOR VOLGORDE


# Writes the message of the email
email_message = ""
for WeatherInfo in weather_data:
    location_info = f"""
    {WeatherInfo.get_location_name()}:
        {WeatherInfo.rain_week_no_numb()} rain  |   {WeatherInfo.avg_rain_week()}
        Average Temperature: {WeatherInfo.avg_temp_week()} °C
    """
    email_message += location_info

print(email_message)