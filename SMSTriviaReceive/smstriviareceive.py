#importing libraries
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import twilio_config as tcfg, qna_settings as qaset, players_config as pcfg
#set configurations

account_sid = tcfg.twilio["account_sid"]
auth_token = tcfg.twilio["auth_token"]
client = Client(account_sid, auth_token)
phones = pcfg.phones

player_answers = {
}

for phonekey in pcfg.phones:
    player_answers.update( {phonekey : {
            "totalScore": 0,
            "currentQuestion": 1,
            "done": False,
            "answers": {
            }}})
#start flask webserver
app = Flask(__name__)
#creating the question as a SMS text
def create_question(question, answers):
    qa = ""
    qa = qa + "\n" + question["question"]
    qa = qa + "\n"
    qa = qa + answers["choice1"] + "\n"
    qa = qa + answers["choice2"] + "\n"
    qa = qa + answers["choice3"] + "\n"
    qa = qa + answers["choice4"]
    return qa
#sends the question through SMS text
def send_question(number, questions, answers, qkey):
    qa = create_question(questions[qkey], answers[qkey])
    message = client.messages \
                        .create(
                        body=qa,
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )

    return qa
#sends a message informing the player that they have finished
def end_message(number):
    message = client.messages \
                        .create(
                        body="You have reached the end of the Quiz! Please wait until everyone has finished answering the questions",
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )
#is able to send a message to the player using SMS text
def send_message(number, text):
    message = client.messages \
                        .create(
                        body=text,
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )
#sends the leaderboard and final message through SMS text
def print_leaderboard(player_answers):
    leaderboard = {}
    for key in player_answers:
        leaderboard[key]=player_answers[key]['totalScore']
    sortedLeaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    for phonekey in player_answers:
        game_end_message = ""
        for (key, value) in sortedLeaderboard:
            leaderboardMessage = ("%s: %s" % (key, value))
            game_end_message = game_end_message + leaderboardMessage + "\n"
        send_message(phonekey,f"\nCongratulations! Everyone has finished the quiz! \n \n ---Leaderboard--- \n{game_end_message}")

#adds one point to the score
def Increment_score(player_answers):
    score = player_answers[number]["totalScore"]
    score += 1
    player_answers[number]["totalScore"] = score
#where the SMS gets received
@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    lasta = message_body
    currentQuestion = player_answers[number]["currentQuestion"]

    if lasta == qaset.answers[str(currentQuestion)]["correct"]:
        Increment_score(player_answers)

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
        print_leaderboard(player_answers)
if __name__ == '__main__':
    for number in phones:
        # sends first question to all
        qa = send_question(number, qaset.questions, qaset.answers, "1")
    app.run()


#Example code
##############

#file_object = open('log.txt', 'a')
#file_object.write(f"{number}, {currentQuestion}, {str(score)}")
#file_object.close()

#player_answers2.update( {'2738' : 2} )
#    print("%s: %s" % (key, player_answers[key]["totalScore"]))
    #player_answers2.update( key = player_answers[key]["totalScore"])
    #player_answers2[key]=player_answers[key]['totalScore']
    #player_answers2.update( {key: player_answers[key]["totalScore"]})
#for key in player_answers2:
    #print("%s: %s" % (key, player_answers2[key]))

#for key, value in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True):
    #print("%s: %s" % (key, scoreboard[key]))
