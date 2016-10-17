# -*- coding: utf-8 -*-
import functools
import plistlib
import pprint
import sys
import zipfile


fn = sys.argv[1]

with zipfile.ZipFile(fn) as z:
    a = functools.reduce(
        lambda a, b: len(a) < len(b) and a or b,
        filter(lambda x: 'Info.plist' in x, z.namelist())
    )
    with z.open(a) as f:
        p = f.read()

    pl = plistlib.loads(p)
    executable = pl['CFBundleExecutable']
    bundle_id = pl['CFBundleIdentifier']
    display_name = pl['CFBundleDisplayName']

    pprint.pprint(executable)
    pprint.pprint(bundle_id)
    pprint.pprint(display_name)
