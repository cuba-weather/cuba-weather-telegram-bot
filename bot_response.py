from datetime import datetime

def welcome_message(name):
    welcome_msg = "Hola {} enviame el nombre de un municipio de Cuba para conocer su estado meteorológico"

    return welcome_msg.format(name)

def get_gemoji(description):
    emoji_dict = {
        'claro': '☀️',
        'despejado': '☀️',
        'ligera': '🌦',
        'nublado': '🌥',
        'intensa': '🌨',
        'eléctricas': '🌩',
        'tormentas': '🌩'
    }

    gemoji = '☁️'

    for k in emoji_dict.keys():
        if k in description:
            gemoji = emoji_dict[k]
    
    return gemoji


def weather_message(weather):
    res_msg ="🌐 {}\n📅 {}\n{}\n🌡 {}°C\n💧 {}%\n⏱ {} hpa\n🌬 {} Km/h {}\n"

    gemoji = get_gemoji(weather.descriptionWeather)

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

def forecast_message(weather):
    res_msg ="🌐 {}\n"

    day_msg = "\n📅 {}\n{}\n🌡min. {}°C\n🌡max. {}°C\n"

    result = res_msg.format(weather.cityName)

    for w in weather.days:
        result += day_msg.format(
            datetime.strftime(w.day, "%d-%m-%Y"),
            get_gemoji(w.description) + ' ' + w.description,
            w.tmin,
            w.tmax,
        )

    return result