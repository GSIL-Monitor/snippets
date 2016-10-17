# -*- coding: utf-8 -*-
import logging
import os



logger = logging.getLogger('parallelism')


class PoolFullError(Exception): pass


class Pool(object):

    def init(self, size, target, args, kwargs):
        raise NotImplementedError()


    def start(self):
        raise NotImplementedError()


    def reap(self):
        raise NotImplementedError()


class ProcessPool(Pool):

    workers = set()

    def init(self, size, target, title=None, *args, **kwargs):
        self.size = size
        self.target = target
        self.args = args
        self.kwargs = kwargs


    def _spawn_missing_worker(self):

        while len(self.workers) < self.size:
            logger.warning('missing worker, spawning new...')
            pid = os.fork()

            if pid:
                # parent
                self.workers.add(pid)
                return

            rv = self.target(*self.args, **self.kwargs)

            os._exit(rv or 0)


    def start(self):
        self._spawn_missing_worker()


    def reap(self):
        self._spawn_missing_worker()

        try:
            for i in range(len(self.workers)):
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid in self.workers:
                    self.workers.remove(pid)
        except ChildProcessError as err:
            pass
