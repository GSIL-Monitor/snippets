# -*- coding: utf-8 -*-
import io
import subprocess
import sys


class Capture(object):

    def __init__(self, **options):
        self.encoding = options.pop('encoding', 'utf-8')

    def __enter__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.out = sys.stdout = io.StringIO()
        self.err = sys.stderr = io.StringIO()
        return self

    def __exit__(self, cls, err, traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        self.out = self.out.getvalue().splitlines()
        self.err = self.err.getvalue().splitlines()

    def run(self, cmd, **options):
        options.pop('stdout', None)
        options.pop('stderr', None)

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
        stdout, stderr = p.communicate()
        code = p.returncode

        self.out.write(stdout.decode(self.encoding))
        self.err.write(stderr.decode(self.encoding))

        return stdout, stderr, code

    def free(self):
        del self.out
        del self.err


with Capture() as out:
    print('hello')
    out.run('ls')
    raise RuntimeError()

print(out.out)
print(out.err)
out.free()
