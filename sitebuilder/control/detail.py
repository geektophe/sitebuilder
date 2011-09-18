#!/usr/bin/env python
"""
Site details related control components
"""

from sitebuilder.utils.event import Event
from sitebuilder.presentation.gtk.detail import DetailMainPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDatabasePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailGeneralPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailSitePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailRepositoryPresentationAgent
from sitebuilder.abstraction.site import SiteConfigurationManager
from sitebuilder.control.base import BaseControlAgent
from sitebuilder.observer.submitaction import SubmitActionListener
from sitebuilder.observer.submitaction import SubmitActionDispatcher
from sitebuilder.observer.cancelaction import CancelActionListener
import gtk

class DetailMainControlAgent(BaseControlAgent, SubmitActionListener,
                             SubmitActionDispatcher, CancelActionListener):
    """
    Site details main interface's control agent
    """

    def __init__(self, configuration, read_only):
        """
        ControlAgent initialization
        """
        BaseControlAgent.__init__(self)
        SubmitActionDispatcher.__init__(self)
        self._read_only = read_only
        self._configuration = configuration
        self._presentation_agent = DetailMainPresentationAgent(self)
        self._presentation_agent.add_submit_action_activated_listener(self)
        self._presentation_agent.add_cancel_action_activated_listener(self)
        self._slaves = []

        # Creates general component
        general = configuration.get_attribute('general')
        slave = DetailGeneralControlAgent(general, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('general', 'hbox_general',
                slave.get_presentation_agent())

        # Creates repository component
        repository = configuration.get_attribute('repository')
        slave = DetailRepositoryControlAgent(repository, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('repository', 'hbox_repository',
                slave.get_presentation_agent())

        # Creates site component
        website = configuration.get_attribute('website')
        slave = DetailSiteControlAgent(website, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('website', 'hbox_sites',
                slave.get_presentation_agent())

        # Creates database component
        database = configuration.get_attribute('database')
        slave = DetailDatabaseControlAgent(database, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('database',
                'hbox_databases', slave.get_presentation_agent())

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation

        As this class is not sensible to DataChanged events (only sub
        components are), because of DataCHangedListener dependcy, this method
        is nulled
        """
        pass

    def validity_changed(self, event=None):
        """
        ValidityChangedListerner trigger mmethod local implementation

        When a sub component has triggerd a state changed event, the mothod
        enbles or disables the presentation agent's OK button depending on each
        component's valid flag.
        """
        flag = True

        for slave in self._slaves:
            flag = flag and slave.get_validity_flag()

        self.get_presentation_agent().set_submit_state(flag)

    def submit_action_activated(self, event=None):
        """
        SubmitActionActivatedListerner trigger mmethod local implementation
        """
        if self._read_only is False:
            self.notify_submit_action_activated(Event(self._configuration))

        self.destroy()

    def cancel_action_activated(self, event=None):
        """
        SubmitActionActivatedListerner trigger mmethod local implementation
        """
        self.destroy()

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    def get_presentation_agent(self):
        """
        Returns presentation
        """
        return self._presentation_agent

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Destroyes slave components
        for slave in self._slaves:
            slave.destroy()

        # Clears listeners lists
        self.clear_data_changed_listeners()
        self.clear_validity_changed_listeners()
        self.clear_submit_action_activated_listeners()

        # Destroyes presentation
        self.get_presentation_agent().destroy()


class DetailBaseControlAgent(BaseControlAgent):
    """
    Generic sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        """
        Initializes control agent.

        The read_only attribute indocates to the presentation that none of then
        widgets should be sensitive. The user is then not allowed to change any
        value.
        """
        BaseControlAgent.__init__(self)
        self._read_only = read_only
        self._configuration = configuration
        self._presentation_agent = None
        configuration.add_data_changed_listener(self)

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_data_changed(event)

    def validity_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_validity_changed(event)

    def get_validity_flag(self):
        """
        Returns component's valididty flag
        """
        return self.get_presentation_agent().get_validity_flag()

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    def get_presentation_agent(self):
        """
        Returns local PresentationAgent implementation instance
        """
        return self._presentation_agent

    def get_configuratuon(self):
        """
        Returns configuration instance
        """
        return self._configuration

    def get_attribute_value(self, name):
        """
        Returns a configuration attribute value
        """
        return self._configuration.get_attribute(name).get_value()

    def set_attribute_value(self, name, value):
        """
        Returns a configuration attribute value
        """
        self._configuration.get_attribute(name).set_value(value)

    def get_platform_name(self):
        """
        Returns platform anme, that is in fact the configuration name
        """
        return self._configuration.get_name()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unsubscribes from configuration data changed events
        self._configuration.remove_data_changed_listener(self)

        # Clears listeners lists
        self.clear_data_changed_listeners()
        self.clear_validity_changed_listeners()

        # Destroyes presentation
        self.get_presentation_agent().destroy()


class DetailSiteControlAgent(DetailBaseControlAgent):
    """
    Site sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        DetailBaseControlAgent.__init__(self, configuration, read_only)
        self._presentation_agent = DetailSitePresentationAgent(self)
        self._presentation_agent.add_validity_changed_listener(self)


class DetailDatabaseControlAgent(DetailBaseControlAgent):
    """
    Database sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        DetailBaseControlAgent.__init__(self, configuration, read_only)
        self._presentation_agent = DetailDatabasePresentationAgent(self)
        self._presentation_agent.add_validity_changed_listener(self)


class DetailRepositoryControlAgent(DetailBaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        DetailBaseControlAgent.__init__(self, configuration, read_only)
        self._presentation_agent = DetailRepositoryPresentationAgent(self)
        self._presentation_agent.add_validity_changed_listener(self)


class DetailGeneralControlAgent(DetailBaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        DetailBaseControlAgent.__init__(self, configuration, read_only)
        self._presentation_agent = DetailGeneralPresentationAgent(self)
        self._presentation_agent.add_validity_changed_listener(self)

if __name__ == '__main__':
    config = SiteConfigurationManager.get_blank_configuration()
    control = DetailMainControlAgent(config, False)
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
