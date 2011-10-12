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
            'mysql': 'MySQL',
            'pgsql': 'PostgresQL'
            }

    @staticmethod
    def get_default_database_type():
        """
        Returns the default databases technology.

        Note that only the mnemonique is returned, not the associated label
        """
        return 'mysql'

    @staticmethod
    def get_repository_types():
        """
        Returns the hash of available RCS repositories technologies supported

        The hash key is the type mnemonique, and the value is the label to be
        diaplayed.
        """
        return {
            'svn': 'SVN',
            'git': 'GIT',
            'cvs': 'CVS'
            }

    @staticmethod
    def get_default_repository_type():
        """
        Returns the hash of available RCS repositories technologies supported

        Note that only the mnemonique is returned, not the associated label
        """
        return 'svn'

    @staticmethod
    def get_platforms():
        """
        Returns a sorted list of available site platfoms.

        The sorted list is mainly used to order components in applicaiton views
        """
        return { 'prod': 'Prod', 'test': 'Test', 'dev': 'Dev' }

    @staticmethod
    def get_default_platform():
        """
        Returns the default platform name.

        Note that only the mnemonique is returned, not the associated label
        """
        return 'prod'

    @staticmethod
    def get_site_templates():
        """
        Returns the hash of available site templates supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'standard': 'Standard',
            'symfony': 'Symfony',
            'zend': 'Zend'
            }

    @staticmethod
    def get_default_site_template():
        """
        Returns the default site template

        Note that only the mnemonique is returned, not the associated label
        """
        return 'standard'

    @staticmethod
    def get_site_accesses():
        """
        Returns the hash of available web sutes access types supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'internal': 'Internal only',
            'external': 'Internal / External',
            'custom': 'Custom'
            }

    @staticmethod
    def get_default_site_access():
        """
        Returns the default site access type

        Note that only the mnemonique is returned, not the associated label
        """
        return 'internal'

    @staticmethod
    def get_domains():
        """
        Returns the hash of available site domains supported

        The hash key is the domain mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'bpinet.com': 'bpinet.com',
            'groupe-bpi.com': 'groupe-bpi.com',
            'bpi-group.com': 'bpi-group.com'
            }

    @staticmethod
    def get_default_domain():
        """
        Returns the available domain name

        Note that only the mnemonique is returned, not the associated label
        """
        return 'bpinet.com'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
