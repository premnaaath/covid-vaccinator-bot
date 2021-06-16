import constants as key
from get_data import get_data, is_valid_pincode
import telebot

API_KEY = key.API_KEY
bot = telebot.TeleBot(API_KEY)

greet_msg = '''
Hello there!
I'm a bot designed to help you find a vaccine slot in your locality...

Please enter your area Pincode.'''


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, greet_msg)


def temp(message):
    return True


@bot.message_handler(func=temp)
def send_data(message):
    msg = get_data(message.text)
    if message.text in ['hi', 'hello']:
        bot.send_message(message.chat.id, greet_msg)
    elif len(msg) == 0:
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


bot.polling()
