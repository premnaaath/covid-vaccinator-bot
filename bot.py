import time
import telebot
import constants as keys
from get_data import get_data, is_valid_pincode

API_KEY = keys.API_KEY
bot = telebot.TeleBot(API_KEY)

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
        string = ""
        for i in data:
            string += i
        bot.send_message(message.chat.id, string)
        bot.send_message(message.chat.id, msg["found"])
    else:
        bot.send_message(message.chat.id, data[0])


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
