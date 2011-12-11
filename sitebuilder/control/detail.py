#!/usr/bin/env python
"""
Site details related control components
"""

from sitebuilder.presentation.gtk.detail import DetailMainPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDatabasePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDNSHostPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailSitePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailRepositoryPresentationAgent
from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from sitebuilder.interfaces.action  import IActionObserver
from sitebuilder.interfaces.action  import IActionSubject
from sitebuilder.observer.action  import Action, ActionSubject
from sitebuilder.control.base import BaseControlAgent
from sitebuilder.utils.parameters import ACTION_SUBMIT, ACTION_CANCEL
from zope.interface import implements
import gtk


class DetailMainControlAgent(BaseControlAgent, ActionSubject):
    """
    Site details main interface's control agent
    """
    implements(IActionObserver, IActionSubject)

    def __init__(self, site, read_only):
        """
        ControlAgent initialization
        """
        BaseControlAgent.__init__(self)
        ActionSubject.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailMainPresentationAgent(self)
        presentation_agent.register_action_observer(self)
        # Main detail presentation agent has no reason to listen to changed
        # attribute events. Disabled.
        # site.register_attribute_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)
        self._slaves = []

        # Creates general component
        slave = DetailDNSHostControlAgent(site.dnshost, read_only)
        self._slaves.append(slave)
        presentation_agent = slave.get_presentation_agent()
        self._presentation_agent.attach_slave('dnshost', 'hbox_general',
                slave.get_presentation_agent())

        # Creates repository component
        slave = DetailRepositoryControlAgent(site.repository, read_only)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('repository', 'hbox_repository',
                slave.get_presentation_agent())

        # Creates site component
        slave = DetailSiteControlAgent(site.website, read_only)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('website', 'hbox_sites',
                slave.get_presentation_agent())

        # Creates database component
        slave = DetailDatabaseControlAgent(site.database, read_only)
        self._slaves.append(slave)
        self._presentation_agent.attach_slave('database',
                'hbox_databases', slave.get_presentation_agent())

    def action_activated(self, action=None):
        """
        ActionPerformedObserver trigger mmethod local implementation
        """
        if action.name == ACTION_SUBMIT:
            # Informs upper component from the submit action
            # Adds site as parameter to event
            self.submit()
        elif action.name == ACTION_CANCEL:
            # No need to inform upper component
            self.cancel()
        else:
            raise NotImplementedError("Unhandled action %d triggered" % action)

    def submit(self):
        """
        The interface submit action has been asked.
        """
        self.notify_action_activated(Action(
            ACTION_SUBMIT,
            {'sites': [ self.get_site() ]} ))
        self.destroy()

    def cancel(self):
        """
        SubmitActionActivatedObserver trigger mmethod local implementation
        """
        self.destroy()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        self.get_presentation_agent().remove_action_observer(self)
        # Destroyes slave components
        for slave in self._slaves:
            slave.destroy()

        BaseControlAgent.destroy(self)


class DetailSiteControlAgent(BaseControlAgent):
    """
    Site sub component control agent
    """

    def __init__(self, site, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailSitePresentationAgent(self)
        site.register_attribute_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailDatabaseControlAgent(BaseControlAgent):
    """
    Database sub component control agent
    """

    def __init__(self, site, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailDatabasePresentationAgent(self)
        site.register_attribute_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailRepositoryControlAgent(BaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, site, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailRepositoryPresentationAgent(self)
        site.register_attribute_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)


class DetailDNSHostControlAgent(BaseControlAgent):
    """
    DNSHost sub component control agent
    """

    def __init__(self, site, read_only=False):
        BaseControlAgent.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailDNSHostPresentationAgent(self)
        site.register_attribute_observer(presentation_agent)
        self.set_presentation_agent(presentation_agent)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

if __name__ == '__main__':
    config = SiteConfigurationManager.get_blank_site()
    control = DetailMainControlAgent(config, False)
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
