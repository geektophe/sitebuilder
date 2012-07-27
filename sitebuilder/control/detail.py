#!/usr/bin/env python
"""
Site details related control components
"""

from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.presentation.gtk.detail import DetailMainPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDatabasePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailDNSHostPresentationAgent
from sitebuilder.presentation.gtk.detail import DetailSitePresentationAgent
from sitebuilder.presentation.gtk.detail import DetailRepositoryPresentationAgent
from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from sitebuilder.observer.attribute import IAttributeObserver
from sitebuilder.observer.action import IActionObserver, IActionSubject
from sitebuilder.observer.action import Action, ActionSubject
from sitebuilder.observer.validity import ValiditySubject, IValidityObserver
from sitebuilder.observer.validity import ValidityChangedEvent
from sitebuilder.observer.widget import IWidgetObserver
from sitebuilder.control.base import BaseControlAgent
from sitebuilder.exception import FieldFormatError
from zope.schema import ValidationError
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


class DetailBaseControlAgent(BaseControlAgent, ValiditySubject):
    """
    Base control agent class providing methods useful for
    DetailMainControlAgent childs.
    """

    implements(IAttributeObserver, IWidgetObserver)

    def __init__(self):
        BaseControlAgent.__init__(self)
        ValiditySubject.__init__(self)

    def widget_changed(self, name, value):
        """
        Observer method run on widget changed event

        Name is the name of the widget that triggerd the event, value is the
        value it was set to.
        """
        pa = self.get_presentation_agent()

        try:
            setattr(self.get_site(), name, value)
        except (ValidationError, FieldFormatError), e:
            pa.set_error(name, True, str(e))
            self.notify_validity_changed(ValidityChangedEvent(False, id(self)))
        else:
            pa.set_error(name, False)
            self.load_widgets_data()
            self.notify_validity_changed(ValidityChangedEvent(True, id(self)))

    def attribute_changed(self, attribute=None):
        """
        AttributeChangedObserver trigger mmethod local implementation
        """
        self.load_widgets_data()


class DetailSiteControlAgent(DetailBaseControlAgent):
    """
    Site sub component control agent
    """

    implements(IAttributeObserver, IWidgetObserver)

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        site.register_attribute_observer(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailSitePresentationAgent(self)
        pa.register_widget_observer(self)
        # Loads comboboxes items
        pa.set_items('template', SiteDefaultsManager.get_site_templates())
        pa.set_items('access', SiteDefaultsManager.get_site_accesses())
        self.set_presentation_agent(pa)
        # Initializes widget values
        self.load_widgets_data()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        site = self.get_site()
        site.remove_attribute_observer(self)

        enabled = self.get_value('enabled')
        done = self.get_value('done')
        read_only = self.get_read_only()
        sensitive = enabled and not done and not read_only

        # Loads enabled checkbox state
        pa.set_value('enabled', enabled)
        pa.set_enabled('enabled', not done and not read_only)

        # Loads maintenance checkbox state
        maintenance = self.get_value('maintenance')
        pa.set_value('maintenance', maintenance)
        # Maintenance should be changeable even if site is in done state
        pa.set_enabled('maintenance', enabled and not read_only)

        # Loads template combobox state
        template = self.get_value('template')
        pa.set_value('template', template)
        pa.set_enabled('template', sensitive)

        # Loads access combobox state
        access = self.get_value('access')
        pa.set_value('access', access)
        # Access should be changeable even if site is in done state
        pa.set_enabled('access', enabled and not read_only)

        site.register_attribute_observer(self)


class DetailDatabaseControlAgent(DetailBaseControlAgent):
    """
    Database sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        site.register_attribute_observer(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailDatabasePresentationAgent(self)
        pa.register_widget_observer(self)
        # Loads comboboxes items
        pa.set_items('type', SiteDefaultsManager.get_database_types())
        self.set_presentation_agent(pa)
        # Initializes widget values
        self.load_widgets_data()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        site = self.get_site()
        site.remove_attribute_observer(self)

        enabled = self.get_value('enabled')
        done = self.get_value('done')
        read_only = self.get_read_only_flag()
        sensitive = enabled and not done and not read_only

        # Loads enabled checkbox state
        pa.set_value('enabled', enabled)
        pa.set_enabled('enabled', not done and not read_only)

        # Loads name entry
        name = self.get_value('name')
        pa.set_value('name', name)
        pa.set_enabled('name', sensitive)

        # Loads username entry
        username = self.get_value('username')
        pa.set_value('username', username)
        pa.set_enabled('username', sensitive)

        # Loads password entry
        password = self.get_value('password')
        pa.set_value('password', password)
        pa.set_enabled('password', sensitive)

        # Loads type combobox selected option
        dbtype = self.get_value('type')
        pa.set_value('type', dbtype)
        pa.set_enabled('type', sensitive)

        site.register_attribute_observer(self)


class DetailRepositoryControlAgent(DetailBaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        site.register_attribute_observer(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailRepositoryPresentationAgent(self)
        pa.register_widget_observer(self)
        # Loads comboboxes items
        pa.set_items('type', SiteDefaultsManager.get_repository_types())
        self.set_presentation_agent(pa)
        # Initializes widget values
        self.load_widgets_data()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        site = self.get_site()
        site.remove_attribute_observer(self)

        enabled = self.get_value('enabled')
        done = self.get_value('done')
        read_only = self.get_read_only_flag()
        sensitive = enabled and not done and not read_only

        # Loads enabled checkbox state
        pa.set_value('enabled', enabled)
        pa.set_enabled('enabled', not done and not read_only)

        # Loads name entry
        name = self.get_value('name')
        pa.set_value('name', name)
        pa.set_enabled('name', sensitive)

        # Loads type combobox selected option
        repotype = self.get_value('type')
        pa.set_value('type', repotype)
        pa.set_enabled('type', sensitive)

        site.register_attribute_observer(self)


class DetailDNSHostControlAgent(DetailBaseControlAgent):
    """
    DNSHost sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        site.register_attribute_observer(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailDNSHostPresentationAgent(self)
        pa.register_widget_observer(self)
        # Loads comboboxes items
        pa.set_items('domain', SiteDefaultsManager.get_domains())
        pa.set_items('platform', SiteDefaultsManager.get_platforms())
        self.set_presentation_agent(pa)
        # Initializes widget values
        self.load_widgets_data()

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unregisters presetations view from site
        self.get_site().remove_attribute_observer(
            self.get_presentation_agent())
        BaseControlAgent.destroy(self)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        site = self.get_site()
        site.remove_attribute_observer(self)

        done = self.get_value('done')
        read_only = self.get_read_only_flag()
        sensitive = not done and not read_only

        # Loads name entry
        name = self.get_value('name')
        pa.set_value('name', name)
        pa.set_enabled('name', sensitive)

        # Loads description entry
        description = self.get_value('description')
        pa.set_value('description', description)
        pa.set_enabled('description', sensitive)

        # Loads domain combobox selected option
        domain = self.get_value('domain')
        pa.set_value('domain', domain)
        pa.set_enabled('domain', sensitive)

        # Loads platform combobox selected option
        platform = self.get_value('platform')
        pa.set_value('platform', platform)
        pa.set_enabled('platform', sensitive)

        site.register_attribute_observer(self)


if __name__ == '__main__':
    config = SiteConfigurationManager.get_blank_site()
    control = DetailMainControlAgent(config, False)
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
