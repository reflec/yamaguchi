from flask_mail import Message
from app import mail
from .decorators import async
from flask import render_template
from config import ADMINS
from threading import Thread
from app import app

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject,sender, recipients ,text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body  = text_body
    msg.html  = html_body
    mail.send(msg)
    thr = Thread(target=send_async_email,args=[app,msg])
    