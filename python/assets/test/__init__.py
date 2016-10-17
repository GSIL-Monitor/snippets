# -*- coding: utf-8 -*-
import os

import qianka.flaskext

class App(qianka.flaskext.QKFlask):

    def __init__(self):
        super(App, self).__init__(
            __name__,
            static_folder=os.path.abspath(
                os.path.dirname(__file__) + '/static',
            ),
            bower_components_folder='../bower_components',
        )

    def prepare(self):
        self.prepare_templates()
        self.prepare_webassets()

        import test.controllers.index


app = App()
