# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import config as cfg

phones = ['Number']

questions = ['What is the capital of our country?',
'How many limbs does a human have?',
'How many calories should a person have in a day?',
'What is this coded in?',
'Whats the capital of our State?']

answers = {"0": {"choice1": "A: Chicago",
"choice2": "B: Washington State",
"choice3": "C: San Francisco",
"choice4": "D: Washington D.C.",
"correct": "D: Washington D.C."},
"1": {"choice1": "Chicago",
"choice2": "Washington State",
"choice3": "San Francisco",
"choice4": "Washington D.C.",
"correct": "Washington D.C."},
"2": {"choice1": "Chicago",
"choice2": "Washington State",
"choice3": "San Francisco",
"choice4": "Washington D.C.",
"correct": "Washington D.C."},
"3": {"choice1": "Chicago",
"choice2": "Washington State",
"choice3": "San Francisco",
"choice4": "Washington D.C.",
"correct": "Washington D.C."},
"4": {"choice1": "Chicago",
"choice2": "Washington State",
"choice3": "San Francisco",
"choice4": "Washington D.C.",
"correct": "Washington D.C."}}

qa = ""
qa = questions[0]
qa = qa + "\n"
qa = qa + answers["0"]["choice1"] + "\n"
qa = qa + answers["0"]["choice2"] + "\n"
qa = qa + answers["0"]["choice3"] + "\n"
qa = qa + answers["0"]["choice4"]

print(qa)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = cfg.twilio["account_sid"]
auth_token = cfg.twilio["auth_token"]
client = Client(account_sid, auth_token)
for number in phones:
    message = client.messages \
                    .create(
                        body=qa,
                        from_='+12568575536',
                        to=number
                        )

    print(message.sid)
