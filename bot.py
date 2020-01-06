from cuba_weather import weather
from cuba_weather import finder

from flask import Flask, request

import config

import telebot

bot = telebot.TeleBot(config.token)
server = Flask(__name__)

welcome_msg = "Hola {0} enviame un municipio de Cuba para conocer su estado meteorológico"

res_msg ="""
<strong>{0}</strong>\n
<strong>{1}</strong>\n
<strong>Temperatura:</strong> {2}°C\n
<strong>Humedad:</strong> {3}%\n
<strong>Presión atmosférica:</strong> {4} hpa
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        welcome_msg.format(message.from_user.first_name)
    )

@bot.message_handler(content_types=['text'])
def send_response(message):
    try:
        loc = finder.get_location(message.text)
        c = weather.RCApiClient(loc)
        bot.reply_to(message, res_msg.format(
            loc,
            c.getGeneral(),
            c.getTemperature(),
            c.getHumidity(),
            c.getPressure()
        ), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, e)

@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
        )]
    )

    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://cuba-weather-bot.herokuapp.com/' + config.token)
    return "!", 200