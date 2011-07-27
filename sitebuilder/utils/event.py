#!/usr/bin/env python
"""
Event class that may be used in event driven programming
"""

class Event(object):
    """
    A standtard event. The envent context can be retrieved using the
    get_context method.
    """

    def __init__(self, context):
        """
        Event initialization. Context is generally the object that generated
        the event.
        """
        self._context = context

    def get_context(self):
        """
        Returns event's context
        """
        return self._context
