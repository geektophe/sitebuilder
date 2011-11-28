#!/usr/bin/env python
"""
Site builder GUI is an interface used as frontend to Site builder scheduler
"""

from sitebuilder.application import init, uninit
from sitebuilder.control.list import ListControlAgent
import gtk


def main():
    """
    Appplication main function
    """
    init()
    control = ListControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
    uninit()


if __name__ == '__main__':
    main()
