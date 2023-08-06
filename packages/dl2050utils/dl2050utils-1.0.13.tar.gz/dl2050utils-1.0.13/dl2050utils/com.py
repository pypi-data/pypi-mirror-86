import os, re
from os.path import basename
import json
import socket
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from multiprocessing import Process
import boto3


default_address_book = {
    'jneto': {'email': 'joao.filipe.neto@gmail.com', 'phone': '+351966221506'},
    'jranito': {'email': 'joao.vasco.ranito@gmail.com', 'phone': '+351966221505'},
}

def read_address_book():
    try:
        with open('./.addressbook') as f:
            d = json.loads(f.read())
    except IOError:
        return None
    return d


#https://realpython.com/python-send-email/
def send_mail_async(email_id, email_passwd, to, subject=None, message=None, html=None, files=[]):
    p = Process(target=send_mail, args=(email_id, email_passwd, to, subject, message, html, files), daemon=True)
    p.start()

def send_mail(email_id, email_passwd, to, subject=None, message=None, html=None, files=[]):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject if subject is not None else ''
    if not type(to) is list:
        to = [to]
    msg['To'] = ', '.join(to)
    msg['From'] = email_id
    body = MIMEText(message, "plain") if html is None else MIMEText(html, 'html')
    msg.attach(body)
    for file in files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        arg = 'attachment; filename="' + basename(file) + '"'
        part.add_header('Content-Disposition', arg)
        msg.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        try:
            res = server.login(email_id, email_passwd)
            res = server.sendmail(email_id, to, msg.as_string())
        except Exception as e:
            return f'Mail sender ERROR: {str(e)}'
    return None


def send_sms_aws(sms_id, sms_passwd, to, msg):
    MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String','StringValue': 'DLOPS'}}
    client = boto3.client('sns', aws_access_key_id=sms_id, aws_secret_access_key=sms_passwd, region_name="eu-west-1")
    client.publish(PhoneNumber=to, Message=msg, MessageAttributes=MessageAttributes)
    return None

#from twilio.rest import Client
#def send_sms_twilio(sms_id, sms_passwd, to, msg):
#    #account_sid, auth_token
#    client = Client(sms_id, sms_passwd)
#    message = client.messages.create(to=to, from_='DLbot', body=msg)
#    #print(message.sid)
#    return None

def send_sms(sms_id, sms_passwd, to, msg):
    return send_sms_aws(sms_id, sms_passwd, to, msg)


class Notify():
    def __init__(self, cfg=None, email_id=None, email_passwd=None, sms_id=None, sms_passwd=None, address_book=None):
        self.address_book = address_book if address_book is not None else default_address_book
        if cfg is not None:
            try:
                email_id = cfg['email']['user']
                email_passwd = cfg['email']['passwd']
                sms_id = cfg['aws']['aws_access_key_id']
                sms_passwd = cfg['aws']['aws_secret_access_key']
            except Exception as e:
                print(f'Config ERROR: cant find variable: {e}')
        self.email_id = email_id
        self.email_passwd = email_passwd
        self.sms_id = sms_id
        self.sms_passwd = sms_passwd
        
    def __call__(self, who, how='mail', subject=None, message=None, html=None, files=[]):
        if who is None or who not in self.address_book:
            return 'Destination not found in address book'
        if how=='email' or how=='email_async':
            if self.email_id is None or self.email_passwd is None:
                return 'email credentials not defined'
            if 'email' not in self.address_book[who]:
                return f'email address not found for {who}'
            to = self.address_book[who]['email']
        if how=='sms':
            if self.sms_id is None or self.sms_passwd is None:
                return 'sms credentials not defined'
            if 'phone' not in self.address_book[who]:
                return f'phone number not found for {who}'
            to = self.address_book[who]['phone']
        if message is None:
            return 'Nothing to notify'
        if how == 'email':
            return send_mail(self.email_id, self.email_passwd, to, subject=subject, message=message,
                             html=html, files=files)
        if how == 'email_async':
            return send_mail_async(self.email_id, self.email_passwd, to, subject=subject, message=message,
                                   html=html, files=files)
        if how == 'sms':
            return send_sms(self.sms_id, self.sms_passwd, to, message)
        return 'Invalid method, options are email, email_async or sms'
    
    def send_mail_async(self, to, subject=None, message=None, html=None, files=[]):
        send_mail_async(self.email_id, self.email_passwd, to, subject=subject, message=message,
                             html=html, files=files)
    
    def send_mail(self, to, subject=None, message=None, html=None, files=[]):
        return send_mail(self.email_id, self.email_passwd, to, subject=subject, message=message,
                             html=html, files=files)

EMAIL_TEMPLATE = \
"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Muli::100,200,300,400,500,600,700,800" rel="stylesheet">
</head>
    <body style="position: relative; float: left; width: 100%; height: 100%;  text-align: center; font-family: 'Muli', sans-serif;">
        <h1 style="float: left; width: 100%; margin: 20px 0px; font-size: 28px; text-align: center; color: #555555;">{title}</h1>
                <h2 style="float: left; width: 100%; margin: 40px 0px 10px 0px; font-size: 16px; text-align: center; color: #555555;">Activation Key:</h2>
        <h2 style="float: left; width: 100%; margin: 0px 0px 40px 0px; font-size: 24px; text-align: center; color: #61C0DF; font-weight: bold;">{ukey}</h2>
        <a  style="display: inline-block; width: 200px; height: 35px; margin: 20px auto 50px auto; padding-top: 15px; border-radius: 10px;
        background: #61C0DF; text-align: center; color: #FFFFFF; text-decoration: none;" href="{href}">SET PASSWORD</a>
    </body>
</html>
"""

def send_ukey_by_email(notify, email, host, ukey, product):
    try:
        subject = f'{product} set password'
        title = f'{product} set password'
        href = f'http://{host}/login/set_passwd?ukey={ukey}'
        html = EMAIL_TEMPLATE
        html = re.sub(r'{title}', title, html)
        html = re.sub(r'{ukey}', f'{ukey}', html)
        html = re.sub(r'{href}', f'{href}', html)
        notify.send_mail_async(email, subject=subject, html=html)
    except Exception as e:
        return str(e)
    return None


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP