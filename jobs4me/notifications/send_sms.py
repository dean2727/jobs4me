import os
from azure.communication.sms import SmsClient

def sendSms(msg, to):
    try:
        sms_client = SmsClient.from_connection_string("endpoint=https://jobs4me-sms-service.communication.azure.com/;accesskey=XCSp5AKE1mnsH3mpbLaFXibjbC35mda2YOsNPu+oTahmpXYk22jUUzH2aEvyDhdsr5Qv8qU6R/Pe5yZM6UYr7A==")
        sms_response = sms_client.send(
            from_="+18332311057",
            to=to,
            message=msg,
            enable_delivery_report=True
        )
    except Exception as ex:
        print('Exception:')
        print(ex)