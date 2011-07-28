#!/usr/bin/env python
"""
Main list interface controller
"""

from sitebuilder.utils.event import Event
from sitebuilder.view.gtk.list import ListView
from sitebuilder.model.configuration import AttributeSet
from sitebuilder.controller.detail import DetailMainController
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.observer.viewaction import ViewActionListener
from sitebuilder.observer.viewaction import ViewActionDispatcher
from sitebuilder.observer.addaction import AddActionListener
from sitebuilder.observer.addaction import AddActionDispatcher
from sitebuilder.observer.editaction import EditActionListener
from sitebuilder.observer.editaction import EditActionDispatcher
from sitebuilder.observer.deleteaction import DeleteActionListener
from sitebuilder.observer.deleteaction import DeleteActionDispatcher
from sitebuilder.observer.submitaction import SubmitActionListener
import gtk


class ListController(ViewActionListener, AddActionListener, EditActionListener,
                     DeleteActionListener, SubmitActionListener,
                     ViewActionDispatcher, AddActionDispatcher,
                     EditActionDispatcher, DeleteActionDispatcher):
    """
    List main component controller
    """

    def __init__(self):
        """
        Initializes controller.
        """
        ViewActionDispatcher.__init__(self)
        AddActionDispatcher.__init__(self)
        EditActionDispatcher.__init__(self)
        DeleteActionDispatcher.__init__(self)
        self._view = ListView(self)
        self._view.add_view_action_activated_listener(self)
        self._view.add_add_action_activated_listener(self)
        self._view.add_edit_action_activated_listener(self)
        self._view.add_delete_action_activated_listener(self)

    def get_view(self):
        """
        Returns ListView view instance
        """
        return self._view

    def get_configuration_all(self):
        """
        Retrieves all the configuraiton items from the model
        """
        return ConfigurationManager.get_configuration_all()

    def show_detail_dialog(self, configuration, read_only=False):
        """
        Shows detail dialog for the specified configuration
        """
        detail = DetailMainController(configuration, read_only)
        detail.add_submit_action_activated_listener(self)
        view = detail.get_view()
        view.show()

    def show_delete_dialog(self, configuration):
        """
        Shows detail dialog for the specified configuration
        """
        conf_id = configuration['general']['id'].get_value()
        conf_name = configuration['general']['name'].get_value()

        dialog = gtk.MessageDialog(
            self._view.get_toplevel(),
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
            "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            self.notify_delete_action_activated(Event(configuration))

    def view_action_activated(self, event=None):
        """
        ViewActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration, True)

    def add_action_activated(self, event=None):
        """
        AddActionListerner trigger mmethod local implementation
        """
        configuration = ConfigurationManager.get_blank_configuration()
        self.show_detail_dialog(configuration)

    def edit_action_activated(self, event=None):
        """
        EditActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration)

    def delete_action_activated(self, event=None):
        """
        DeleteActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_delete_dialog(configuration)

    def submit_action_activated(self, event=None):
        """
        SubmitActionListerner trigger mmethod local implementation

        Here, event should contain the child configuration instance as context
        attribute.
        """
        if event is not None:
            context = event.get_context()

            if isinstance(context, AttributeSet):
                print "configuration submitted: %d" % \
                       context['general']['id'].get_value()

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Clears listeners lists
        self.clear_add_action_activated_listeners()
        self.clear_view_action_activated_listeners()
        self.clear_edit_action_activated_listeners()
        self.clear_delete_action_activated_listeners()

        # Destroyes view
        self.get_view().destroy()


if __name__ == '__main__':
    controller = ListController()
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
