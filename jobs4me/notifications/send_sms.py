import os
from azure.communication.sms import SmsClient

def sendSms(username, users_name, to, job_title, job_url, match_percentage):
    try:
        #sms_connection_string = os.environ.get("JOBS4ME_SMS_SERVICE")
        msg1 = "New job from Jobs4Me!\n\nHi " + users_name + "! We found a new job for you, which matched " + match_percentage + " of your latest resume! Here are some details:"
        msg2 = "Title: " + job_title + "\nLink to this posting: " + job_url

        sms_client = SmsClient.from_connection_string("endpoint=https://jobs4me-sms-service.communication.azure.com/;accesskey=XCSp5AKE1mnsH3mpbLaFXibjbC35mda2YOsNPu+oTahmpXYk22jUUzH2aEvyDhdsr5Qv8qU6R/Pe5yZM6UYr7A==")
        sms_response1 = sms_client.send(
            from_="+18332311057",
            to=to,
            message=msg1,
            enable_delivery_report=True
        )

        sms_response2 = sms_client.send(
            from_="+18332311057",
            to=to,
            message=msg2,
            enable_delivery_report=True
        )

        print("SMS messages successfully sent to user " + username)
    except Exception as ex:
        print('Exception:')
        print(ex)