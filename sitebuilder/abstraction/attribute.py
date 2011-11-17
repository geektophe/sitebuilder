#!/us/bin/env python
"""
This module contains Attribute utility classes, used to build value controlled
data trees (like dictionnaries).

It contains the basic Atribute class that represents an attribute, identified
by its name, with its attached value, and the necessary routines to control it.

It also contains the AttributeSet class that represents a collection of
attributes. It has the necessary methods to manipulate attributes.
"""

import re
from sitebuilder.observer.attribute import AttributeChangedObserver
from sitebuilder.observer.attribute import AttributeChangedSubject
from sitebuilder.observer.attribute import AttributeChangedEvent
from zope.interface import implements, Interface
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty

class Attribute(AttributeChangedSubject):
    """
    A configuration attribute item that is part of a configuration tree.

    Each configuration attribute is identified by its name, and can be get or
    set its value.

    It also presents a validate method that checks that the current value is
    valid. The value validity checking is performed by default by checking if
    is matches a regular expression that may be changed. Subclasses may
    implement their own validity checking method. The load method has to be
    overloeded also to take in consideration this change.

    As the attribute is part of a tree, it is possible to check whether the
    it has childs using has_children, and childre can be fetched using
    get_children method.

    A load method is also available to build a configuration tree composed of
    attribute objects from an input dictionnary. The corresponding dump method
    is also available to dump the current configuartion as a dictionnary.
    """

    def __init__(self, name, value=None, validator=None, errmsg=None):
        """
        Object initialization. The only mandatory argument is the attribute
        name, that cannot be changed later.
        """
        AttributeChangedSubject.__init__(self)
        self._name = name
        self._value = value
        self._validator = validator
        self._errmsg = errmsg
        self._changed = False
        self._re = None

    def get_name(self):
        """
        Returns attribute name

        >>> attr = Attribute(name='somename')
        >>> attr.get_name()
        'somename'
        """
        return self._name

    def validate(self, value):
        """
        Checks whether an input value is valid

        If a regex is passed at instanciation, it should be used to validate
        against data validity

        >>> attr = Attribute(name='somename', validator=r'^[\d]+$')
        >>> attr.validate(5)
        True
        >>> attr.validate('somestring')
        False

        If none is defined, a value should always ve valid

        >>> attr = Attribute(name='somename')
        >>> attr.validate(5)
        True
        >>> attr.validate('somestring')
        True

        Validator may also be a type. In such a case, the value validates if
        it is a direct or indirect instance of this type

        >>> attr = Attribute(name='somename', validator=bool)
        >>> attr.validate(True)
        True
        >>> attr.validate('string')
        False

        It can also be a list. In such a case, value is valid if is matches one
        of the values

        >>> attr = Attribute(name='somename', validator=(1, 2, 3))
        >>> attr.validate(1)
        True
        >>> attr.validate(4)
        False
        
        It can also be a fucntion, such as a lambda function

        >>> attr = Attribute(name='somename', validator=lambda x: x == 1)
        >>> attr.validate(1)
        True
        >>> attr.validate(2)
        False
        """
        validator = self._validator

        if validator is None:
            return True

        elif isinstance(validator, str) and len(validator) and \
                    validator[0] == '^' and validator[-1] == '$':
            if self._re is None:
                self._re = re.compile(validator)
            return (self._re.match(str(value)) is not None)

        elif isinstance(validator, (tuple, list)):
            return value in self._validator

        elif isinstance(validator, type):
            return isinstance(value, validator)

        elif callable(validator):
            return validator(value)

        else:
            raise AttributeError("Unsupported validator type")

    def get_value(self):
        """
        Returns current value

        >>> attr = Attribute(name='somename', value='somevalue')
        >>> attr.get_value()
        'somevalue'
        """
        return self._value

    def set_value(self, value, check=True):
        """
        Sets current value.

        >>> attr = Attribute(name='somename')
        >>> attr.set_value('somevalue')
        >>> attr.get_value()
        'somevalue'

        If a validatoin regex is passed at instanciation, it should be used to
        check against data validity.

        >>> attr = Attribute(name='somename', validator=r'^[\d]+$')
        >>> attr.set_value(5)
        >>> attr.get_value()
        5

        If an invalid data is passed, an AttributeError should be raised.

        >>> attr = Attribute(name='somename', validator=r'^[\d]+$')
        >>> attr.set_value('somevalue')
        Traceback (most recent call last):
            ...
        AttributeError: Value did not match '^[\\d]+$'

        An custom error message can be set at construction

        >>> attr = Attribute(name='somename', validator=r'^[\d]+$', errmsg='Error')
        >>> attr.set_value('somevalue')
        Traceback (most recent call last):
            ...
        AttributeError: Error

        Finally, if the user interface has previously checked data with the
        check method, in order to avoid double check, it is possible to disable
        data check. This way, any data should be set.

        >>> attr = Attribute(name='somename', validator=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.get_value()
        5
        >>> attr.set_value('somevalue', False)
        >>> attr.get_value()
        'somevalue'

        A value set should enable the changed flag
        >>> attr = Attribute(name='somename', validator=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.is_changed()
        True

        As an AttributeChangedSubject, when an attribute value is set, an event is
        sent containing the attribute itself as context.

        >>> class TestListener(AttributeChangedObserver):
        ...     def __init__(self):
        ...         self._event = None
        ...     def attribute_changed(self, event):
        ...         self._event = event
        ...     def get_event(self):
        ...         return self._event
        >>> observer = TestListener()
        >>> attr = Attribute(name='somename')
        >>> attr.register_attribute_changed_observer(observer)
        >>> attr.set_value(5)
        >>> context = observer.get_event().get_attribute()
        >>> attr is context
        True
        """
        if check is True and self.validate(value) is False:
            # TODO: be more descriptive
            if self._errmsg is not None:
                raise AttributeError(self._errmsg)
            else:
                raise AttributeError(r"Value did not match '%s'" % self._validator)
        self._value = value
        self._changed = True
        self.notify_attribute_changed(AttributeChangedEvent(self))

    def is_changed(self):
        """
        Returns the changed flag
        """
        return self._changed

    def clear_changed(self):
        """
        Resets the changed flag
        """
        self._changed = False

    def __str__(self):
        """
        Returns object string representation.
        """
        return '<Attribute object {name: %s, value: %s}>' % \
            (self._name, self._value)


