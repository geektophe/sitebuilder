#!/us/bin/env python
"""
This module contains Attribute utility classes, used to build value controlled
data trees (like dictionnaries).

It contains the basic Atribute class that represents an attribute, identified
by its name, with its attached value, and the necessary routines to control it.

It also contains the AttributeSet class that represents a collection of
attributes. It has the necessary methods to manipulate attributes.
"""

from sitebuilder.observer.attribute import AttributeSubject
from sitebuilder.observer.attribute import IAttributeSubject, IAttributeObserver
from zope.interface import Interface, implements
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty


class TriggerFieldProperty(FieldProperty):

    """
    Descriptor class vased on Zope's FieldProperty that triggers
    AttrubteChngedEvent event on value set.

    It should be used to define an object attribute descriptor. The owner class
    should have a 'notify_attribute_changed' method. The simplest is to
    subclass AttributeSubject.

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(AttributeSubject):
    ...     attr = TriggerFieldProperty(ITestSubject['attr'])
    ...
    >>> obj = TestSubject()
    >>> obj.attr
    u'initvalue'

    >>> obj.attr = u'val'
    >>> obj.attr
    u'val'

    When the subject attribute value is set, an AttributeEvent should
    be sent to observers.

    >>> class TestObserver(object):
    ...     implements(IAttributeObserver)
    ...     notified = False
    ...     def attribute_changed(self, event=None):
    ...         self.notified = True
    ...
    >>> observer = TestObserver()
    >>> obj.register_attribute_observer(observer)
    >>> obj.attr = u'val2'
    >>> observer.notified
    True
    """

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        FieldProperty.__set__(self, instance, value)

        if IAttributeSubject.providedBy(instance):
            instance.notify_attribute_changed(instance)


class UnicodeTriggerFieldProperty(TriggerFieldProperty):
    """
    This class works exactly as TriggerFieldProperty, but str values are
    transcoded to unicode.

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(AttributeSubject):
    ...     attr = UnicodeTriggerFieldProperty(ITestSubject['attr'])
    ...
    >>> obj = TestSubject()
    >>> obj.attr
    u'initvalue'

    >>> obj.attr = 'val'
    >>> obj.attr
    u'val'
    """

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        if isinstance(value, str):
            value = unicode(value)

        TriggerFieldProperty.__set__(self, instance, value)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
