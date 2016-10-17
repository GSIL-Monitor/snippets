# -*- coding: utf-8 -*-
import errno
import os
import fcntl


def nb_fd_readline(fd):
    """non-blocking readline from fd

    Args:
        fd (int): file descriptor to read from

    Returns:
        string, int: line, status
            status: 0  a new line
            status: -1 not a new line
    """
    line = b''
    while True:
        try:
            _ = os.read(fd, 1)
            line += _
            if _ == b'\n':
                return line, 0
            if _ == b'\r':
                _ = os.read(fd, 1)
                return line, 0
        except OSError as e:
            try:
                if type(e) == BlockingIOError:
                    return line, -1
                else:
                    raise
            except NameError:
                if e.errno == errno.EAGAIN:
                    return line, -1
                else:
                    raise


def run_in_child(cmd):
    """run shell command in child process,
    non-blocking yields output.

    Args:
        cmd (string): command to run

    Returns:
        string, string, int: stderr, stderr and exit value,
            output would be ``None'',
            exit value should use the last one.

    """
    outr, outw = os.pipe()
    errr, errw = os.pipe()
    pid = os.fork()

    exitvalue = None
    if pid == 0:
        # child
        os.dup2(outw, 1)
        os.dup2(errw, 2)

        os.close(outr)
        os.close(outw)
        os.close(errr)
        os.close(errw)

        os.execl('/bin/bash', 'bash', '-c', cmd)
    else:
        f = fcntl.fcntl(outr, fcntl.F_GETFL)
        fcntl.fcntl(outr, fcntl.F_SETFL, f | os.O_NONBLOCK)
        f = fcntl.fcntl(errr, fcntl.F_GETFL)
        fcntl.fcntl(errr, fcntl.F_SETFL, f | os.O_NONBLOCK)

        outline = b''
        errline = b''
        while True:
            _, s = nb_fd_readline(outr)
            if _ and s == 0:
                outline += _
                yield outline.decode('UTF-8').strip(), None, exitvalue
                outline = b''
                continue
            if _ and s == -1:
                outline += _

            _, s = nb_fd_readline(errr)
            if _ and s == 0:
                errline += _
                yield None, errline.decode('UTF-8').strip(), exitvalue
                errline = b''
                continue
            if _ and s == -1:
                errline += _

            try:
                _pid, exitvalue = os.waitpid(-1, os.WNOHANG)
            except Exception as e:
                try:
                    if type(e) == ChildProcessError:
                        break
                    else:
                        raise
                except NameError:
                    if e.errno == errno.ECHILD:
                        break
                    else:
                        raise

        outline = b''
        while True:
            _, s = nb_fd_readline(outr)
            if _ and s == 0:
                outline += _
                yield outline.decode('UTF-8').strip(), None, exitvalue
                outline = b''
                continue
            if _ and s == -1:
                outline += _
            if not _:
                yield outline.decode('UTF-8').strip(), None, exitvalue
                break
        errline = b''
        while True:
            _, s = nb_fd_readline(errr)
            if _ and s == 0:
                errline += _
                yield None, errline.decode('UTF-8').strip(), exitvalue
                errline = b''
                continue
            if _ and s == -1:
                errline += _
            if not _:
                yield None, errline.decode('UTF-8').strip(), exitvalue
                break


def local(cmd, quiet=False, _raise=True):
    """run local command, prints output non-blocking

    Args:
        cmd (string): command to run
        quiet (bool): whether to surpress output
        _raise (bool): whether to raise RuntimeError when exit value is not 0
    """
    line = ''
    exitvalue = 0
    for outline, errline, exitvalue in run_in_child(cmd):
        if not quiet and outline:
            print(outline)
        if not quiet and errline:
            print(errline)

    if exitvalue != 0:
        raise RuntimeError('run local command failed: %s' % cmd)


import threading
t1 = threading.Thread(target=local, args=('python -u sleep.py',))
t2 = threading.Thread(target=local, args=('python -u sleep.py',))

t1.start()
t2.start()
t1.join()
t2.join()
