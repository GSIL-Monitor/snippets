# -*- coding: utf-8 -*-
import builtins
import logging
import os

import pyinotify


LOGGER = logging.getLogger(__name__)


class CodeChangeEmitter(object):

    def __init__(self):
        self._parent = None

        wm = self.wm = pyinotify.WatchManager()

        mask = self.mask = (
            pyinotify.IN_DELETE |
            pyinotify.IN_CREATE |
            pyinotify.IN_MODIFY |
            pyinotify.IN_ATTRIB |
            pyinotify.IN_MOVED_FROM |
            pyinotify.IN_MOVED_TO
        )  # watched events

        handler = EventHandler(self)
        self.noti = pyinotify.ThreadedNotifier(wm, handler)
        path = os.getcwd()
        LOGGER.error('watching %s', path)
        wdd = wm.add_watch(path, mask, rec=True)

    def start(self):
        self.noti.start()

    def inject_import(self):
        _baseimport = builtins.__import__
        self.deps = _dependencies = dict()

        def _import(name, globals=None, locals=None, fromlist=None, level=-1):
            LOGGER.error('injected _import %s', name)
            # Track our current parent module.  This is used to find our current
            # place in the dependency graph.
            # global _parent
            bak = self._parent
            parent = name

            # Perform the actual import using the base import function.
            m = _baseimport(name, globals, locals, fromlist, level)
            if not m.__name__.startswith('hebe'):
                return m

            LOGGER.error(m)
            LOGGER.error('parent: %s', parent)

            # If we have a parent (i.e. this is a nested import) and this is a
            # reloadable (source-based) module, we append ourself to our parent's
            # dependency list.
            if parent is not None and hasattr(m, '__file__'):
                l = _dependencies.setdefault(parent, set())
                l.add(m)

            # Lastly, we always restore our global _parent pointer.
            self._parent = bak
            LOGGER.error('parent2: %s', parent)

            return m

        builtins.__import__ = _import
        LOGGER.error('builtins.__import__ injected')


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, emitter):
        self.emitter = emitter

    def detect(self, event):
        import pprint
        pprint.pprint(self.emitter.deps)

    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)
        self.detect(event)

    def process_IN_DELETE(self, event):
        print("Removing:", event.pathname)
        self.detect(event)

    def process_IN_MODIFY(self, event):
        print("Updated:", event.pathname)
        self.detect(event)

    def process_IN_ATTRIB(self, event):
        print("Attrib:", event.pathname)
        self.detect(event)

    def process_IN_MOVED_FROM(self, event):
        print("mv from:", event.pathname)
        self.detect(event)

    def process_IN_MOVED_TO(self, event):
        print("mv to:", event.pathname)
        self.detect(event)
