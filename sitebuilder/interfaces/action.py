#!/usr/bin/env python
"""
ActionActivated observer interace
"""

from zope.interface import Interface
from zope.schema import TextLine, Dict


class IAction(Interface):
    """
    Actionn asked in a GUI
    """
    name = TextLine(title=u"Action name", required=True, default=u'')
    parameters = Dict(title=u"Action parameters", required=True, default={})


class IActionObserver(Interface):
    """
    Observers methods are called on action activaee event.
    """

    def action_activated(self, action):
        """
        Observer method run on action avtivated event
        """

class IActionSubject(Interface):
    """
    Subject notify observers on action events
    """

    def register_action_observer(observer):
        """
        Adds a ActionActivatedObserver observer object to observers list
        """

    def remove_action_observer(observer):
        """
        Deletes a ActionActivatedObserver observer object to observers list
        """

    def clear_action_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_action_activated(action):
        """
        Notifies all observers that a data has changed
        """
