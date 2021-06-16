import os
import constants as key
from get_data import get_data, is_valid_pincode
from flask import Flask, request
import telebot

TOKEN = key.TOKEN
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

greet_msg = """
Hello there!
I'm a bot designed to help you find a vaccine slot in your locality...

Please enter your area Pincode."""


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, greet_msg)


def temp(message):
    return True


@bot.message_handler(func=temp)
def send_data(message):
    msg = get_data(message.text)
    if message.text in ["hi", "hello"]:
        bot.send_message(message.chat.id, greet_msg)
    elif len(msg) == 0:
        temp = """ 
Sorry, there are no vaccines available near your locality for today!
Please try again after sometime...
        """
        bot.send_message(message.chat.id, temp)
    elif is_valid_pincode(message.text):
        for i in msg:
            bot.send_message(message.chat.id, i)
        text = """
For Registration, please visit
https://selfregistration.cowin.gov.in/

Have a nice day! :)
        """
        bot.send_message(message.chat.id, text=text)
    else:
        bot.send_message(message.chat.id, msg[0])


@app.route("/" + TOKEN, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://covid-vaccinator-bot.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
