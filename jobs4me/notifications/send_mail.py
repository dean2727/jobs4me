from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendEmail(receiver, bod, token):
    sender = "dean27@tamu.edu"

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject="New Job from Jobs4Me!",
        html_content=str(bod))

    try:
        sg = SendGridAPIClient(token)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)