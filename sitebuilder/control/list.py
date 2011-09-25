#!/usr/bin/env python
"""
Main list interface control agent
"""

from sitebuilder.presentation.gtk.list import ListPresentationAgent
from sitebuilder.control.detail import DetailMainControlAgent
from sitebuilder.abstraction.site import SiteConfigurationManager
from sitebuilder.observer.action import ActionPerformedObserver
import gtk


class ListControlAgent(ActionPerformedObserver):
    """
    List main component control agent
    """

    def __init__(self):
        """
        Initializes control agent.
        """
        self._presentation_agent = ListPresentationAgent(self)
        self._presentation_agent.register_action_performed_observer(self)

    def action_performed(self, event=None):
        """
        ActionPerformedObserver trigger mmethod local implementation
        """
        action = event.get_name()

        # Handles add action that do nat need any parameter
        if action == 'add':
            self.add_site()
            return

        # Checks that ids parameter is correctly set in event parameters
        parms = event.get_parameters()

        if not parms.has_key('ids'):
            raise AttributeError('ids parameter is not set in action parameters')

        # Handles view action
        if action == 'view':
            self.view_selected_sites(parms['ids'])
        elif action == 'edit':
            self.edit_selected_sites(parms['ids'])
        elif action == 'delete':
            self.delete_selected_sites(parms['ids'])
        else:
            raise NotImplementedError("Unhandled action %d triggered" % action)

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def get_configuration_all(self):
        """
        Retrieves all the configuraiton items from the abstraction
        """
        return SiteConfigurationManager.get_configuration_all()

    def show_detail_dialog(self, configuration, read_only=False):
        """
        Shows detail dialog for the specified configuration
        """
        detail = DetailMainControlAgent(configuration, read_only)
        presentation = detail.get_presentation_agent()
        presentation.show()

    def show_delete_dialog(self, configuration):
        """
        Shows detail dialog for the specified configuration
        """
        conf_id = configuration['general']['id'].get_value()
        conf_name = configuration['general']['name'].get_value()

        dialog = gtk.MessageDialog(
            self.get_presentation_agent().get_toplevel(),
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
            "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            print "deleted site id %s" % conf_id 

    def add_site(self):
        """
        Display detail dialog in add mode with a new site configuration
        """
        configuration = SiteConfigurationManager.get_blank_configuration()
        self.show_detail_dialog(configuration)

    def view_selected_sites(self, selection):
        """
        Display detail dialog in view mode for each selected configuration id
        """
        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration, True)

    def edit_selected_sites(self, selection):
        """
        Display detail dialog in edit mode for each selected configuration id
        """
        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration)

    def delete_selected_sites(self, selection):
        """
        Display delete dialog for each selected configuration id
        """
        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
            self.show_delete_dialog(configuration)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes presentation
        self._presentation_agent.register_action_performed_observer(self)
        self._presentation_agent.destroy()


if __name__ == '__main__':
    control = ListControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
