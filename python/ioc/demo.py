# -*- coding: utf-8 -*-
import pprint
from common import ctx
import boot

ctx.refresh()
print(pprint.pformat(ctx.beans))

ctx['Greeter'].greet()
