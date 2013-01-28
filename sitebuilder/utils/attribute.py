#!/us/bin/env python
"""
This module contains Attribute utility classes, used to build value controlled
data trees (like dictionnaries).

It contains the basic Atribute class that represents an attribute, identified
by its name, with its attached value, and the necessary routines to control it.

It also contains the AttributeSet class that represents a collection of
attributes. It has the necessary methods to manipulate attributes.
"""

from zope.schema.fieldproperty import FieldProperty
from sitebuilder.event.events import DataChangeEvent
from sitebuilder.event.interface import IEventBroker


class TriggerFieldProperty(FieldProperty):

    """
    Descriptor class vased on Zope's FieldProperty that triggers
    AttrubteChngedEvent event on value set.

    It should be used to define an object attribute descriptor. The owner class
    should have a 'notify_attribute_changed' method. The simplest is to
    subclass AttributeSubject.

    >>> from zope.interface import implements
    >>> from sitebuilder.event.bus import EventBus
    >>> from zope.interface import Interface
    >>> from zope.schema import TextLine

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(object):
    ...     implements(IEventBroker)
    ...     attr = TriggerFieldProperty(ITestSubject['attr'])
    ...	    def __init__(self):
    ...         self._event_bus = EventBus()
    ...     def get_event_bus(self):
    ...         return self._event_bus

    >>> obj = TestSubject()
    >>> obj.attr
    u'initvalue'

    >>> obj.attr = u'val'
    >>> obj.attr
    u'val'

    When the subject attribute value is set, an AttributeEvent should
    be sent to observers.

    >>> class TestObserver(object):
    ...     notified = False
    ...     def attribute_changed(self, event):
    ...         self.notified = True
    ...
    >>> observer = TestObserver()
    >>> obj.get_event_bus().subscribe(DataChangeEvent, observer.attribute_changed)
    >>> obj.attr = u'val2'
    >>> observer.notified
    True
    """
    def __init__(self, field, name=None):
        """
        Fied initialization
        """
        FieldProperty.__init__(self, field, name)
        self.name = field.__name__

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        FieldProperty.__set__(self, instance, value)

        if IEventBroker.providedBy(instance):
            instance.get_event_bus().publish(
                DataChangeEvent(instance, attribute=self.name, value=value))


class UnicodeTriggerFieldProperty(TriggerFieldProperty):
    """
    This class works exactly as TriggerFieldProperty, but str values are
    transcoded to unicode.

    >>> from sitebuilder.event.bus import EventBus
    >>> from zope.interface import Interface
    >>> from zope.schema import TextLine

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(object):
    ...     attr = UnicodeTriggerFieldProperty(ITestSubject['attr'])
    ...	    def __init__(self):
    ...         self._event_bus = EventBus()
    ...     def get_event_bus(self):
    ...         return self._event_bus
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
