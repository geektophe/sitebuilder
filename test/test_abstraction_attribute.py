#!/usr/bin/env python
"""
Test classes for abstraction.attribute moodule
"""

import unittest
import doctest
from sitebuilder.abstraction import attribute
from sitebuilder.abstraction.attribute import AttributeSet
from sitebuilder.observer.attribute import AttributeModifiedObserver


class TestListener(AttributeModifiedObserver):
    """
    Test listener that sets its internal state flag to tru if it's notified
    """

    def __init__(self):
        """
        Listener initialization
        """
        self._flag = False

    def attribute_modified(self, event=None):
        """
        Sets flag to true when notified
        """
        self._flag = True

    def get_flag(self):
        """
        Returns internal state flag
        """
        return self._flag


class Test(unittest.TestCase):
    """Unist tests for attributes"""

    def test_doctests(self):
        """Run configuration doctests"""
        doctest.testmod(attribute)

    def test_notification_chain(self):
        """
        Creates a hierarchy of attributes, then adds DataChangedListener
        objects on leaf and root elements. When the lead element is changed,
        both listeners should have been notified.
        """
        # Defines test data to load
        test_data = { 'child1' : { 'child11' : ('11',) }}

        # Builds attributes tree
        root = AttributeSet('root')
        root.load(test_data)
        child11 = root.get_attribute('child1').get_attribute('child11')

        # Instanciates listeners and affetc them to the corresponding nodes
        root_listener = TestListener()
        child_listener = TestListener()

        root.register_attribute_modified_observer(root_listener)
        child11.register_attribute_modified_observer(child_listener)

        # Changes leaf attribute value
        child11.set_value('child11_changed')

        self.assertTrue(
            child_listener.get_flag(),
            "The child listener has not been notified")

        self.assertTrue(
            root_listener.get_flag(),
            "The root listener has not been notified")


if __name__ == "__main__":
    unittest.main()

