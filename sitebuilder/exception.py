#!/usr/bin/env python
"""
Various custom exceptions used in application
"""

class FieldFormatError(Exception):
    """
    Exception that should be risen when a field format is wrong to notify
    views. It then may dispaly a relevant error message to the user.

    The exception should contain the required format rather the the technical
    reason it was reasen.
    """


class LookupError(Exception):
    """
    Exception that should be risen when a search has failed in the backend
    driver.
    """