class AttributeSet(AttributeChangedObserver, AttributeChangedSubject):
    """
    A class that represents a set of attributes.

    Each attrbiute can be fetched using its name (get_attribute), or through
    an iterator (for statement).

    A load method allows to load a set of predefined attributes from
    dictionary (see load method docstring for details)

    """

    def __init__(self, name=None, attributes=None):
        """
        AttribvuteSet initialization
        """
        AttributeChangedSubject.__init__(self)
        self._name = name
        self._attributes = {}
        self._changed = False

        if  attributes is not None:
            self.load(attributes)

    def get_name(self):
        """
        Returns attribute set name

        >>> aset = AttributeSet('aset')
        >>> aset.get_name()
        'aset'
        """
        return self._name

    def load(self, attrdict):
        """
        = Attribute set loading from dictionnary

        The load method allows to load a set of predefined attributes from
        dictionary using the following formalism:

        - Each key represents an attribute name.
        - If dictionary's associated value is a tupple, then a new Attribute
        object should be instanciated (see Attribute loading from tupple
        section below for details on Attribute formalism)
        - If the associated value is another dictionnary, then it should be
        loaded as sub AttributeSet.

        = Attrribute loading from tuppple

        When a tupple is detected in a dictionary value, it is loaded as an
        Attribute object. The tupple must stick the following formalism :

        (value, validator, verrdescr)

        Where 'name' is the attribute name, 'validator' is the attrbibute regex
        used to check attribute value vaidity while using set_attrbiute methid
        (should be None if you don't want to apply value cehcking), and 'value'
        is the initial attrbiute value (should be None if you don't knwo it).

        >>> attrdict = {}
        >>> attrdict['somename'] = ('somevalue', None, None)
        >>> attrdict['sub'] = {}
        >>> attrdict['sub']['someothername'] = ('someothervalue', '^[\w]+$',
        ...                                       'Value should be a string')
        >>> aset = AttributeSet('aset')
        >>> aset.load(attrdict)
        >>> attr = aset.get_attribute('somename')
        >>> isinstance(attr, Attribute)
        True
        >>> attr.get_name()
        'somename'
        >>> attr.get_value()
        'somevalue'
        >>> sub = aset.get_attribute('sub')
        >>> isinstance(sub, AttributeSet)
        True
        >>> subattr = sub.get_attribute('someothername')
        >>> subattr.get_name()
        'someothername'
        >>> subattr.get_value()
        'someothervalue'

        The load operation is atomic. If an attribute loading fails, the whole
        loading should be rollbacked.

        A loaded attribute set should have changed flag unset

        >>> aset.is_changed()
        False
        """
        new_attributes = {}

        for key, value in attrdict.iteritems():
            if isinstance(value, tuple):
                options = []

                for index in range(3):
                    if len(value) > index:
                        options.append(value[index])

                new_attributes[key] = Attribute(key, *options)
                new_attributes[key].register_attribute_changed_observer(self)
            elif isinstance(value, dict):
                new_attributes[key] = AttributeSet(key)
                new_attributes[key].register_attribute_changed_observer(self)
                new_attributes[key].load(value)
            else:
                raise AttributeError('Invalid data format for key %s' % key)

            self._attributes = new_attributes

    def dump(self):
        """
        Returns a dump of the internal data
        """
        # TODO: implement dump method
        raise NotImplementedError(
            'dump method is not implemented for the moment.')

    def get_attribute(self, name):
        """
        Returns attribute named 'name'

        >>> attrdict = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attrdict)
        >>> attr = aset.get_attribute('somename')
        >>> isinstance(attr, Attribute)
        True
        >>> attr.get_value()
        'somevalue'

        If attribute does not exist, it should raise ne exception.

        >>> aset = AttributeSet('aset')
        >>> attr = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'
        """
        if not self._attributes.has_key(name):
            raise AttributeError("No attribute named '%s'" % name)

        return self._attributes[name]

    def del_attribute(self, name):
        """
        Deletes attribute named 'name'

        >>> attrdict = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attrdict)
        >>> attr = aset.del_attribute('somename')
        >>> attr = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'

        If attribute does not exist, it should raise ne exception.

        >>> aset = AttributeSet('aset')
        >>> attr = aset.del_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'
        """
        if not self._attributes.has_key(name):
            raise AttributeError("No attribute named '%s'" % name)

        del self._attributes[name]

    def get_attribute_names(self):
        """
        Returns the list of contained attributes

        >>> attrdict = {}
        >>> attrdict['somename'] = ('somevalue', None, None)
        >>> attrdict['someothername'] = ('someothervalue', None, None)
        >>> aset = AttributeSet('aset', attrdict)
        >>> aset.get_attribute_names()
        ['somename', 'someothername']
        """
        return self._attributes.keys()

    def add_attribute(self, attribute):
        """
        Adds an Attribute or an AttributeSet.

        The key under which the attribute is stored is the same as the
        attribute name

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = AttributeSet('someothername')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> attr3 = aset.get_attribute('somename')
        >>> isinstance(attr3, Attribute)
        True
        >>> attr3.get_value()
        'somevalue'
        >>> attr3 = aset.get_attribute('someothername')
        >>> isinstance(attr3, AttributeSet)
        True

        Only Attribute and AttributteSet types are allowed.

        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute('string')
        Traceback (most recent call last):
            ...
        AttributeError: Invalid attribute type. Only Attribute and AttributeSet allowed.

        Adding attributes whiche name are the same is forbidden.

        >>> aset = AttributeSet('aset')
        >>> attr1 = Attribute('somename')
        >>> attr2 = Attribute('somename')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        Traceback (most recent call last):
            ...
        AttributeError: Attribute name 'somename' already exists.

        As an AttributeChangedSubject, when an attribute is added, an event is
        sent containing the attribute set itself as context.

        >>> class TestListener(AttributeChangedObserver):
        ...     def __init__(self):
        ...         self._event = None
        ...     def attribute_changed(self, event):
        ...         self._event = event
        ...     def get_event(self):
        ...         return self._event
        >>> observer = TestListener()
        >>> aset = AttributeSet('aset')
        >>> aset.register_attribute_changed_observer(observer)
        >>> attr = Attribute(name='somename')
        >>> aset.add_attribute(attr)
        >>> context = observer.get_event().get_attribute()
        >>> aset is context
        True
        """
        if not isinstance(attribute, Attribute) and \
                not isinstance(attribute, AttributeSet):

            raise AttributeError(
                'Invalid attribute type. ' +
                'Only Attribute and AttributeSet allowed.')

        if self._attributes.has_key(attribute.get_name()):
            raise AttributeError("Attribute name '%s' already exists." %
                                attribute.get_name())

        self._attributes[attribute.get_name()] = attribute
        attribute.register_attribute_changed_observer(self)
        self.notify_attribute_changed(AttributeChangedEvent(self))

    def remove_attribute(self, name):
        """
        Removes an Attribute or an AttributeSet.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset['somename'] = attr
        >>> attr2 = aset.get_attribute('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> aset.remove_attribute('somename')
        >>> attr2 = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'

        As an AttributeChangedSubject, when an attribute is removed, an event
        is sent containing the attribute set itself as context.

        >>> class TestListener(AttributeChangedObserver):
        ...     def __init__(self):
        ...         self._event = None
        ...     def attribute_changed(self, event):
        ...         self._event = event
        ...     def get_event(self):
        ...         return self._event
        >>> observer = TestListener()
        >>> aset = AttributeSet('aset')
        >>> aset.register_attribute_changed_observer(observer)
        >>> attr = Attribute(name='somename')
        >>> aset.add_attribute(attr)
        >>> context = observer.get_event().get_attribute()
        >>> aset is context
        True
        """
        attribute = self.get_attribute(name)

        if isinstance(attribute, AttributeSet):
            for attrname in attribute.get_attribute_names():
                attribute.remove_attribute(attrname)

        attribute.remove_attribute_changed_observer(self)
        del self._attributes[name]
        self.notify_attribute_changed(AttributeChangedEvent(self))

    def attribute_changed(self, event=None):
        """
        Listener trigger method implementation
        """
        self._changed = True
        self.notify_attribute_changed(event)

    def is_changed(self):
        """
        Returns the changed flag

        When an attribute is changed, the whole up tree should be in changed
        state:

        >>> attrdict = {}
        >>> attrdict['somename'] = ('somevalue', None, None)
        >>> attrdict['sub'] = {}
        >>> attrdict['sub']['someothername'] = ('someothervalue', '^[\w]+$',
        ...                                       'Value should be a string')
        >>> aset = AttributeSet('aset')
        >>> aset.load(attrdict)
        >>> aset.is_changed()
        False
        >>> attr = aset['sub']['someothername']
        >>> attr.set_value('abc')
        >>> aset.is_changed()
        True
        """
        return self._changed

    def clear_changed(self, recurse=False):
        """
        Resets the changed flag

        >>> attrdict = {}
        >>> attrdict['somename'] = ('somevalue', None, None)
        >>> attrdict['sub'] = {}
        >>> attrdict['sub']['someothername'] = ('someothervalue', '^[\w]+$',
        ...                                       'Value should be a string')
        >>> aset = AttributeSet('aset')
        >>> aset.load(attrdict)
        >>> attr = aset['sub']['someothername']
        >>> attr.set_value('abc')
        >>> aset.is_changed()
        True
        >>> aset.clear_changed()
        >>> aset.is_changed()
        False

        If is_changed is not called with recurse flag, only the current
        attribute is cleared its changed state

        >>> attr.is_changed()
        True

        If is_changed is called with recurse flag, all the subtree is cleared
        its changed state

        >>> aset.clear_changed(recurse=True)
        >>> attr.is_changed()
        False
        """
        self._changed = False

        if recurse is True:

            for attribute in self._attributes.values():
                if isinstance(attribute, Attribute):
                    attribute.clear_changed()
                elif isinstance(attribute, AttributeSet):
                    attribute.clear_changed(recurse=True)

    def iteritems(self):
        """
        Returns an iterator on attributes

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ (key, value.get_value()) for key, value in aset.iteritems() ]
        [('somename', 'somevalue'), ('someothername', 'someothervalue')]
        """
        return self._attributes.iteritems()

    def items(self):
        """
        Returns attributes keys and values

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ (key, value.get_value()) for key, value in aset.items() ]
        [('somename', 'somevalue'), ('someothername', 'someothervalue')]
        """
        return self._attributes.iteritems()

    def keys(self):
        """
        Returns attributes keys

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> aset.keys()
        ['somename', 'someothername']
        """
        return self._attributes.keys()

    def values(self):
        """
        Returns attributes keys

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ value.get_value() for  value in aset.values() ]
        ['somevalue', 'someothervalue']
        """
        return self._attributes.values()

    def has_key(self, key):
        """
        Checks whether an attribute is registered as key

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> aset.has_key('somename')
        True
        >>> aset.has_key('someothername')
        False
        """
        return self._attributes.has_key(key)

    def clear(self):
        """
        Clears internal dictionnary

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> aset.has_key('somename')
        True
        >>> aset.clear()
        >>> aset.has_key('somename')
        False
        """
        return self._attributes.clear()

    def get(self, key, default=None):
        """
        Gets value from dictionnary. If key does not exist, returnd default.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset.get('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr.get_value()
        'somevalue'
        >>> attr3 = aset.get('someothername')
        >>> attr3 is None
        True
        """
        return self._attributes.get(key, default)

    def pop(self, key, default=None):
        """
        Pops an element from the internal dictionnary

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset.pop('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_value()
        'somevalue'
        >>> aset.has_key('somename')
        False
        >>> attr3 = aset.pop('somename')
        >>> attr3 is None
        True
        """
        return self._attributes.pop(key, default)

    def __getitem__(self, name):
        """
        Dictionnary like magic method

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset['somename']
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_name()
        'somename'
        >>> attr2.get_value()
        'somevalue'
        """
        return self.get_attribute(name)

    def __setitem__(self, name, attribute):
        """
        Dictionnary like magic method.

        Caution, the key used is the real object name, not the name parameter.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset['somename'] = attr
        >>> attr2 = aset.get_attribute('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_name()
        'somename'
        >>> attr2.get_value()
        'somevalue'
        """
        self.add_attribute(attribute)

    def __delitem__(self, name):
        """
        Dictionnary like magic method.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset['somename'] = attr
        >>> attr2 = aset.get_attribute('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> del aset['somename']
        >>> attr2 = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'
        """
        self.remove_attribute(name)

    def __str__(self):
        """
        Returns internal attributes string representation.
        """
        return str(self._attributes)


