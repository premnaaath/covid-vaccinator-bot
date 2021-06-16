import os
import telebot
from flask import Flask, request
from datetime import date
import re
import requests
import json

TOKEN = "1871608505:AAHTk1het3w4dtxjPIEsz0N6A92aJ6eQBWQ"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# covid_vaccinator_bot
base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"


def is_valid_pincode(pincode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    temp = re.compile(regex)
    if pincode == "":
        return False
    result = re.match(temp, pincode)
    if result:
        return True
    return False


def fetch(pincode):
    today = date.today().strftime("%d-%m-%Y")
    req = base_url + "?pincode={}&date={}".format(pincode, today)
    res = requests.get(req).json()
    return res["sessions"]


def get_possible(data):
    op = list()
    for i in data:
        if i["available_capacity"] > 0:
            op.append(i)
    return op


def generate_msg(data):
    message = list()
    for i in data:
        msg = """
Hospital Name: {}
Address: {}
Pincode: {}
Age Limit: {}+
Dose 1: {}
Dose 2: {}
Fee in Rs: {}
Availability Count: {}
Working Time: {}
        """.format(
            i["name"],
            i["address"],
            i["pincode"],
            i["min_age_limit"],
            i["available_capacity_dose1"],
            i["available_capacity_dose2"],
            i["fee"],
            i["available_capacity"],
            "{} to {}".format(i["from"], i["to"]),
        )
        message.append(msg)
    return message


def get_data(pincode):
    if is_valid_pincode(pincode) == False:
        return ["Invalid pincode, please try again!"]
    data = fetch(pincode)
    data = get_possible(data)
    return generate_msg(data)


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
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, msg[0])


@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://covid-vaccinator-bot.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
