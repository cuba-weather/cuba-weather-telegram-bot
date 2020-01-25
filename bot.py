import config

import telebot

from cuba_weather import RCApiClient

bot = telebot.TeleBot(config.token)

api = RCApiClient()

welcome_msg = "Hola {0} enviame el nombre de una localidad de Cuba para conocer su estado meteorológico"

res_msg ="""
<strong>🌐 {0}</strong>\n
<strong>{1}</strong>\n
<strong>🌡 Temperatura:</strong> {2}°C\n
<strong>💧 Humedad:</strong> {3}%\n
<strong>Presión atmosférica:</strong> {4} hpa\n
<strong>🌬 Vientos: </strong>\n
{5}\n
📅 {6}
"""

emoji_dict = {}

defaul_emoji = '⛅️'

emoji_dict['despejado'] = '☀️'
emoji_dict['ligera'] = '🌦'
emoji_dict['nublado'] = '🌥'
emoji_dict['intensa'] = '🌨'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        welcome_msg.format(message.from_user.first_name)
    )

@bot.message_handler(content_types=['text'])
def send_response(message):
    weather = api.get(message.text, suggestion=True)

    gemoji = defaul_emoji

    for k in emoji_dict.keys():
        if k in weather.general.lower():
            gemoji = emoji_dict[k]

    bot.reply_to(message, res_msg.format(
        weather.city_name,
        gemoji + ' ' + weather.general,
        weather.temperature,
        weather.humidity,
        weather.pressure,
        weather.wind,
        weather.timestamp
    ), parse_mode='HTML')

bot.polling()
