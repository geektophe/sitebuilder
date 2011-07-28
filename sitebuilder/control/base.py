#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.observer.datachanged import DataChangedListener
from sitebuilder.observer.datachanged  import DataChangedDispatcher
from sitebuilder.observer.validitychanged  import ValidityChangedListener
from sitebuilder.observer.validitychanged  import ValidityChangedDispatcher


class BaseControlAgent(DataChangedDispatcher, DataChangedListener,
                       ValidityChangedDispatcher, ValidityChangedListener):
    """
    Base control Agent class to be subclassed
    """

    def __init__(self):
        """
        Base controller initialization
        """
        DataChangedDispatcher.__init__(self)
        ValidityChangedDispatcher.__init__(self)
