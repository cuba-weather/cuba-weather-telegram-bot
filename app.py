import config

from flask import Flask, request

from bot import bot

import telebot

server = Flask(__name__)

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
    bot.set_webhook(url='https://cuba-weather.herokuapp.com/' + config.token)
    return "!", 200