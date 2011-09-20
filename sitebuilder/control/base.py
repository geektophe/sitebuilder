#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.observer.attribute import AttributeModifiedObserver
from sitebuilder.observer.attribute  import AttributeModifiedSubject
from sitebuilder.observer.validitychanged  import ValidityChangedListener
from sitebuilder.observer.validitychanged  import ValidityChangedDispatcher


class BaseControlAgent(AttributeModifiedSubject, AttributeModifiedObserver,
                       ValidityChangedDispatcher, ValidityChangedListener):
    """
    Base control Agent class to be subclassed
    """

    def __init__(self):
        """
        Base controller initialization
        """
        AttributeModifiedSubject.__init__(self)
        ValidityChangedDispatcher.__init__(self)
