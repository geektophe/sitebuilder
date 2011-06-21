#!/usr/bin/env python
"""
Test classes for abstraction.configuration moodule
"""

import unittest
import doctest
from sitebuilder.model import configuration

class Test(unittest.TestCase):
    """Unist tests for configuration."""

    def test_doctests(self):
        """Run configuration doctests"""
        doctest.testmod(configuration)

if __name__ == "__main__":
    unittest.main()
