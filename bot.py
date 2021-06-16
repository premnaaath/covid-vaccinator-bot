import os
import time
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from get_data import get_data, is_valid_pincode

scheduler = BackgroundScheduler()
scheduler.start()
TOKEN = "1871608505:AAHTk1het3w4dtxjPIEsz0N6A92aJ6eQBWQ"
bot = telebot.TeleBot(TOKEN)


greet_msg = """
Hello there!
I'm a bot designed to help you find a vaccine slot in your locality...

Please enter your area Pincode."""

temp = """ 
Sorry, there are no vaccines available near your locality for today!
Please try again after sometime...
        """

text = """
For Registration, please visit
https://selfregistration.cowin.gov.in/

Have a nice day! :)
        """


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, greet_msg)


@bot.message_handler(func=lambda msg: msg.text is not None and "@" not in msg.text)
def send_data(message):
    msg = get_data(message.text)
    if message.text in ["hi", "hello"]:
        bot.send_message(message.chat.id, greet_msg)
    elif len(msg) == 0:
        bot.send_message(message.chat.id, temp)
    elif is_valid_pincode(message.text):
        for i in msg:
            bot.send_message(message.chat.id, i)
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, msg[0])


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
