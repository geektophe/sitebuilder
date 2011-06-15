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

class Attribute(object):
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

    def __init__(self, name, value=None, vregex=None):
        """
        Object initialization. The only mandatory argument is the attribute
        name, that cannot be changed later.
        """
        self._name = name
        self._value = value
        self._vregex = vregex
        self._modified = False

        if vregex is not None:
            self._validator = re.compile(vregex)
        else:
            self._validator = None

    def get_name(self):
        """
        Returns attribute name

        >>> attr = Attribute(name='somename')
        >>> attr.get_name()
        'somename'
        """
        return self._name

    def get_vregex(self):
        """
        Returns attribute validation regex

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.get_vregex()
        '^[\\\\d]+$'
        """
        return self._vregex

    def check(self, value):
        """
        Checks whether an input value is valid

        If a regex is passed at instanciation, it should be used to check
        against data valididty

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.check(5)
        True
        >>> attr.check('somestring')
        False

        If none is defined, a value should always ve valid

        >>> attr = Attribute(name='somename')
        >>> attr.check(5)
        True
        >>> attr.check('somestring')
        True
        """
        if self._validator is None:
            return True
        else:
            return (self._validator.match(str(value)) is not None)

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

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5)
        >>> attr.get_value()
        5

        If an invalid data is passed, an AttributeError should be raised.

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value('somevalue')
        Traceback (most recent call last):
            ...
        AttributeError: Invalid input data

        Finally, if the user interface has previously checked data with the
        check method, in order to avoid double check, it is possible to disable
        data check. This way, any data should be set.

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.get_value()
        5
        >>> attr.set_value('somevalue', False)
        >>> attr.get_value()
        'somevalue'

        A value set should enable the modified flag
        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.is_modified()
        True
        """
        if check is True and self.check(value) is False:
            # TODO: be more descriptive
            raise AttributeError('Invalid input data')
        self._value = value
        self._modified = True

    def is_modified(self):
        """
        Returns the modified flag
        """
        return self._modified

    def clear_modified(self):
        """
        Resets the modified flag
        """
        self._modified = False

    def __str__(self):
        """
        Returns object string representation.
        """
        return '<Attribute object {name: %s, vregex: %s, value: %s}>' % \
            (self._name, self._vregex, self._value)


class AttributeSet(object):
    """
    A class that represents a set of attributes.

    Each attrbiute can be fetched using its name (get_attribute), or through
    an iterator (for statement).

    A load method allows to load a set of predefined attributes from
    dictionary (see load method docstring for details)

    """

    def __init__(self, name, attributes=None):
        self._name = name
        self._attributes = {}

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

    def load(self, attributes):
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

        (value, vregex, verrdescr)

        Where 'name' is the attribute name, 'vregex' is the attrbibute regex
        used to check attribute value vaidity while using set_attrbiute methid
        (should be None if you don't want to apply value cehcking), and 'value'
        is the initial attrbiute value (should be None if you don't knwo it).

        >>> attributes = {}
        >>> attributes['somename'] = ('somevalue', None, None)
        >>> attributes['sub'] = {}
        >>> attributes['sub']['someothername'] = ('someothervalue', '^[\w]+$',
        ...                                       'Value should be a string')
        >>> aset = AttributeSet('aset')
        >>> aset.load(attributes)
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

        The load operation should also be atomic. If an attribute loading
        fails, the whole loading should be rollbacked.
        """
        new_attributes = {}

        for key, value in attributes.iteritems():
            if isinstance(value, tuple):
                new_attributes[key] = Attribute(key, value[0], value[1])
            elif isinstance(value, dict):
                new_attributes[key] = AttributeSet(key)
                new_attributes[key].load(value)
            else:
                raise AttributeError('Invalid data format for key %s' % key)

            self._attributes = new_attributes

    def get_attribute(self, name):
        """
        Returns attribute named 'name'

        >>> attributes = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attributes)
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

        >>> attributes = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attributes)
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

        >>> attributes = {}
        >>> attributes['somename'] = ('somevalue', None, None)
        >>> attributes['someothername'] = ('someothervalue', None, None)
        >>> aset = AttributeSet('aset', attributes)
        >>> aset.get_attribute_names()
        ['somename', 'someothername']
        """
        return self._attributes.keys()

    def add_attribute(self, attribute):
        """
        Adds an Attribute anr an AttributeSet.

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

    def __str__(self):
        """
        Returns internal attributes string representation.
        """
        return str(self._attributes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
