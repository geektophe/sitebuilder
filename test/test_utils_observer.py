#!/usr/bin/env python
"""
Test classes for utils.observer moodule
"""

import unittest
import doctest
from sitebuilder.utils import observer

class Test(unittest.TestCase):
    """Unist tests for attributes"""

    def test_doctests(self):
        """Run configuration doctests"""
        doctest.testmod(observer)

if __name__ == "__main__":
    unittest.main()

