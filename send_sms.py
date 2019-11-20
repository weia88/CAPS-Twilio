#! usr/bin/env python3
#If server dies, have a catch or error be sent via email, to restart server asap
    #probably outside of python
import os
import argparse
import json # feed in file and numbers

participant_list = {}

from twilio.rest import Client

parser = argparse.ArgumentParser()
parser.add_argument("dayofweek", type = str, nargs = "?", default = "wednesday") # wednesday, thursday, friday, saturday, sunday
parser.add_argument("timeofday", type = str, nargs = "?", default = "morning") # morning or afternoon
parser.add_argument("currenttime", type = int, nargs = "?", default = 0) # Either initial or reminded (0/1))
args = parser.parse_args()
#args.day will return "wednesday or nargs"
# print("today is " + args.dayofweek) test cron

# Test purposes dayofweek and timeofday are hardcoded
day_of_week = args.dayofweek
time_of_day = args.timeofday
current_time = args.currenttime

morning_days = ["friday", "saturday", "sunday"]
afternoon_days = ["thursday", "friday", "saturday"]

#Participant class
class Participant:
    def __init__(self, PIN, phone, entry, completed):
        self.PIN = PIN
        self.phone = phone
        self.entry = entry
        self.completed = completed

    def print_participant(self):
        print("PIN: " + self.PIN + "|Phone Number: " + self.phone +  "|entry: "
                + self.entry + "|completed: " + str(self.completed))
#read in data file
with open("test.txt", "r") as json_file:
    data = json.load(json_file)
    #make participant_list a dictionary of Participant (class)
    for p in data["participants"]:
        participant_list[p["PIN"]] = Participant(p["PIN"], p["phone"], p["entry"], p["completed"])

def send_message(phone_num, text_body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)
    client.messages.create(
        to=phone_num,
        from_=" ", # place phone number here
        body=text_body
    )

# ************
if "wednesday" in day_of_week:
    for participant in participant_list: #grab relevant info
        text_body = "Hello, \n This is to remind you of that your follow up surveys for the " \
                        "College, Alcohol and Peers Study will start tomorrow at 4 PM. " \
                        "This is week " + participant_list[participant].entry + " of 4." \
                        "Please reply to this text to confirm receipt."
        send_message(participant_list[participant].phone, text_body)


#Friday, Saturday, Sunday morning diary (Initial)
if any(x in day_of_week for x in morning_days) and "morning" in time_of_day:
    if current_time == 0:
        for participant in participant_list: #grab relevant info
            text_body = "Your CAPS morning survey is now ready and will close at 1 pm PST. " \
                        "You will earn $2 for completing these questions. " \
                        "https://uwartsandsciences.sjc1.qualtrics.com/" \
                        "jfe/form/SV_6nYkAPKhKtXemIR?PIN=" + participant_list[participant].PIN
            send_message(participant_list[participant].phone, text_body)
    elif current_time == 1:
        for participant in participant_list: #grab relevant info
            if participant_list[participant].completed:
                text_body = "It is not too late to complete your CAPS afternoon survey before 1 pm PST. " \
                            "Remember, you will get a $10 bonus for completing 80% of surveys " \
                            "in addition to what you have already earned. " \
                            "https://uwartsandsciences.sjc1.qualtrics.com/" \
                            "jfe/form/SV_6nYkAPKhKtXemIR?PIN=" + participant_list[participant].PIN
                send_message(participant_list[participant].phone, text_body)

#Thursday, Friday, Saturday afternoon diary (initial)
if any(x in day_of_week for x in afternoon_days) and "afternoon" in time_of_day:
    if current_time == 0:
        for participant in participant_list: #grab relevant info
            text_body = "Your CAPS morning survey is now ready and will close at 6 pm PST. " \
                        "You will earn $2 for completing these questions. " \
                        "https://uwartsandsciences.sjc1.qualtrics.com/" \
                        "jfe/form/SV_87jBIX8rPUGahgx?PIN=" + participant_list[participant].PIN
            send_message(participant_list[participant].phone, text_body)
    elif current_time == 1:
        for participant in participant_list: #grab relevant info
            if participant_list[participant].completed:
                text_body = "It is not too late to complete your CAPS afternoon survey before 6 pm PST. " \
                            "Remember, you will get a $10 bonus for completing 80% of surveys " \
                            "in addition to what you have already earned. " \
                            "https://uwartsandsciences.sjc1.qualtrics.com/" \
                            "jfe/form/SV_87jBIX8rPUGahgx?PIN=" + participant_list[participant].PIN
                send_message(participant_list[participant].phone, text_body)
# ************

# if __name__ == "__main__":
