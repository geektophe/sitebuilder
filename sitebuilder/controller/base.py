#!/usr/bin/env python
"""
Base controller class to be subclassed
"""

from sitebuilder.utils.observer import DataChangedListener
from sitebuilder.utils.observer import DataChangedDispatcher


class BaseController(DataChangedDispatcher, DataChangedListener):
    """
    Base controller class to be subclassed
    """

    def __init__(self):
        """
        Base controller initialization
        """
        DataChangedDispatcher.__init__(self)
