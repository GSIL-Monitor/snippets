# -*- coding: utf-8 -*-

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

msg = MIMEText('test')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'h1391 disk 81%'
msg['From'] = 'ops@qianka.com'
msg['To'] = '18621504692@wo.cn'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
