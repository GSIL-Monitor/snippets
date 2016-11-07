# -*- coding: utf-8 -*-
import logging
import signal
import sys
import time


logging.basicConfig(level=logging.DEBUG)

class Tester(object):

    def __init__(self):
        pass


    def start(self):
        self._quit = False

        def signal_handler(sig, frame):
            logging.error('signal: %s' % sig)
            if sig in (signal.SIGINT, signal.SIGTERM):
                # graceful exit
                logging.error('graceful shutdown...')
                self.quit()
            if sig in (signal.SIGQUIT,):
                # rudely exit
                logging.error('rudely shutdown, bye!')
                sys.exit(-1)

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGQUIT, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        return self

    def join(self):
        while self._quit is False:
            try:
                logging.error('sleep for 1 sec...')
                time.sleep(1)
            except KeyboardInterrupt:
                logging.error('KeyboardInterrupt detected, quit...')
                self.quit()
            except Exception as err:
                logging.exception('error')

    def quit(self):
        self._quit = True
        # maybe house keeping here



def main():

    t = Tester()
    t.start().join()
    return 0


if __name__ == '__main__':
    sys.exit(main())
