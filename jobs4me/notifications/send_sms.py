import os
from azure.communication.sms import SmsClient

# not using SMS for this project
def sendSms(username, users_name, to, match_percentage):
    try:
        #sms_connection_string = os.environ.get("JOBS4ME_SMS_SERVICE")
        msg = "New job from Jobs4Me!\nHi " + users_name + "! We found a new job for you, which matched " + match_percentage + "%" + " of your resumes! For details, login to your account or check your email."

        sms_client = SmsClient.from_connection_string("replace me with the connection string Azure gives you")
        sms_response = sms_client.send(
            from_="replace me with the phone number Azure gives you",
            to=to,
            message=msg,
            enable_delivery_report=True
        )

        print("SMS messages successfully sent to user " + username)
    except Exception as ex:
        print('Exception:')
        print(ex)