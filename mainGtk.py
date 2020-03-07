#!/usr/bin/python3

"""Entry point"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from windows.main import MainWindow

# TODO:
# Write glade file
# Apply flake8 to codebase
# Develop basic structures (Point, Line, Wire_Frame, Display_File)
# Rename this file to 'z'

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.show()
    Gtk.main()
