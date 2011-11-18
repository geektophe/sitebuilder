#!/usr/bin/env python
"""
This module contains several application parameters used in other modules.
"""

from os.path import abspath, dirname

# Glade resources related constants
GLADE_BASEDIR = dirname(abspath( __file__ )) + "/../resources/glade"

# GUI actions related constants
ACTION_SUBMIT = 'submit'
ACTION_CANCEL = 'cancel'
ACTION_ADD    = 'add'
ACTION_VIEW   = 'view'
ACTION_EDIT   = 'edit'
ACTION_DELETE = 'delete'

# The following variables are module closed. They should NEVER be directly set
CONTEXT_NORMAL = 'normal'
CONTEXT_TEST = 'test'

_ALLOWED_APPLICATION_CONTEXTS = (CONTEXT_NORMAL, CONTEXT_TEST )
_APPLICATION_CONTEXT = CONTEXT_NORMAL

def get_application_context():
    """
    Returns the context the application runs in.

    Useful to determine if the application is run from a test session or in
    normal mode.
    """
    global _APPLICATION_CONTEXT
    return _APPLICATION_CONTEXT

def get_allowed_application_contexts():
    """
    Returns the list af allowed contexts the application may run in.

    Useful to determine if the application is run from a test session or in
    normal mode.
    """
    global _ALLOWED_APPLICATION_CONTEXTS
    return _ALLOWED_APPLICATION_CONTEXTS

def set_application_context(context):
    """
    Sets the context the application runs in.
    """
    global _APPLICATION_CONTEXT
    global _ALLOWED_APPLICATION_CONTEXTS

    if not context in _ALLOWED_APPLICATION_CONTEXTS:
        raise RuntimeError("Unknown applicaiton context. Should be one of %s"%\
                           str(_ALLOWED_APPLICATION_CONTEXTS))

    _APPLICATION_CONTEXT = context
