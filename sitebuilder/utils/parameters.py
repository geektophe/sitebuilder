#!/usr/bin/env python
"""
This module contains several application parameters used in other modules.
"""

from os.path import abspath, dirname

# Glade resources related constants
GLADE_BASEDIR = dirname(abspath( __file__ )) + "/../resources/glade"

# GUI actions related constants
ACTION_SUBMIT    = u'submit'
ACTION_CANCEL    = u'cancel'
ACTION_ADD       = u'add'
ACTION_VIEW      = u'view'
ACTION_EDIT      = u'edit'
ACTION_DELETE    = u'delete'
ACTION_RELOAD    = u'reload'
ACTION_CLEARLOGS = u'clearlogs'
ACTION_SHOWLOGS  = u'showlogs'

# The following variables are module closed. They should NEVER be directly set
CONTEXT_NORMAL = u'normal'
CONTEXT_TEST = u'test'

_ALLOWED_APPLICATION_CONTEXTS = (CONTEXT_NORMAL, CONTEXT_TEST )
_APPLICATION_CONTEXT = CONTEXT_NORMAL

def get_application_context():
    """
    Returns the context the application runs in.

    Useful to determine if the application is run from a test session or in
    normal mode.
    """
    return _APPLICATION_CONTEXT

def get_allowed_application_contexts():
    """
    Returns the list af allowed contexts the application may run in.

    Useful to determine if the application is run from a test session or in
    normal mode.
    """
    return _ALLOWED_APPLICATION_CONTEXTS

def set_application_context(context):
    """
    Sets the context the application runs in.
    """
    global _APPLICATION_CONTEXT

    if not context in _ALLOWED_APPLICATION_CONTEXTS:
        raise RuntimeError("Unknown applicaiton context. Should be one of %s"%\
                           str(_ALLOWED_APPLICATION_CONTEXTS))

    _APPLICATION_CONTEXT = context
