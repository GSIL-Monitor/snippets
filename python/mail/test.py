# -*- coding: utf-8 -*-

import smtplib

SERVER = "172.20.1.10"

FROM = "80x24@momoka.net"
TO = ["80x24@momoka.net"] # must be a list

SUBJECT = "Hello!"

TEXT = "This message was sent with Python's smtplib."

    # Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail

server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
