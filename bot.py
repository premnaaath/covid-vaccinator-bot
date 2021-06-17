import time
import telebot
import constants as keys
from get_data import get_data, is_valid_pincode
from apscheduler.schedulers.background import BackgroundScheduler

API_KEY = keys.API_KEY
bot = telebot.TeleBot(API_KEY)
scheduler = BackgroundScheduler()
scheduler.start()


@bot.message_handler(commands=["start"])
def start(message):
    msg = '''
Hello there!
I'm a bot designed to help you find a vaccine slot in your locality...

Please enter your area Pincode.'''
    bot.send_message(message.chat.id, msg)


def temp(message):
    return True


@bot.message_handler(func=lambda *_: True)
def send_data(message):
    msg = get_data(message.text)
    if len(msg) == 0:
        temp = ''' 
Sorry, there are no vaccines available near your locality for today!
Please try again after sometime...
        '''
        bot.send_message(message.chat.id, temp)
    elif is_valid_pincode(message.text):
        for i in msg:
            bot.send_message(message.chat.id, i)
        text = '''
For Registration, please visit
https://selfregistration.cowin.gov.in/

Have a nice day! :)
        '''
        bot.send_message(message.chat.id, text=text)
    else:
        bot.send_message(message.chat.id, msg[0])


while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
