#!/usr/bin/env python
"""
Test classes for utils.observer module
"""

import unittest
import doctest
from sitebuilder.observer import validitychanged, attribute

class Test(unittest.TestCase):
    """Unist tests for observer modules"""

    def test_doctests(self):
        """Run doctests"""
        for module in ( validitychanged, attribute):
            doctest.testmod(module)

if __name__ == "__main__":
    unittest.main()
