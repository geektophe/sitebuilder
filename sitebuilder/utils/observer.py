#!/usr/bin/env python
"""
This module defines sever listener classes used at different applicaiton
levels.
"""

from sitebuilder.utils.event import Event


class DataChangedListener(object):
    """
    Listener object that may be called when a model data has been changed and
    an action is needed from other components to take it in account.
    """

    def data_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class DataChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch data changed
    events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._data_changed_listeners = []

    def add_data_changed_listener(self, listener):
        """
        Adds a DataChangedListener listener object to listeners list

        We may add a DataChangedListener instance

        >>> dispatcher = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> dispatcher.add_data_changed_listener(listener)

        Adding an object that is not a DataChangedListener should raise an
        exception

        >>> dispatcher = DataChangedDispatcher()
        >>> dispatcher.add_data_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of DataChangedListener
        """
        if not isinstance(listener, DataChangedListener):
            raise AttributeError(
                "Listener must be an instance of DataChangedListener")
        self._data_changed_listeners.append(listener)

    def remove_data_changed_listener(self, listener):
        """
        Deletes a DataChangedListener listener object to listeners list
        """
        try:
            self._data_changed_listeners.remove(listener)
        except ValueError:
            pass

    def clear_data_changed_listeners(self):
        """
        Deletes all DataChangedListener listeners object from listeners list
        """
        del self._data_changed_listeners[:]

    def notify_data_changed(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the DataChangedListener instance we use for the test is only used as
        an abstract class, the notify method should raise a NotImplementedError

        >>> dispatcher = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> dispatcher.add_data_changed_listener(listener)
        >>> dispatcher.notify_data_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_data_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_data_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._data_changed_listeners:
            listener.data_changed(event)


class ValidityChangedListener(object):
    """
    Listener object that may be called when a component value has been changed,
    its validity has changed and an action is needed from other components to
    take it in account.
    """

    def validity_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ValidityChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch validity
    changed events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._validity_changed_listeners = []

    def add_validity_changed_listener(self, listener):
        """
        Adds a ValidityChangedListener listener object to listeners list

        We may add a DataChangedListener instance

        >>> dispatcher = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> dispatcher.add_validity_changed_listener(listener)

        Adding an object that is not a ValidityChangedListener should raise an
        exception

        >>> dispatcher = ValidityChangedDispatcher()
        >>> dispatcher.add_validity_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ValidityChangedListener
        """
        if not isinstance(listener, ValidityChangedListener):
            raise AttributeError(
                "Listener must be an instance of ValidityChangedListener")
        self._validity_changed_listeners.append(listener)

    def remove_validity_changed_listener(self, listener):
        """
        Deletes a ValidityChangedListener listener object to listeners list
        """
        try:
            self._validity_changed_listeners.remove(listener)
        except ValueError:
            pass

    def clear_validity_changed_listeners(self):
        """
        Deletes all ValidityChangedListener listeners object from listeners list
        """
        del self._validity_changed_listeners[:]

    def notify_validity_changed(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the ValidityChangedListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> dispatcher.add_validity_changed_listener(listener)
        >>> dispatcher.notify_validity_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_validity_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_validity_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._validity_changed_listeners:
            listener.validity_changed(event)


class ViewActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def view_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ViewActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'view action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._view_action_activated_listeners = []

    def add_view_action_activated_listener(self, listener):
        """
        Adds a ViewActionListener listener object to listeners list

        We may add a ViewActionListener instance

        >>> dispatcher = ViewActionDispatcher()
        >>> listener = ViewActionListener()
        >>> dispatcher.add_view_action_activated_listener(listener)

        Adding an object that is not a ViewActionListener should raise an
        exception

        >>> dispatcher = ViewActionDispatcher()
        >>> dispatcher.add_view_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ViewActionListener
        """
        if not isinstance(listener, ViewActionListener):
            raise AttributeError(
                "Listener must be an instance of ViewActionListener")
        self._view_action_activated_listeners.append(listener)

    def remove_view_action_activated_listener(self, listener):
        """
        Deletes a ViewActionListener listener object to listeners list
        """
        try:
            self._view_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_view_action_activated_listeners(self):
        """
        Deletes all ViewActionActivatedListener listeners object from listeners
        list
        """
        del self._view_action_activated_listeners[:]

    def notify_view_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the ViewActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = ViewActionDispatcher()
        >>> listener = ViewActionListener()
        >>> dispatcher.add_view_action_activated_listener(listener)
        >>> dispatcher.notify_view_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_view_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_view_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._view_action_activated_listeners:
            listener.view_action_activated(event)


class AddActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def add_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class AddActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'add action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._add_action_activated_listeners = []

    def add_add_action_activated_listener(self, listener):
        """
        Adds a AddActionListener listener object to listeners list

        We may add a AddActionListener instance

        >>> dispatcher = AddActionDispatcher()
        >>> listener = AddActionListener()
        >>> dispatcher.add_add_action_activated_listener(listener)

        Adding an object that is not a AddActionListener should raise an
        exception

        >>> dispatcher = AddActionDispatcher()
        >>> dispatcher.add_add_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of AddActionListener
        """
        if not isinstance(listener, AddActionListener):
            raise AttributeError(
                "Listener must be an instance of AddActionListener")
        self._add_action_activated_listeners.append(listener)

    def remove_add_action_activated_listener(self, listener):
        """
        Deletes a AddActionListener listener object to listeners list
        """
        try:
            self._add_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_add_action_activated_listeners(self):
        """
        Deletes all AddActionActivatedListener listeners object from listeners
        list
        """
        del self._add_action_activated_listeners[:]

    def notify_add_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the AddActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = AddActionDispatcher()
        >>> listener = AddActionListener()
        >>> dispatcher.add_add_action_activated_listener(listener)
        >>> dispatcher.notify_add_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_add_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_add_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._add_action_activated_listeners:
            listener.add_action_activated(event)


class EditActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def edit_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class EditActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'edit action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._edit_action_activated_listeners = []

    def add_edit_action_activated_listener(self, listener):
        """
        Edits a EditActionListener listener object to listeners list

        We may edit a EditActionListener instance

        >>> dispatcher = EditActionDispatcher()
        >>> listener = EditActionListener()
        >>> dispatcher.add_edit_action_activated_listener(listener)

        Editing an object that is not a EditActionListener should raise an
        exception

        >>> dispatcher = EditActionDispatcher()
        >>> dispatcher.add_edit_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of EditActionListener
        """
        if not isinstance(listener, EditActionListener):
            raise AttributeError(
                "Listener must be an instance of EditActionListener")
        self._edit_action_activated_listeners.append(listener)

    def remove_edit_action_activated_listener(self, listener):
        """
        Deletes a EditActionListener listener object to listeners list
        """
        try:
            self._edit_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_edit_action_activated_listeners(self):
        """
        Deletes all EditActionActivatedListener listeners object from listeners
        list
        """
        del self._edit_action_activated_listeners[:]

    def notify_edit_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the EditActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = EditActionDispatcher()
        >>> listener = EditActionListener()
        >>> dispatcher.add_edit_action_activated_listener(listener)
        >>> dispatcher.notify_edit_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_edit_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_edit_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._edit_action_activated_listeners:
            listener.edit_action_activated(event)


class DeleteActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def delete_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class DeleteActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'delete action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._delete_action_activated_listeners = []

    def add_delete_action_activated_listener(self, listener):
        """
        Deletes a DeleteActionListener listener object to listeners list

        We may delete a DeleteActionListener instance

        >>> dispatcher = DeleteActionDispatcher()
        >>> listener = DeleteActionListener()
        >>> dispatcher.add_delete_action_activated_listener(listener)

        Deleteing an object that is not a DeleteActionListener should raise an
        exception

        >>> dispatcher = DeleteActionDispatcher()
        >>> dispatcher.add_delete_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of DeleteActionListener
        """
        if not isinstance(listener, DeleteActionListener):
            raise AttributeError(
                "Listener must be an instance of DeleteActionListener")
        self._delete_action_activated_listeners.append(listener)

    def remove_delete_action_activated_listener(self, listener):
        """
        Deletes a DeleteActionListener listener object to listeners list
        """
        try:
            self._delete_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_delete_action_activated_listeners(self):
        """
        Deletes all DeleteActionActivatedListener listeners object from
        listeners list
        """
        del self._delete_action_activated_listeners[:]

    def notify_delete_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the DeleteActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = DeleteActionDispatcher()
        >>> listener = DeleteActionListener()
        >>> dispatcher.add_delete_action_activated_listener(listener)
        >>> dispatcher.notify_delete_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_delete_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_delete_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._delete_action_activated_listeners:
            listener.delete_action_activated(event)


class SubmitActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def submit_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class SubmitActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'submit action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._submit_action_activated_listeners = []

    def add_submit_action_activated_listener(self, listener):
        """
        Submits a SubmitActionListener listener object to listeners list

        We may submit a SubmitActionListener instance

        >>> dispatcher = SubmitActionDispatcher()
        >>> listener = SubmitActionListener()
        >>> dispatcher.add_submit_action_activated_listener(listener)

        Submiting an object that is not a SubmitActionListener should raise an
        exception

        >>> dispatcher = SubmitActionDispatcher()
        >>> dispatcher.add_submit_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of SubmitActionListener
        """
        if not isinstance(listener, SubmitActionListener):
            raise AttributeError(
                "Listener must be an instance of SubmitActionListener")
        self._submit_action_activated_listeners.append(listener)

    def remove_submit_action_activated_listener(self, listener):
        """
        Submits a SubmitActionListener listener object to listeners list
        """
        try:
            self._submit_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_submit_action_activated_listeners(self):
        """
        Deletes all SubmitActionActivatedListener listeners object from
        listeners list
        """
        del self._submit_action_activated_listeners[:]

    def notify_submit_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the SubmitActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = SubmitActionDispatcher()
        >>> listener = SubmitActionListener()
        >>> dispatcher.add_submit_action_activated_listener(listener)
        >>> dispatcher.notify_submit_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_submit_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_submit_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._submit_action_activated_listeners:
            listener.submit_action_activated(event)


class CancelActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def cancel_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class CancelActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'cancel action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._cancel_action_activated_listeners = []

    def add_cancel_action_activated_listener(self, listener):
        """
        Submits a CancelActionListener listener object to listeners list

        We may cancel a CancelActionListener instance

        >>> dispatcher = CancelActionDispatcher()
        >>> listener = CancelActionListener()
        >>> dispatcher.add_cancel_action_activated_listener(listener)

        Submiting an object that is not a CancelActionListener should raise an
        exception

        >>> dispatcher = CancelActionDispatcher()
        >>> dispatcher.add_cancel_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of CancelActionListener
        """
        if not isinstance(listener, CancelActionListener):
            raise AttributeError(
                "Listener must be an instance of CancelActionListener")
        self._cancel_action_activated_listeners.append(listener)

    def remove_cancel_action_activated_listener(self, listener):
        """
        Submits a CancelActionListener listener object to listeners list
        """
        try:
            self._cancel_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_cancel_action_activated_listeners(self):
        """
        Deletes all CancelActionActivatedListener listeners object from
        listeners list
        """
        del self._cancel_action_activated_listeners[:]

    def notify_cancel_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the CancelActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = CancelActionDispatcher()
        >>> listener = CancelActionListener()
        >>> dispatcher.add_cancel_action_activated_listener(listener)
        >>> dispatcher.notify_cancel_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_cancel_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_cancel_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._cancel_action_activated_listeners:
            listener.cancel_action_activated(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
