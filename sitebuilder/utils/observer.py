#!/usr/bin/env python
"""
This module defines sever listener classes used at different applicaiton
levels.
"""

class DataChangedListener(object):
    """
    Listener object that may be called when a model data has been changed and
    an action is needed from other components to take it in account.
    """

    def data_changed(self):
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
        Adds a DataChangedListener listener boject to listeners list

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
        Deletes a DataChangedListener listener boject to listeners list
        """
        try:
            self._data_changed_listeners.remove(listener)
        except ValueError:
            pass

    def notify_data_changed(self):
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
        """
        for listener in self._data_changed_listeners:
            listener.data_changed()


class ValidityChangedListener(object):
    """
    Listener object that may be called when a component value has been changed,
    its validity has changed and an action is needed from other components to
    take it in account.
    """

    def validity_changed(self):
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
        Adds a ValidityChangedListener listener boject to listeners list

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
        Deletes a ValidityChangedListener listener boject to listeners list
        """
        try:
            self._validity_changed_listeners.remove(listener)
        except ValueError:
            pass

    def notify_validity_changed(self):
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
        """
        for listener in self._validity_changed_listeners:
            listener.validity_changed()


class ViewActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def view_action_activated(self):
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
        Adds a ViewActionListener listener boject to listeners list

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
        Deletes a ViewActionListener listener boject to listeners list
        """
        try:
            self._view_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def notify_view_action_activated(self):
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
        """
        for listener in self._view_action_activated_listeners:
            listener.view_action_activated()


class AddActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def add_action_activated(self):
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
        Adds a AddActionListener listener boject to listeners list

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
        Deletes a AddActionListener listener boject to listeners list
        """
        try:
            self._add_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def notify_add_action_activated(self):
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
        """
        for listener in self._add_action_activated_listeners:
            listener.add_action_activated()


class EditActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def edit_action_activated(self):
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
        Edits a EditActionListener listener boject to listeners list

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
        Deletes a EditActionListener listener boject to listeners list
        """
        try:
            self._edit_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def notify_edit_action_activated(self):
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
        """
        for listener in self._edit_action_activated_listeners:
            listener.edit_action_activated()


class DeleteActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def delete_action_activated(self):
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
        Deletes a DeleteActionListener listener boject to listeners list

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
        Deletes a DeleteActionListener listener boject to listeners list
        """
        try:
            self._delete_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def notify_delete_action_activated(self):
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
        """
        for listener in self._delete_action_activated_listeners:
            listener.delete_action_activated()


class SubmitActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def submit_action_activated(self):
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
        Submits a SubmitActionListener listener boject to listeners list

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
        Submits a SubmitActionListener listener boject to listeners list
        """
        try:
            self._submit_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def notify_submit_action_activated(self):
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
        """
        for listener in self._submit_action_activated_listeners:
            listener.submit_action_activated()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
