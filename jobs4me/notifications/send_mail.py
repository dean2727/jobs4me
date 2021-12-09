import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sender = sys.argv[1]
receiver = sys.argv[2]
token = sys.argv[3]
sub = sys.argv[4]
bod = sys.argv[5]
message = Mail(
    from_email=str(sender),
    to_emails=str(receiver),
    subject=str(sub),
    html_content=str(bod))

try:
    sg = SendGridAPIClient(token)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
