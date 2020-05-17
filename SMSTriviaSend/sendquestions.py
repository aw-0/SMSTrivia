# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import twilio_config as tcfg, qna_settings as qaset, players_config as pcfg

phones = pcfg.phones

# qa = {"question": {"q_no": "1"}, {"question": "What is the capital of our country?"},
# {"answers": "choice1": "A: Chicago",
# "choice2": "B: Washington State",
# "choice3": "C: San Francisco",
# "choice4": "D: Washington D.C.",
# "correct": "D: Washington D.C."}


def create_question(question, answers):
    qa = ""
    qa = qa + "\n" + question["question"]
    qa = qa + "\n"
    qa = qa + answers["choice1"] + "\n"
    qa = qa + answers["choice2"] + "\n"
    qa = qa + answers["choice3"] + "\n"
    qa = qa + answers["choice4"]
    return qa

def create_questions(player_name, number, questions, answers):
    # qa = ""
    # qa = qa + "Hello " + player_name + ","
    # for qkey in questions:
    qa = create_question(questions['1'], answers['1'])
    message = client.messages \
                        .create(
                        body=qa,
                        from_=tcfg.twilio["twilio_number"],
                        to=number
                        )

    print(message.sid)
    return qa

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = tcfg.twilio["account_sid"]
auth_token = tcfg.twilio["auth_token"]
client = Client(account_sid, auth_token)
i = 0
for number in phones:
    qa = create_questions(pcfg.players[i], number, qaset.questions, qaset.answers)

    i = i + 1

    print(qa)
