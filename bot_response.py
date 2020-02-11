def welcome_message(name):
    welcome_msg = "Hola {} enviame el nombre de un municipio de Cuba para conocer su estado meteorológico"

    return welcome_msg.format(name)


def weather_message(weather):
    res_msg ="🌐 {}\n📅 {}\n{}\n🌡 {}°C\n💧 {}%\n⏱: {} hpa\n🌬 {} Km/h {}\n"

    emoji_dict = {
        'despejado': '☀️',
        'ligera': '🌦',
        'nublado': '🌥',
        'intensa': '🌨',
    }

    gemoji = '⛅️'

    for k in emoji_dict.keys():
        if k in weather.descriptionWeather.lower():
            gemoji = emoji_dict[k]

    return res_msg.format(
        weather.cityName,
        str(weather.dt.date),
        gemoji + ' ' + weather.descriptionWeather,
        weather.temp,
        weather.humidity,
        weather.pressure,
        weather.windVelocity,
        weather.windDirectionDescription,
    )

    