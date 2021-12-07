from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
import sys

access_token = sys.argv[1]
data = "Hi " + str(sys.argv[2]) + " "
text = "The Message is "
for i in range(3, len(sys.argv)):
    text = text + " " + str(sys.argv[i])
pb = PushBullet(access_token)
push = pb.push_note(data, text)
print("Message successfully sent")
