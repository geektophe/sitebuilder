#!/usr/bin/env python
"""
Event bus class.

An event bus dispatches events to subscribers. Each subscriber is called a
callback function which is passed the event that is dispatched.

Subscribers subscribe to event types, as for exceptions.

A bus may dispatch several events of different types. A subscriber that
subsrcibed to an event type will be notified only if that particular event
type is dispatched.

An event bus may also be connected to an other event bus (as subscriber), and
dispatch events from connected bus to its own subscribers.

Any subscribed client may also be unsubscribed.

Class maching is done throug instanceof instruction. It is therefore possible
to achieve thin class matching, or broader by specifying a parent class.

Note that it is not possible to tell in which order subscribers will be called
in a bus when an event is dispatched. A code using an EventBus should never
rely on execution order in the bus.
"""

from sitebuilder.event.interface import IEvent


class BusError(Exception):
    """
    Error risen when an error occured in a bus routine.
    """


class EventBus(object):
    """
    Standard (local) event bus.

    An object may subscribe to an event type
    """

    def __init__(self):
        """
        Bus initialization.
        """
        self.subscribers = {}

    def subscribe(self, klass, callback):
        """
        Subscribe a callable to an event type (class).

        An already subscribed callback is ignored.

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        if not IEvent.implementedBy(klass):
            raise BusError('Invalid unsubscription, klass should implenent IEvent')

        if not self.subscribers.has_key(klass):
            self.subscribers[klass] = []

        if not callback in self.subscribers[klass]:
            self.subscribers[klass].append(callback)

    def unsubscribe(self, klass, callback):
        """
        Unsubscribe a callable from an event type (class).

        An already subscribed callback is ignored.

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        if not IEvent.implementedBy(klass):
            raise BusError('Invalid unsubscription, klass should implenent IEvent')

        if self.subscribers.has_key(klass):
            # Removes subscriber callback
            if callback in self.subscribers[klass]:
                self.subscribers[klass].remove(callback)

            # Cleans subscriber disctionnary
            if not len(self.subscribers[klass]):
                del self.subscribers[klass]

    def unsubscribe_all(self):
        """
        Unsubscribes all subscribers
        """
        del self.subscribers
        self.subscribers = {}
