#!/usr/bin/env python
"""
Main list interface controller
"""

from sitebuilder.view.gtk.list import ListView
from sitebuilder.controller.detail import DetailMainController
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.utils.observer import ViewActionListener
from sitebuilder.utils.observer import AddActionListener
from sitebuilder.utils.observer import EditActionListener
from sitebuilder.utils.observer import DeleteActionListener
from sitebuilder.utils.observer import SubmitActionListener
from sitebuilder.utils.observer import ViewActionDispatcher
from sitebuilder.utils.observer import AddActionDispatcher
from sitebuilder.utils.observer import EditActionDispatcher
from sitebuilder.utils.observer import DeleteActionDispatcher
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
            print "delete"

    def view_action_activated(self):
        """
        ViewActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration, True)

    def add_action_activated(self):
        """
        AddActionListerner trigger mmethod local implementation
        """
        configuration = ConfigurationManager.get_blank_configuration()
        self.show_detail_dialog(configuration)

    def edit_action_activated(self):
        """
        EditActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration)

    def delete_action_activated(self):
        """
        DeleteActionListerner trigger mmethod local implementation
        """
        selection = self._view.get_selected_items()

        for identifier in selection:
            configuration = ConfigurationManager.get_configuration_by_id(identifier)
            self.show_delete_dialog(configuration)


if __name__ == '__main__':
    controller = ListController()
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
