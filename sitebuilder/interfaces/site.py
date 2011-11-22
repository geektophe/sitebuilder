#!/usr/bin/env python
"""
Site components related interfaces definition
"""

from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from zope.interface import Interface
from zope.schema import Object, Choice, TextLine, Bool, Int
import re

# Site related constants
SITE_NEW    = 0
SITE_EXISTS = 1

class IDNSHost(Interface):
    """
    Interface describing site general settings
    """
    name = TextLine(
        title=u"Host name",
        required=True,
        description=u"Should be an alphanumeric string (^[\w\d_-]+$)",
        constraint=re.compile(r'^[\w\d_-]*$').match,
        default=u'')

    domain = Choice(
        SiteDefaultsManager.get_domains().keys(),
        title=u"Domain name",
        required=True,
        description=u"Should be one of allowed domains",
        default=SiteDefaultsManager.get_default_domain())

    platform = Choice(
        SiteDefaultsManager.get_platforms().keys(),
        required=True,
        title=u"Platform",
        description=u"Should be one of allowed platforms",
        default=SiteDefaultsManager.get_default_platform())

    description = TextLine(
        title=u"Description",
        required=True,
        description=u"Site description",
        default=u'')

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Should be a boolean value",
        default=False)


class IRCSRepository(Interface):
    """
    Interface describing RCS repository related settings
    """
    enabled = Bool(
        title=u"Repository enabled",
        required=True,
        description=u"Should be a boolean value",
        default=False)

    name = TextLine(
        title=u"Repository name",
        required=True,
        description=u"Should be an alphanumeric string (^[\w\d_-]+$)",
        constraint=re.compile(r'^[\w\d_-]*$').match,
        default=u'')

    type = Choice(
        SiteDefaultsManager.get_repository_types().keys(),
        title=u"Repository type",
        required=True,
        description=u"Should be one of allowed types",
        default=SiteDefaultsManager.get_default_repository_type())

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Should be a boolean value",
        default=False)


class IWebsite(Interface):
    """
    Interface describing website related settings
    """
    enabled = Bool(
        title=u"Website enabled",
        required=True,
        description=u"Should be a boolean value",
        default=False)

    template = Choice(
        SiteDefaultsManager.get_site_templates().keys(),
        title=u"Website template",
        required=True,
        description=u"Should be one of allowed site templates",
        default=SiteDefaultsManager.get_default_site_template())

    access = Choice(
        SiteDefaultsManager.get_site_accesses().keys(),
        title=u"Website access",
        required=True,
        description=u"Should be one of allowed site accesses",
        default=SiteDefaultsManager.get_default_site_access())

    maintenance = Bool(
        title=u"Maintenance",
        required=True,
        description=u"Should be a boolean value",
        default=False)

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Should be a boolean value",
        default=False)


class IDatabase(Interface):
    """
    Interface describing database related settings
    """
    enabled = Bool(
        title=u"Database enabled",
        required=True,
        description=u"Should be a boolean value",
        default=False)

    type = Choice(
        SiteDefaultsManager.get_database_types().keys(),
        title=u"Type",
        required=True,
        description=u"Should be one of allowed database types",
        default=SiteDefaultsManager.get_default_database_type())

    name = TextLine(
        title=u"Database name",
        required=True,
        description=u"Should be an alphanumeric string (^[\w\d_]+$)",
        constraint=re.compile(r'^[\w\d_]*$').match,
        default=u'')

    username = TextLine(
        title=u"Database owner",
        required=True,
        description=u"Should be an alphanumeric string (^[\w\d_]+$)",
        constraint=re.compile(r'^[\w\d_]*$').match,
        default=u'')

    password = TextLine(
        title=u"Owner password",
        required=True,
        description=u"Database owner password",
        default=u'')

    done = Bool(
        title=u"Done",
        required=True,
        description=u"Should be a boolean value",
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
        title=u"Datababse",
        description=u"Database definition object")

    status = Int(
        title=u"Status",
        required=True,
        description=u"Should be an integer value",
        default=SITE_NEW)
