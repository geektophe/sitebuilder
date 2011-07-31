#!/usr/bin/env python
"""
Main list interface control agent
"""

from sitebuilder.utils.event import Event
from sitebuilder.presentation.gtk.list import ListPresentationAgent
from sitebuilder.utils.attribute import AttributeSet
from sitebuilder.control.detail import DetailMainControlAgent
from sitebuilder.abstraction.site import SiteConfigurationManager
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


class ListControlAgent(ViewActionListener, AddActionListener,
                       EditActionListener, DeleteActionListener,
                       SubmitActionListener, ViewActionDispatcher,
                       AddActionDispatcher, EditActionDispatcher,
                       DeleteActionDispatcher):
    """
    List main component control agent
    """

    def __init__(self):
        """
        Initializes control agent.
        """
        ViewActionDispatcher.__init__(self)
        AddActionDispatcher.__init__(self)
        EditActionDispatcher.__init__(self)
        DeleteActionDispatcher.__init__(self)
        self._presentation_agent = ListPresentationAgent(self)
        self._presentation_agent.add_view_action_activated_listener(self)
        self._presentation_agent.add_add_action_activated_listener(self)
        self._presentation_agent.add_edit_action_activated_listener(self)
        self._presentation_agent.add_delete_action_activated_listener(self)

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
        detail.add_submit_action_activated_listener(self)
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
            self.notify_delete_action_activated(Event(configuration))

    def view_action_activated(self, event=None):
        """
        ViewActionListerner trigger mmethod local implementation
        """
        selection = self.get_presentation_agent().get_selected_items()

        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration, True)

    def add_action_activated(self, event=None):
        """
        AddActionListerner trigger mmethod local implementation
        """
        configuration = SiteConfigurationManager.get_blank_configuration()
        self.show_detail_dialog(configuration)

    def edit_action_activated(self, event=None):
        """
        EditActionListerner trigger mmethod local implementation
        """
        selection = self.get_presentation_agent().get_selected_items()

        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
            self.show_detail_dialog(configuration)

    def delete_action_activated(self, event=None):
        """
        DeleteActionListerner trigger mmethod local implementation
        """
        selection = self.get_presentation_agent().get_selected_items()

        for identifier in selection:
            configuration = SiteConfigurationManager.get_configuration_by_id(identifier)
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

        # Destroyes presentation
        self.get_presentation_agent().destroy()


if __name__ == '__main__':
    control = ListControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
