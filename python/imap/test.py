# -*- coding: utf-8 -*-

import imaplib

mail = imaplib.IMAP4_SSL('imap.anjuke.com', 993)
mail.login('chenlei@anjuke.com', '123anjuke')
a = mail.list()
mail.select('Sent')

result, data = mail.search(None, 'ALL')
ids = data[0]
id_list = ids.split()
lid = id_list[-1]

result, data = mail.fetch(lid, "(RFC822)")

print(data)
