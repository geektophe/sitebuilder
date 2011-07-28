#!/usr/bin/env python
"""
Test classes for utils.observer module
"""

import unittest
import doctest
from sitebuilder.observer import addaction
from sitebuilder.observer import cancelaction
from sitebuilder.observer import datachanged
from sitebuilder.observer import deleteaction
from sitebuilder.observer import editaction
from sitebuilder.observer import submitaction
from sitebuilder.observer import validitychanged
from sitebuilder.observer import viewaction

class Test(unittest.TestCase):
    """Unist tests for observer modules"""

    def test_addaction_doctests(self):
        """Run doctests"""
        doctest.testmod(addaction)

    def test_cancelaction_doctests(self):
        """Run doctests"""
        doctest.testmod(cancelaction)

    def test_datachanged_doctests(self):
        """Run doctests"""
        doctest.testmod(datachanged)

    def test_deleteaction_doctests(self):
        """Run doctests"""
        doctest.testmod(deleteaction)

    def test_editaction_doctests(self):
        """Run doctests"""
        doctest.testmod(editaction)

    def test_submitaction_doctests(self):
        """Run doctests"""
        doctest.testmod(submitaction)

    def test_validitychanged_doctests(self):
        """Run doctests"""
        doctest.testmod(validitychanged)

    def test_viewaction_doctests(self):
        """Run doctests"""
        doctest.testmod(viewaction)

if __name__ == "__main__":
    unittest.main()
