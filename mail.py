# -*- coding: utf-8 -*-
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL, SMTP
from settings import *

#from mail import send_email_qq
def send_email_qq(message):
    #qq邮箱smtp服务器
    smtp_server = QQ.get('smtpserver')

    hour = datetime.now().hour
    if hour in range(15):
        qq = QQ.get('qq')[0]
        #pwd为qq邮箱的授权码
        pwd = QQ.get('password')[0]
    else:
        qq = QQ.get('qq')[1]
        pwd = QQ.get('password')[1]
    # sender_qq为发件人的qq号码
    sender_qq = qq
    #发件人的邮箱
    sender_qq_mail = qq + '@qq.com'
    #收件人邮箱
    receiver = QQ.get('receive')
    #邮件的正文内容
    mail_content = message
    #邮件标题
    mail_title = '你现在在进行一项用python登录qq邮箱发邮件的测试'

    #ssl登录
    smtp = SMTP_SSL(smtp_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    # smtp.set_debuglevel(1)
    smtp.ehlo(smtp_server)
    smtp.login(sender_qq, pwd)
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = str(receiver)
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()


def send_email_ctrip(message):
    smtp_server = CTRIP.get('smtpserver')
    sender = CTRIP.get('sender')
    password = CTRIP.get('password')

    msg = MIMEText(message)

    msg['Subject'] = 'Email by Python'
    msg['From'] = CTRIP.get('ctrip')
    msg['To'] = CTRIP.get('ctrip')

    mailserver = SMTP(smtp_server, 25)
    mailserver.login(sender, password)
    mailserver.sendmail(msg['From'], [msg['To']], msg.as_string())
    mailserver.quit()
