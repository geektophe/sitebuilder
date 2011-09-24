#!/usr/bin/env python
"""
Site details related control components
"""

from sitebuilder.presentation.gtk.detail import DetailMainPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDatabasePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailGeneralPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailSitePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailRepositoryPresentationAgent
from sitebuilder.abstraction.site import SiteConfigurationManager
from sitebuilder.control.base import BaseControlAgent
import gtk

class DetailMainControlAgent(BaseControlAgent):
    """
    Site details main interface's control agent
    """

    def __init__(self, configuration, read_only):
        """
        ControlAgent initialization
        """
        BaseControlAgent.__init__(self)
        self.set_configuration(configuration)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailMainPresentationAgent(self)
        # Main detail presentation agent has no reason to listen to changed
        # attribute events. Disabled.
        # configuration.register_attribute_changed_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self._slaves = []

        # Creates general component
        general = configuration.get_attribute('general')
        slave = DetailGeneralControlAgent(general, read_only)
        slave.register_validity_changed_observer(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('general', 'hbox_general',
                slave.get_presentation_agent())

        # Creates repository component
        repository = configuration.get_attribute('repository')
        slave = DetailRepositoryControlAgent(repository, read_only)
        slave.register_validity_changed_observer(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('repository', 'hbox_repository',
                slave.get_presentation_agent())

        # Creates site component
        website = configuration.get_attribute('website')
        slave = DetailSiteControlAgent(website, read_only)
        slave.register_validity_changed_observer(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('website', 'hbox_sites',
                slave.get_presentation_agent())

        # Creates database component
        database = configuration.get_attribute('database')
        slave = DetailDatabaseControlAgent(database, read_only)
        slave.register_validity_changed_observer(self)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('database',
                'hbox_databases', slave.get_presentation_agent())

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

    def submit(self):
        """
        The interface submit action has been asked.
        """
        # TODO: implement message passing
        print "site configuration submitted"
        self.destroy()

    def cancel(self):
        """
        SubmitActionActivatedListerner trigger mmethod local implementation
        """
        self.destroy()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Destroyes slave components
        for slave in self._slaves:
            slave.destroy()

        BaseControlAgent.destroy(self)


class DetailSiteControlAgent(BaseControlAgent):
    """
    Site sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_configuration(configuration)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailSitePresentationAgent(self)
        configuration.register_attribute_changed_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self.get_presentation_agent().register_validity_changed_observer(self)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view fromconfiguration
        self.get_configuration().remove_attribute_changed_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailDatabaseControlAgent(BaseControlAgent):
    """
    Database sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_configuration(configuration)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailDatabasePresentationAgent(self)
        configuration.register_attribute_changed_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self.get_presentation_agent().register_validity_changed_observer(self)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view fromconfiguration
        self.get_configuration().remove_attribute_changed_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailRepositoryControlAgent(BaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_configuration(configuration)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailRepositoryPresentationAgent(self)
        configuration.register_attribute_changed_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self._presentation_agent.register_validity_changed_observer(self)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view fromconfiguration
        self.get_configuration().remove_attribute_changed_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailGeneralControlAgent(BaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, configuration, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_configuration(configuration)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailGeneralPresentationAgent(self)
        configuration.register_attribute_changed_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self._presentation_agent.register_validity_changed_observer(self)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view fromconfiguration
        self.get_configuration().remove_attribute_changed_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

if __name__ == '__main__':
    config = SiteConfigurationManager.get_blank_configuration()
    control = DetailMainControlAgent(config, False)
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
