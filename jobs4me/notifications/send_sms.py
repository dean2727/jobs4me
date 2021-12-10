import os
from azure.communication.sms import SmsClient

def sendSms(username, users_name, to, match_percentage):
    try:
        #sms_connection_string = os.environ.get("JOBS4ME_SMS_SERVICE")
        msg = "New job from Jobs4Me!\nHi " + users_name + "! We found a new job for you, which matched " + match_percentage + "%" + " of your resumes! For details, login to your account or check your email."

        sms_client = SmsClient.from_connection_string("endpoint=https://jobs4me-sms-service.communication.azure.com/;accesskey=XCSp5AKE1mnsH3mpbLaFXibjbC35mda2YOsNPu+oTahmpXYk22jUUzH2aEvyDhdsr5Qv8qU6R/Pe5yZM6UYr7A==")
        sms_response = sms_client.send(
            from_="+18332311057",
            to=to,
            message=msg,
            enable_delivery_report=True
        )

        print("SMS messages successfully sent to user " + username)
    except Exception as ex:
        print('Exception:')
        print(ex)