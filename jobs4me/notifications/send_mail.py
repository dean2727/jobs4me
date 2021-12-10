from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendEmail(receiver, bod):
    sender = "bubunda@tamu.edu"
    token = "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"

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject="New Job from Jobs4Me!",
        html_content=str(bod))

    try:
        sg = SendGridAPIClient(token)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
