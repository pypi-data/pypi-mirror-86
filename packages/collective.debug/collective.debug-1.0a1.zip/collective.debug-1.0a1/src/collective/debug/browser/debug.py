# -*- coding: utf-8 -*-


from Products.Five.browser import BrowserView
from collections import OrderedDict

import plone.api


class Debug(BrowserView):

    def get_instance_dict(self):
        result = OrderedDict()
        for k in sorted(self.context.__dict__.keys()):
            result[k] = self.context.__dict__[k]
        return result

    def isManager(self):
        return 'Manager' in plone.api.user.get_roles()

