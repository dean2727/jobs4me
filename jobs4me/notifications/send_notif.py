from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
import sys

def sendPushBulletNotification(username, header, msg, token):
    try:
        pb = PushBullet(token)
        push = pb.push_note(header, msg)
        print("Push Bullet message successfully sent to user " + username)
    except:
        print("Could not send Push Bullet notification for user " + username)
