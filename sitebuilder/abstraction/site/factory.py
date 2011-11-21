#!/usr/bin/env python
"""
Object factories
"""

from sitebuilder.abstraction.site.object import Site, DNSHost
from zope.component.factory import Factory


# Zope factory for Site objects
site_factory = Factory(Site, 'Site')

# Zope factory for DNSHost objects
dnshost_factory = Factory(DNSHost, 'DNSHost')
