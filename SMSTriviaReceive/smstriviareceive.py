from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import twilio_config as tcfg, qna_settings as qaset, players_config as pcfg

account_sid = tcfg.twilio["account_sid"]
auth_token = tcfg.twilio["auth_token"]
client = Client(account_sid, auth_token)

app = Flask(__name__)

def create_question(question, answers):
    qa = ""
    qa = qa + "\n" + question["question"]
    qa = qa + "\n"
    qa = qa + answers["choice1"] + "\n"
    qa = qa + answers["choice2"] + "\n"
    qa = qa + answers["choice3"] + "\n"
    qa = qa + answers["choice4"]
    return qa

def send_question(number, questions, answers, qkey):
    # for qkey in questions:
    qa = create_question(questions[qkey], answers[qkey])
    message = client.messages \
                        .create(
                        body=qa,
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )

    print(message.sid)
    return qa

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    lastq,lasta = message_body.split(":")
    nextkey = str(int(lastq) + 1)

    #if message_body == "1:D":
    file_object = open('log.txt', 'a')
    file_object.write("\n Correct Answer")
    file_object.close()

    nextq = send_question(number, qaset.questions, qaset.answers, nextkey)

if __name__ == '__main__':
    phones = pcfg.phones
    for number in phones:
        # sends first question to all
        qa = send_question(number, qaset.questions, qaset.answers, "1")
    app.run()
