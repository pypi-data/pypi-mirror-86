from __future__ import print_function

from halo_app.classes import AbsBaseClass

class settingsx(AbsBaseClass):
    def __getattribute__(self, name):
        global flx

        from flask import current_app as app
        settings = app.config
        try:

            attr = settings.get(name)
            return attr
        except RuntimeError as e:
            print("settingsx=" + name + " error:" + str(e))
            return None
