#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

class SiteViewMain(object):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    def __init__(self, mode, controller):
        """
        Class initialization.

        The mandatory mode parameter defines whether the view mode to be used.

        - In add mode, the widgets are set in intearcative mode, and a blank
        configuration is used.

        - In edit mode, the widgets are set in interacative mode, and
        configuration loaded from the database is used to fill the widgets.

        - In view mode, the widgets are set non interactive, and
        configuration loaded from the database is used to fill the widgets.
        """
