# -*- coding: utf-8 -*-
import logging
import os
import re
import sys


import yaml



PATTERN = re.compile("""
---(?P<header>.*)---
""", re.VERBOSE|re.MULTILINE|re.S)

logging.basicConfig(level=logging.DEBUG)


def main():

    for line in sys.stdin.readlines():
        filename = os.path.abspath(line.strip())

        with open(filename) as f:
            content = f.read()

        m = PATTERN.search(content)
        if m:
            _d = m.groupdict()
            header = _d['header'].strip()

            try:
                title = yaml.load(header).get('title')
            except yaml.error.YAMLError:
                logging.warning('no title found: %s' % filename)
                continue
            if title is None:
                logging.warning('no title found: %s' % filename)
                continue

            title = title.strip().strip("'")

            header = '---\ntitle: %s\n---\n' % title

            new_content = re.sub(PATTERN, header, content, re.M|re.S)

            with open(filename, 'w') as f:
                f.write(new_content)

        else:
            logging.warning('file has no header: %s' % filename)


if __name__ == '__main__':
    sys.exit(main())