class StdTriggerAttribute(object):
    """
    Descriptor class that triggers AttrubteChngedEvent event on value set.

    It should be used to define an object attribute descriptor. The owner class
    should have a 'notify_attribute_changed' method. The simplest is to
    subclass AttributeChangedSubject.

    >>> class TestSubject(AttributeChangedSubject):
    ...     attr = StdTriggerAttribute('attr', 'initvalue')
    ...
    >>> obj = TestSubject()
    >>> obj.attr
    'initvalue'

    >>> obj.attr = 'val'
    >>> obj.attr
    'val'

    When the subject attribute value is set, an AttributeChangedEvent should
    be sent to observers.

    >>> class TestObserver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...
    >>> observer = TestObserver()
    >>> obj.register_attribute_changed_observer(observer)
    >>> obj.attr = 'val2'
    >>> observer.flag
    True
    """

    def __init__(self, name, value=None):
        """
        Descriptor initialization

        """
        self._name = name
        self._value = value

    def __get__(self, instance, klass):
        """
        Attribute value is set
        """
        return self._value

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        self._value = value
        instance.notify_attribute_changed(AttributeChangedEvent())


class UnicodeTriggerAttribute(StdTriggerAttribute):
    """
    This class works exactly as StdTriggerAttribute, but str values are
    transcoded to unicode.

    >>> class TestSubject(AttributeChangedSubject):
    ...     attr = UnicodeTriggerAttribute('attr', 'initvalue')
    ...
    >>> obj = TestSubject()
    >>> obj.attr
    u'initvalue'

    >>> obj.attr = 'val'
    >>> obj.attr
    u'val'

    Other values are left as they are

    >>> obj.attr = True
    >>> obj.attr
    True
    >>> obj.attr = u'val'
    >>> obj.attr
    u'val'
    """

    def __init__(self, name, value=None):
        """
        Descriptor initialization
        """
        if isinstance(value, str):
            value = unicode(value)

        StdTriggerAttribute.__init__(self, name, value)

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        if isinstance(value, str):
            value = unicode(value)

        StdTriggerAttribute.__set__(self, instance, value)


