# -*- coding: utf-8 -*-

accesslog = "-"
access_log_format = ("%(t)s	%(s)s	%(D)s	"
                     "%(h)s	%({X-Forwarded-For}i)s	"
                     "%(r)s	%(b)s	%(f)s	%(a)s")
workers = 4
bind = ['127.0.0.1:8000', '127.0.0.1:5000']
proc_name = "test"
