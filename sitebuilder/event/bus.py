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

    A bus is empty at initialization

    Let's declare a test subscriber class

    >>> class TestSubscriber(object):
    ...     notified = 0
    ...     def notify(self, event):
    ...         self.notified += 1
    ...     def clear(self):
    ...         self.notified = 0

    And two test event classes

    >>> from sitebuilder.event.events import BaseEvent

    >>> class TestEvent1(BaseEvent):
    ...     pass

    >>> class TestEvent2(BaseEvent):
    ...     pass

    Let's instantiate a bus

    >>> bus = EventBus()

    And a subscriber

    >>> subscr = TestSubscriber()
    >>> subscr.notified
    0

    Let's subscribe the subscriber to the bus for TestEvent2 events

    >>> bus.subscribe(TestEvent2, subscr.notify)

    If we dispatch a TestEvent1 event, subscriber should not have been
    notified.

    >>> bus.dispatch( TestEvent1(__name__) )
    >>> subscr.notified
    0

    If we dispatch a TestEvent2 event, it have been notified

    >>> bus.dispatch( TestEvent2(__name__) )
    >>> subscr.notified
    1

    If we subsrcibe the subscriber to both events, it should be notified both.

    >>> bus.subscribe(TestEvent1, subscr.notify)
    >>> subscr.clear()
    >>> bus.dispatch( TestEvent1(__name__) )
    >>> bus.dispatch( TestEvent2(__name__) )
    >>> subscr.notified
    2

    If we unsubscribe to subsrcriber from TestEvent2, it should be notified
    only once.

    >>> bus.unsubscribe(TestEvent2, subscr.notify)
    >>> subscr.clear()
    >>> bus.dispatch( TestEvent1(__name__) )
    >>> bus.dispatch( TestEvent2(__name__) )
    >>> subscr.notified
    1

    If we clear all subscribers, no the subscriber should not be notified
    anymore.

    >>> bus.unsubscribe_all()
    >>> subscr.clear()
    >>> bus.dispatch( TestEvent1(__name__) )
    >>> bus.dispatch( TestEvent2(__name__) )
    >>> subscr.notified
    0

    Let's create a second subscriber, and a second bus

    >>> bus2 = EventBus()
    >>> subscr2 = TestSubscriber()

    And let's connect bus2 to bus

    >>> bus.connect(bus2)

    Let's subscribe subscr2 to bus2

    >>> bus2.subscribe(TestEvent1, subscr2.notify)

    If we dispatch a TestEvent1 on bus, it should be redispatched on bus2, and
    subscr2 should be notified.

    >>> bus.dispatch( TestEvent1(__name__) )
    >>> subscr2.notified
    1

    If we disconnect bus2 from bus, evenst should not be redispatched anymore.

    >>> bus.disconnect(bus2)
    >>> subscr2.clear()
    >>> bus.dispatch( TestEvent1(__name__) )
    >>> subscr2.notified
    0
    """

    def __init__(self):
        """
        Bus initialization.
        """
        self.subscribers = {}
        self.followers = []

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

    def has_subscribed(self, klass, callback):
        """
        Tells if a callback has already subscribed to a scpecific event type
        (class).

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        return  self.subscribers.has_key(klass) and \
                callback in self.subscribers[klass]

    def connect(self, bus):
        """
        Connects an external bus. All dispatched events are re-dispatched on
        connected buses.
        """
        self.followers.append(bus)

    def disconnect(self, bus):
        """
        Disconnects an external bus. No furter events will follow.
        """
        self.followers.remove(bus)

    def is_connected(self, bus):
        """
        Tells if an external bus is connected.
        """
        return bus in self.followers

    def disconnect_all(self):
        """
        Disconnects all followers.
        """
        del self.followers
        self.followers = []

    def clear(self):
        """
        Totally clears a bus.
        """
        self.unsubscribe_all()
        self.disconnect_all()

    def dispatch(self, event):
        """
        Dispatches an event to subscribers.
        """
        if not IEvent.providedBy(event):
            raise BusError('Invalid dispatching, event should provide IEvent')

        # Dispatches event to subscribers
        if self.subscribers.has_key(type(event)):
            for subscriber in self.subscribers[type(event)]:
                subscriber(event)

        # Dispatches event to connected buses
        for follower in self.followers:
            follower.dispatch(event)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
