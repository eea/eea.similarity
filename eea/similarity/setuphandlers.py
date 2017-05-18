# -*- coding: utf-8 -*-
""" setuphandlers
"""
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    """ Hidden Profiles"""

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'eea.similarity:uninstall',
        ]

def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
