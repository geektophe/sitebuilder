#!/usr/bin/env python
"""
Base controller class to be subclassed
"""

from sitebuilder.utils.observer import DataChangedListener
from sitebuilder.utils.observer import DataChangedDispatcher
from sitebuilder.utils.observer import ValidityChangedListener
from sitebuilder.utils.observer import ValidityChangedDispatcher


class BaseController(DataChangedDispatcher, DataChangedListener,
                     ValidityChangedDispatcher, ValidityChangedListener):
    """
    Base controller class to be subclassed
    """

    def __init__(self):
        """
        Base controller initialization
        """
        DataChangedDispatcher.__init__(self)
        ValidityChangedDispatcher.__init__(self)
