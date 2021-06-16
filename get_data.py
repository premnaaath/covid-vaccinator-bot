from datetime import date
import re
import requests
import json


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


# Test
if __name__ == "__main__":
    data = get_data("600096")
    for i in data:
        print(i)
