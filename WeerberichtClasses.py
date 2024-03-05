import requests

def getdata(latitude, longitude):
    try:
        # Fetch location data
        location = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={latitude},{longitude}&appid=45bd72ea28e3d31cd6abd08f17e7d154&units=metric").json()

        # Check if the location data is empty
        if not location:
            return {"error": "Unable to fetch location data."}

        lat = location[0].get("lat")
        lon = location[0].get("lon")

        # Fetch weather data
        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=45bd72ea28e3d31cd6abd08f17e7d154&units=metric").json()

        # Check if the 'list' key exists in the weather data
        if 'list' not in weather:
            return {"error": "Unable to fetch weather data."}

        response = {}
        for element in weather.get('list'):
            date = element.get('dt_txt').split(' ')[0]
            if date not in response:
                response.update({date: [element]})
            else:
                response.get(date).append(element)

        for dayitems in response.items():
            day = dayitems[1]
            maxlist = []

            for result in day:
                maxlist.append(result.get('main').get('temp_max'))

            maxTemp = maxlist[0]
            for temp in maxlist:
                if maxTemp < temp:
                    maxTemp = temp

            minlist = []
            for result in day:
                minlist.append(result.get('main').get('temp_min'))

            minTemp = minlist[0]
            for temp in minlist:
                if minTemp > temp:
                    minTemp = temp

            rain = 0
            for result in day:
                if result.get('rain') is not None:
                    rain += result.get('rain').get('3h')

            weatherdescription = {}
            for result in day:
                description = result.get('weather')[0].get('description')
                if description in weatherdescription:
                    weatherdescription.update({description: weatherdescription.get(description) + 1})
                else:
                    weatherdescription.update({description: 1})

            windlist = []
            for result in day:
                windlist.append(result.get('wind').get('speed'))

            wind1 = windlist[0]
            for wind in windlist:
                if wind1 < wind:
                    wind1 = wind

            response.update({dayitems[0]: {"max-temp": maxTemp, "min-temp": minTemp, "rain": rain, "wind": wind1,
                                           "description": weatherdescription}})

        return response

    except requests.exceptions.RequestException as e:
        return {"error": f"Request to OpenWeatherMap API failed: {e}"}
