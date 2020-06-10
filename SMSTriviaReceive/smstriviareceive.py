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
            "done": False,
            "answers": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": "",}},
    pcfg.phones[1]: {
            "totalScore": 0,
            "currentQuestion": 1,
            "done": False,
            "answers": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": ""}}}
scoreboard = {
    "1800": 3,
    "1224": 5,
    "1312": 4
}

for key, value in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True):
    print("%s: %s" % (key, scoreboard[key]))

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

def end_message(number):
    message = client.messages \
                        .create(
                        body="You have reached the end of the Quiz! Please wait until everyone has finished answering the questions",
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )
    print(message.sid)

def send_message(number, text):
    message = client.messages \
                        .create(
                        body=text,
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )
    print(message.sid)

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

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

    temp_nextkey = str(player_answers[number]["currentQuestion"] + 1)

    if temp_nextkey not in qaset.questions:
        end_message(number)
        player_answers[number]["done"] = True
    else:
        player_answers[number]["currentQuestion"] += 1
        nextq = send_question(number, qaset.questions, qaset.answers, temp_nextkey)

    end_or_not = True

    for phonekey in player_answers:
        if player_answers[phonekey]["done"] == False:
            end_or_not = False
            break

    if end_or_not == True:
        for phonekey in player_answers:

            winner = "no one!"
            send_message(phonekey, "Congratulations! Everyone has finished the quiz!")

            # board = f"""
            # --LEADERBOARD--
            #
            # {phones[0]} finished with {player_answers[phones[0]['totalScore']} correct!
            #
            # {phones[1]} finished with {player_answers[phones[1]]['totalScore']} correct!
            #
            # In the end, {} won!
            #
            # """
            send_message(phonekey, f"You finished with {player_answers[phonekey]['totalScore']} correct!")
            #--LEADERBOARD--

            #Player1 finished with 3(totalscore) questions correct!

            #Player2 finished with 5 questions correct!

            #In the end, Player2 won!



if __name__ == '__main__':
    for number in phones:
        # sends first question to all
        qa = send_question(number, qaset.questions, qaset.answers, "1")
    app.run()
