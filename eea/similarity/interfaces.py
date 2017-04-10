# -*- coding: utf-8 -*-
""" Module where all interfaces, events and exceptions live.
"""
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.similarity.controlpanel.interfaces import IEEASimilaritySettings


class IEeaSimilarityLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

__all__ = [
    IEeaSimilarityLayer.__name__,
    IEEASimilaritySettings.__name__,
]
