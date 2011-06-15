#!/usr/bin/env python
"""
Test classes for utils.attribute moodule
"""

import unittest
import doctest
from sitebuilder.utils import attribute

class Test(unittest.TestCase):
    """Unist tests for attributes"""

    def test_doctests(self):
        """Run configuration doctests"""
        doctest.testmod(attribute)

if __name__ == "__main__":
    unittest.main()

