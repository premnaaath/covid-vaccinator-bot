import os
import time
import telebot
import constants as keys
from flask import Flask, request
from get_data import get_data, is_valid_pincode


TOKEN = keys.TOKEN
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

msg = dict()

msg["greet"] = '''
Hello there!
I'm a bot designed to help you find a vaccine slot in your locality...

Please enter your area Pincode.'''

msg["nil"] = ''' 
Sorry, there are no vaccines available near your locality for today!
Please try again after sometime...'''

msg["found"] = '''
For Registration, please visit
https://selfregistration.cowin.gov.in/

Have a nice day! :)'''


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, msg["greet"])


@bot.message_handler(func=lambda *_: True)
def send_data(message):
    data = get_data(message.text)
    if len(data) == 0:
        bot.send_message(message.chat.id, msg["nil"])
    elif is_valid_pincode(message.text):
        for i in data:
            bot.send_message(message.chat.id, i)
        bot.send_message(message.chat.id, msg["found"])
    else:
        bot.send_message(message.chat.id, data[0])


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ancient-temple-78234.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