class TriggerFieldProperty(FieldProperty):

    """
    Descriptor class vased on Zope's FieldProperty that triggers
    AttrubteChngedEvent event on value set.

    It should be used to define an object attribute descriptor. The owner class
    should have a 'notify_attribute_changed' method. The simplest is to
    subclass AttributeChangedSubject.

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(AttributeChangedSubject):
    ...     attr = TriggerFieldProperty(ITestSubject['attr'])
    ...
    >>> obj = TestSubject()
    >>> obj.attr
    u'initvalue'

    >>> obj.attr = u'val'
    >>> obj.attr
    u'val'

    When the subject attribute value is set, an AttributeChangedEvent should
    be sent to observers.

    >>> class TestObserver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...
    >>> observer = TestObserver()
    >>> obj.register_attribute_changed_observer(observer)
    >>> obj.attr = u'val2'
    >>> observer.flag
    True
    """

    def __set__(self, instance, value):
        """
        Attribute value is set
        """
        FieldProperty.__set__(self, instance, value)
        instance.notify_attribute_changed(AttributeChangedEvent())


class UnicodeTriggerFieldProperty(TriggerFieldProperty):
    """
    This class works exactly as TriggerFieldProperty, but str values are
    transcoded to unicode.

    >>> class ITestSubject(Interface):
    ...     attr = TextLine(title=u'attr', default=u'initvalue')
    ...
    >>> class TestSubject(AttributeChangedSubject):
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
