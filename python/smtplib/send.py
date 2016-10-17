# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

s = smtplib.SMTP_SSL('smtp.exmail.qq.com')
print(s.helo())
print(s.ehlo())

print(s.login('postmaster@qianka.com', 'QIANKApassw0rd'))
m = MIMEText('hello world')
m['Subject'] = 'test subject'
m['To'] = 'chen.lei@qianka.com'
m['From'] = 'Qianka OPS <postmaster@qianka.com>'

# print(s.send_message(m))
