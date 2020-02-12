import config

import telebot

from cuba_weather_redcuba import CubaWeatherRedCuba

import bot_response as br

bot = telebot.TeleBot(config.token)

api = CubaWeatherRedCuba()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        br.welcome_message(message.from_user.first_name)
    )

from cuba_weather_owm import CubaWeatherOWM
import os

@bot.message_handler(commands=['forecast'])
def send_forecast(message):
    try:
        _, location = message.text.split(' ')
    except:
        bot.reply_to(
            message,
            'Enviame /forecast localidad , ej: /forecast Santiago'
        )
        return

    API_KEY = os.environ['OWM_API']

    api = CubaWeatherOWM(API_KEY)

    weath = api.get(location)

    bot.reply_to(
        message,
        br.forecast_message(weath)
    )

@bot.message_handler(content_types=['text'])
def send_response(message):
    weather = api.get(message.text)

    bot.reply_to(message, br.weather_message(weather), parse_mode='HTML')

## INLINE
from telebot import types

@bot.inline_handler(lambda query: len(query.query) > 2)
def query_text(inline_query):
    weather = api.get(inline_query.query)

    try:
        r = types.InlineQueryResultArticle(
            '1',
            weather.cityName,
            types.InputTextMessageContent(
                br.weather_message(weather),
                parse_mode='HTML'
            )
        )

        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)

import time
import sys

def main_loop():
    bot.polling(True)
    
    while 1:
        time.sleep(3)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)