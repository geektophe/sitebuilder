#!/usr/bin/env python

"""
Configuration related classes
"""

class SiteDefaultsManager(object):
    """
    Handles site configuration default or allowed values (in select controls)
    """

    def __init__(self):
        """
        Since it should be used as a static class, instaciation is forbdden.
        """
        raise NotImplementedError("Oops. Instaciation not allowed")

    def __copy__(self):
        """
        Since it should be used as a static class, cloning is forbdden.
        """
        raise NotImplementedError("Oops. Copy not allowed")

    @staticmethod
    def get_database_types():
        """
        Returns the hash of available databases technologies supported

        The hash key is the type mnemonique, and the value is the label to be
        diaplayed.
        """
        return {
            u'mysql': u'MySQL',
            u'pgsql': u'PostgresQL'
            }

    @staticmethod
    def get_default_database_type():
        """
        Returns the default databases technology.

        Note that only the mnemonique is returned, not the associated label
        """
        return u'mysql'

    @staticmethod
    def get_repository_types():
        """
        Returns the hash of available RCS repositories technologies supported

        The hash key is the type mnemonique, and the value is the label to be
        diaplayed.
        """
        return {
            u'svn': u'SVN',
            u'git': u'GIT',
            u'cvs': u'CVS'
            }

    @staticmethod
    def get_default_repository_type():
        """
        Returns the hash of available RCS repositories technologies supported

        Note that only the mnemonique is returned, not the associated label
        """
        return u'svn'

    @staticmethod
    def get_platforms():
        """
        Returns a sorted list of available site platfoms.

        The sorted list is mainly used to order components in applicaiton views
        """
        return { u'prod': u'Prod', u'test': u'Test', u'dev': u'Dev' }

    @staticmethod
    def get_default_platform():
        """
        Returns the default platform name.

        Note that only the mnemonique is returned, not the associated label
        """
        return u'prod'

    @staticmethod
    def get_site_templates():
        """
        Returns the hash of available site templates supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            u'standard': u'Standard',
            u'symfony': u'Symfony',
            u'zend': u'Zend'
            }

    @staticmethod
    def get_default_site_template():
        """
        Returns the default site template

        Note that only the mnemonique is returned, not the associated label
        """
        return u'standard'

    @staticmethod
    def get_site_accesses():
        """
        Returns the hash of available web sutes access types supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            u'internal': u'Internal only',
            u'external': u'Internal / External',
            u'custom': u'Custom'
            }

    @staticmethod
    def get_default_site_access():
        """
        Returns the default site access type

        Note that only the mnemonique is returned, not the associated label
        """
        return u'internal'

    @staticmethod
    def get_domains():
        """
        Returns the hash of available site domains supported

        The hash key is the domain mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            u'bpinet.com': u'bpinet.com',
            u'groupe-bpi.com': u'groupe-bpi.com',
            u'bpi-group.com': u'bpi-group.com'
            }

    @staticmethod
    def get_default_domain():
        """
        Returns the available domain name

        Note that only the mnemonique is returned, not the associated label
        """
        return u'bpinet.com'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
