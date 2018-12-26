# -*- coding: utf-8 -*-
import argparse

import logging
from subprocess import Popen, PIPE
import time

import cipip as pyipip
import requests


LOGGER = logging.getLogger(__name__)


class STATE(object):
    INIT = 0
    OK = 1
    CHANGING = 2


class Aso100Scheduler(object):

    def __init__(self, options):
        self.options = options
        self.currentIp = ''
        self.previousIp = ''

        # self.state = STATE.INIT
        self.state = STATE.OK

        self.workCount = 0

        self.controlHandle = None
        self.proxyHandle = None

        # self.controlTunnel()

        self.ipip = None

    def controlTunnel(self):
        cmd = '/usr/bin/ssh -vTN {} -L 127.0.0.1:{}:127.0.0.1:{} {}@{}'
        identity = ''
        cmd = cmd.format(
            identity,
            self.options.local_proxy_port,
            self.options.remote_proxy_port,
            self.options.remote_user,
            self.options.remote_host,
        )
        self.controlHandle = p = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE)

    def oneRun(self):

        # FIXME: STATE == CHANGING 状态太久的话需要有个处理

        currentIp = self.getIp()
        LOGGER.error('currentIp: %s', currentIp)

        if not currentIp:
            return

        self.currentIp = currentIp

        if self.previousIp != self.currentIp:
            geo1 = self.geoip(self.previousIp)
            LOGGER.error('before %s %s', self.previousIp, geo1)
            geo2 = self.geoip(self.currentIp)
            LOGGER.error('after %s %s', self.currentIp, geo2)
            self.changePost()
            return

        if self.previousIp == self.currentIp:
            if self.needChange():
                LOGGER.error('>>> do change')
                if not self.changeIp():
                    LOGGER.error('!!! change req failed!!!')
            return

    def postRun(self):
        self.previousIp = self.currentIp

    def loop(self):

        while True:
            ip = self.getIp()
            if ip:
                break

        self.previousIp = ip

        while True:
            self.oneRun()
            self.postRun()
            self.doWork()

            time.sleep(3)

    def needChange(self):
        if self.state == STATE.CHANGING:
            LOGGER.error('>>> IN CHANGING, skip')
            return False

        if self.workCount >= 3:
            LOGGER.error('>>> workCount exceeded !!!')
            return True

        LOGGER.error('>>> no need to change')
        return False

    def changePost(self):
        self.state = STATE.OK
        self.workCount = 0

    def doWork(self):
        if self.state == STATE.CHANGING:
            LOGGER.error('!! IN CHANGING, skip work')
            return

        self.workCount += 1
        LOGGER.error('>> doWork, count: %s', self.workCount)

    def getIp(self):
        try:
            resp = requests.get(
                'http://127.0.0.1:3000/get-public-ip', timeout=15)
            if resp.status_code == 200:
                rv = resp.text.strip()
                return rv
        except requests.exceptions.Timeout as err:
            LOGGER.error('getIp timeout')
        except requests.exceptions.RequestException as err:
            LOGGER.exception(str(err))

        return ''

    def changeIp(self):
        rv = False
        try:
            resp = requests.get(
                'http://127.0.0.1:3000/change-public-ip', timeout=15)
            self.state = STATE.CHANGING
            rv = resp.status_code == 202
        except requests.exceptions.Timeout as err:
            LOGGER.error('changeIp timeout')
        except requests.exceptions.RequestException as err:
            LOGGER.exception(str(err))

        return rv

    def geoip(self, ip):
        db = self.options.ipipx_database
        rv = ''
        if not db:
            return rv

        if self.ipip is None:
            self.ipip = pyipip.IPIPXDatabase(db)

        rv = self.ipip.lookup(ip)
        return rv


ap = argparse.ArgumentParser()
ap.add_argument('--remote-host', default='tmp')
ap.add_argument('--identity-file')
ap.add_argument('--local-proxy-port', type=int, default=3000)
ap.add_argument('--remote-proxy-port', type=int, default=3000)
ap.add_argument('--remote-user', default='root')
ap.add_argument('--ipipx-database')

options = ap.parse_args()

scheduler = Aso100Scheduler(options)
# 需要等连接开始
# LOGGER.error('>>> wait tunnel to connect')
# time.sleep(5)
# LOGGER.error('>>> start work')
scheduler.loop()
