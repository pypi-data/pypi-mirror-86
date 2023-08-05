# encoding: utf-8
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class DiazoView(BrowserView):

    def is_homepage(self):
        """
        Returns true if we are on navigation root
        """
        context_helper = getMultiAdapter((self.context, self.request), name='plone_context_state')
        return context_helper.is_portal_root()
