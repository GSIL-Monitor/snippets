# -*- coding: utf-8 -*-
import subprocess
import sys
import threading


class ThreadHandler(object):

    def __init__(self, fo):
        self.fo = fo
        self.data = ''
        self.start()
        self.exception = None

    def loop(self):

        while True:
            print(self.fo.read(1))

    def start(self):

        def wrapper(*args, **kwargs):
            try:
                self.loop()
            except BaseException:
                self.exception = sys.exc_info()

        t = threading.Thread(target=wrapper)
        t.setDaemon(True)
        self.t = t
        t.start()

    def raise_if_needed(self):
        if self.exception:
            e = self.exception
            print(e)
            raise e


def local(command):

    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )

    to = ThreadHandler(p.stdout)
    to.start()

    te = ThreadHandler(p.stdout)
    te.start()

    (stdout, stderr) = p.communicate()

    to.t.join()
    to.raise_if_needed()
    te.t.join()
    te.raise_if_needed()

    return to.data, te.data, p.returncode


o, e, c = local('echo 1; sleep 1; echo 2; sleep 1; echo 3;')

print(o)
