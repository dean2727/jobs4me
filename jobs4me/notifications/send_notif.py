from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
import sys

def sendPushBulletNotification(username, header, msg, token):
    pb = PushBullet(token)
    push = pb.push_note(header, msg)
    print("Push bullet message successfully sent to user " + username)
