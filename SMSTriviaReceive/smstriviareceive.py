from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import twilio_config as tcfg, qna_settings as qaset, players_config as pcfg

account_sid = tcfg.twilio["account_sid"]
auth_token = tcfg.twilio["auth_token"]
client = Client(account_sid, auth_token)
phones = pcfg.phones

player_answers = {
    pcfg.phones[0]: {
            "totalScore": 0,
            "currentQuestion": 1,
            "answers": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": ""}},
    pcfg.phones[1]: {
            "totalScore": 0,
            "currentQuestion": 1,
            "answers": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": ""}}}
print(player_answers["+18479221678"]["currentQuestion"])

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

    # lastq,lasta = message_body.split(":")
    # nextkey = str(int(lastq) + 1)

    lasta = message_body
    currentQuestion = player_answers[number]["currentQuestion"]

    print(qaset.answers[str(currentQuestion)]["correct"])
    print(lasta)
    if lasta == qaset.answers[str(currentQuestion)]["correct"]:
        score = player_answers[number]["totalScore"]
        score += 1
        player_answers[number]["totalScore"] = score
        file_object = open('log.txt', 'a')
        file_object.write(f"{number}, {currentQuestion}, {str(score)}")
        file_object.close()

    player_answers[number]["currentQuestion"] += 1
    nextkey = str(player_answers[number]["currentQuestion"])

    nextq = send_question(number, qaset.questions, qaset.answers, nextkey)

if __name__ == '__main__':
    for number in phones:
        # sends first question to all
        qa = send_question(number, qaset.questions, qaset.answers, "1")
    app.run()
