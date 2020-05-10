from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

account_sid = "ACb9f38ef210a2dbefeec2e92f23a469e8"#tcfg.twilio["account_sid"]
auth_token = "0ae8bb03e3e532dd0f8d1bae24699037"#tcfg.twilio["auth_token"]
client = Client(account_sid, auth_token)


app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    resp = MessagingResponse()
    messagelog = 'Hello World {}, you said: {}'.format(number, message_body)
    resp.message(messagelog)

    file_object = open('log.txt', 'a')
    file_object.write(messagelog)
    file_object.close()

    if message_body == "0:D":
         file_object = open('log.txt', 'a')
         file_object.write("\n Correct Answer")
         file_object.close()

         message = client.messages \
                          .create(
                             body="Correct Answer!",
                             from_="+12568575536",#tcfg.twilio["twilio_number"],
                             to=number
                             )

    return str(resp)

if __name__ == '__main__':
    app.run()
