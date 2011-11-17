#!/usr/bin/env python
"""
Site components related interfaces definition
"""

from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from zope.interface import Interface
from zope.schema import Object, Choice, TextLine, Bool
import re


class IDNSHost(Interface):
    """
    Interface describing site general settings
    """
    name = TextLine(
        title=u"Name",
        required=True,
        description=u"Host name",
        constraint=re.compile(r'^[\w\d_-]+$').match)
        #default=u'')

    domain = Choice(
        SiteDefaultsManager.get_domains().keys(),
        title=u"Type",
        required=True,
        description=u"Repository type",
        default=SiteDefaultsManager.get_default_domain())

    platform = Choice(
        SiteDefaultsManager.get_platforms().keys(),
        required=True,
        title=u"Platform",
        description=u"Site platform",
        default=SiteDefaultsManager.get_default_platform())

    description = TextLine(
        title=u"Description",
        description=u"Site description")
        #default=u'')

    done = Bool(
        title=u"Done",
        required=True,
        description=u"DNS host creation done",
        default=False)


class IRCSRepository(Interface):
    """
    Interface describing RCS repository related settings
    """
    enabled = Bool(
        title=u"Enabled",
        required=True,
        description=u"Repository enabled",
        default=False)

    name = TextLine(
        title=u"Name",
        required=True,
        description=u"Repository name",
        constraint=re.compile(r'^[\w\d_-]+$').match)
        #default=u'')

    type = Choice(
        SiteDefaultsManager.get_repository_types().keys(),
        title=u"Type",
        required=True,
        description=u"Repository type",
        default=SiteDefaultsManager.get_default_repository_type())

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Repository creation done",
        default=False)


class IWebsite(Interface):
    """
    Interface describing website related settings
    """
    enabled = Bool(
        title=u"Enabled",
        required=True,
        description=u"Website enabled",
        default=False)

    template = Choice(
        SiteDefaultsManager.get_site_templates().keys(),
        title=u"Template",
        required=True,
        description=u"Website template",
        default=SiteDefaultsManager.get_default_site_template())

    access = Choice(
        SiteDefaultsManager.get_site_accesses().keys(),
        title=u"Access",
        required=True,
        description=u"Site access level",
        default=SiteDefaultsManager.get_default_site_access())

    maintenance = Bool(
        title=u"Maintenance",
        required=True,
        description=u"Website under maintenance",
        default=False)

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Website creation done",
        default=False)


class IDatabase(Interface):
    """
    Interface describing database related settings
    """
    enabled = Bool(
        title=u"Enabled",
        required=True,
        description=u"Database enabled",
        default=False)

    type = Choice(
        SiteDefaultsManager.get_database_types().keys(),
        title=u"Type",
        required=True,
        description=u"Database type",
        default=SiteDefaultsManager.get_default_database_type())

    name = TextLine(
        title=u"Name",
        required=True,
        description=u"Database name",
        constraint=re.compile(r'^[\w\d_]+$').match)
        #default=u'')

    username = TextLine(
        title=u"Username",
        required=True,
        description=u"Database username (owner)",
        constraint=re.compile(r'^[\w\d_]+$').match)
        #default=u'')

    password = TextLine(
        title=u"Password",
        required=True,
        description=u"Database owner password")
        #default=u'')

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Database creation done",
        default=False)


class ISite(Interface):
    """
    Interface describing a site object
    """
    dnshost = Object(
        required=True,
        schema=IDNSHost,
        title=u"DNS",
        description=u"DNS definition object")

    repository = Object(
        required=True,
        schema=IRCSRepository,
        title=u"Repository",
        description=u"RCS repository definition object")

    website = Object(
        required=True,
        schema=IWebsite,
        title=u"Website",
        description=u"Website definition object")

    database = Object(
        required=True,
        schema=IDatabase,
        description=u"Database definition object")
