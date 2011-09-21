#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.observer.attribute import AttributeChangedObserver
from sitebuilder.observer.attribute  import AttributeChangedSubject
from sitebuilder.observer.validitychanged  import ValidityChangedListener
from sitebuilder.observer.validitychanged  import ValidityChangedDispatcher


class BaseControlAgent(AttributeChangedSubject, AttributeChangedObserver,
                       ValidityChangedDispatcher, ValidityChangedListener):
    """
    Base control Agent class to be subclassed
    """

    def __init__(self):
        """
        Base controller initialization
        """
        AttributeChangedSubject.__init__(self)
        ValidityChangedDispatcher.__init__(self)
