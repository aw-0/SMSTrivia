set echo off
sh twilio phone-numbers:update "+12568575536" --sms-url="http://localhost:5000/sms" 2> error.log &
echo "* Welcome to the SMS Trivia Game Server! *"
cd /Users/andrew/Desktop/Coding/CoderSchool/SMSTrivia/SMSTriviaReceive
source bin/activate
cd /Users/andrew/Desktop/Coding/CoderSchool/SMSTrivia/SMSTriviaReceive
python3 smstriviareceive.py
