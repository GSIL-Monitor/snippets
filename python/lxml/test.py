# -*- coding: utf-8 -*-

from io import StringIO
from lxml import etree

with open('/tmp/a.html') as f:
    content = f.read()

content = '<html>%s</html>' % content



tree = etree.parse(StringIO(content))

r = tree.xpath('/html/div')

if len(r) > 0:
    print(etree.tostring(r[0], encoding='UTF-8').decode('UTF-8'))
