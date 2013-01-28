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
from sitebuilder.control.base import BaseControlAgent
from sitebuilder.exception import FieldFormatError
from sitebuilder.event.events import UIActionEvent, UIWidgetEvent
from sitebuilder.event.events import DataValidityEvent, DataChangeEvent
from zope.schema import ValidationError
from sitebuilder.utils.parameters import ACTION_SUBMIT, ACTION_CANCEL
from zope.interface import implements
import gtk


class DetailMainControlAgent(BaseControlAgent):
    """
    Site details main interface's control agent
    """

    def __init__(self, site, read_only):
        """
        ControlAgent initialization
        """
        BaseControlAgent.__init__(self)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        presentation_agent = DetailMainPresentationAgent(self)
        presentation_agent.get_event_bus().subscribe(
            UIActionEvent, self.action_evt_callback)
        # Main detail presentation agent has no reason to listen to changed
        # attribute events. Disabled.
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

        self._validity_matrix = {}

    def action_evt_callback(self, event):
        """
        ActionPerformedObserver trigger mmethod local implementation
        """
        # Reads action name
        # Parses action
        if event.action == ACTION_SUBMIT:
            # Informs upper component from the submit action
            # Adds site as parameter to event
            self.submit()
        elif event.action == ACTION_CANCEL:
            # No need to inform upper component
            self.cancel()
        else:
            raise NotImplementedError("Unhandled action %d triggered" % action)

    def data_validity_evt_callback(self, event):
        """
        Observer method run on validity changed event
        """
        self._validity_matrix[id(event.source)] = flag

        res = True
        for value in self._validity_matrix.values():
            if value is False:
                res = False
                break

        pa = self.get_presentation_agent()
        pa.set_enabled('submit', res)

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
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(
            UIActionEvent, self.action_evt_callback)

        # Destroyes slave components
        for slave in self._slaves:
            slave.destroy()

        BaseControlAgent.destroy(self)


class DetailBaseControlAgent(BaseControlAgent):
    """
    Base control agent class providing methods useful for
    DetailMainControlAgent childs.
    """

    def __init__(self):
        BaseControlAgent.__init__(self)

    def widget_evt_callback(self, event):
        """
        Observer method run on widget changed event

        Name is the name of the widget that triggerd the event, value is the
        value it was set to.
        """
        pa = self.get_presentation_agent()
        site = self.get_site()

        # Avoids change notification loop, as we're also listening to site
        # TODO: implement site event bus
        site.get_event_bus().unsubscribe(UIWidgetEvent, self.widget_evt_callback)

        try:
            setattr(site, event.name, event.value)
        except (ValidationError, FieldFormatError), e:
            pa.set_error(event.name, True, str(e))
            self.get_event_bus().publish(
                DataValidityEvent(self, attribute=event.name, state=False) )
        else:
            pa.set_error(event.name, False)
            self.load_widgets_data()
            self.get_event_bus().publish(
                DataValidityEvent(self, attribute=event.name, state=True) )

        # TODO: implement site event bus
        site.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        site = self.get_site()
        # TODO: implement site event bus
        site.get_event_bus().unsubscribe(
            DataChangeEvent, self.data_change_evt_callback)

        BaseControlAgent.destroy(self)


class DetailSiteControlAgent(DetailBaseControlAgent):
    """
    Site sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        # TODO: implement site event bus
        site.get_event_bus().subscribe(DataChangeEvent, self.load_widgets_data)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailSitePresentationAgent(self)
        self.set_presentation_agent(pa)
        # Loads comboboxes items
        pa.set_items('template', SiteDefaultsManager.get_site_templates())
        pa.set_items('access', SiteDefaultsManager.get_site_accesses())
        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)
        # Initializes widget values
        self.load_widgets_data()

    def load_widgets_data(self, event=None):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.load_widgets_data)

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

        pa.get_event_bus().subscribe(UIWidgetEvent, self.load_widgets_data)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.load_widgets_data)
        DetailBaseControlAgent.destroy(self)


class DetailDatabaseControlAgent(DetailBaseControlAgent):
    """
    Database sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        # TODO: implement site event bus
        site.get_event_bus().subscribe(DataChangeEvent, self.load_widgets_data)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailDatabasePresentationAgent(self)
        self.set_presentation_agent(pa)
        # Loads comboboxes items
        pa.set_items('type', SiteDefaultsManager.get_database_types())
        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)
        # Initializes widget values
        self.load_widgets_data()

    def load_widgets_data(self, event=None):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.widget_evt_callback)

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

        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.load_widgets_data)
        DetailBaseControlAgent.destroy(self)


class DetailRepositoryControlAgent(DetailBaseControlAgent):
    """
    Repository sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        # TODO: implement event bus in site objects
        site.get_event_bus().subscribe(DataChangeEvent, self.load_widgets_data)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailRepositoryPresentationAgent(self)
        self.set_presentation_agent(pa)
        # Loads comboboxes items
        pa.set_items('type', SiteDefaultsManager.get_repository_types())
        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)
        # Initializes widget values
        self.load_widgets_data()

    def load_widgets_data(self, event=None):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.widget_evt_callback)

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

        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.load_widgets_data)
        DetailBaseControlAgent.destroy(self)


class DetailDNSHostControlAgent(DetailBaseControlAgent):
    """
    DNSHost sub component control agent
    """

    def __init__(self, site, read_only=False):
        DetailBaseControlAgent.__init__(self)
        site.get_event_bus().subscribe(DataChangeEvent, self.load_widgets_data)
        self.set_site(site)
        self.set_read_only_flag(read_only)
        pa = DetailDNSHostPresentationAgent(self)
        self.set_presentation_agent(pa)
        # Loads comboboxes items
        pa.set_items('domain', SiteDefaultsManager.get_domains())
        pa.set_items('platform', SiteDefaultsManager.get_platforms())
        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)
        # Initializes widget values
        self.load_widgets_data()

    def load_widgets_data(self, event=None):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.widget_evt_callback)

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

        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        pa = self.get_presentation_agent()
        pa.get_event_bus().unsubscribe(UIWidgetEvent, self.load_widgets_data)
        DetailBaseControlAgent.destroy(self)


if __name__ == '__main__':
    config = SiteConfigurationManager.get_blank_site()
    control = DetailMainControlAgent(config, False)
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
