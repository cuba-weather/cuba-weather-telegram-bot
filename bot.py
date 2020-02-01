import config

import telebot

from cuba_weather_redcuba import CubaWeatherRedCuba

from .bot_response import welcome_message, weather_message

bot = telebot.TeleBot(config.token)

api = CubaWeatherRedCuba()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        welcome_message(message.from_user.first_name)
    )

@bot.message_handler(content_types=['text'])
def send_response(message):
    weather = api.get(message.text)

    gemoji = defaul_emoji

    for k in emoji_dict.keys():
        if k in weather.descriptionWeather.lower():
            gemoji = emoji_dict[k]

    bot.reply_to(message, weather_message(weather), parse_mode='HTML')

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
                weather_message(weather),
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