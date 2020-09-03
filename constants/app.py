#!/usr/bin/python3

""" Provides basic meta information about the main program.

    What this class does is basically saving constants about the main
    program.  The main benefit realizing this as a class is to be able
    to easily import and read by other tools, in example to read the
    current version number.

    Usage:
        APP = app.App(__file__)
        print(APP.VERSION)
"""

import os.path
from pathlib import Path


class App():

    """ Meta information about the calling project.

    Attributes
    ----------
    NAME : str
        Name of the app or project.
    SOURCE : str
        The sourece string which is added when the main app adds a
        source attribute to the game-elements in the XML files.  It
        serves as an id.
    VERSION : str
        Current version of the project.
    CREATOR : str
        Developer and creator of the project.
    DESC : str
        Short description of the project.
    LICENSE : str
        License text of the project.
    EXEPATH : str
        Full path of the current executed application.  This solves
        links too, so the attribute will point to the final Python
        script.
    DIR : str
        Basically EXEPATH without filename, just the directory portion.
    """

    def __init__(self, path_of_calling_app):
        self.NAME = 'Gamelist Addon'
        self.SOURCE = 'gamelistaddon'
        self.VERSION = '0.4'
        self.CREATOR = 'Tuncay D.'
        self.DESC = ('Add new game entries to gamelist.xml files '
                     'created for EmulationStation.')
        self.LICENSE = (
'Copyright (C) 2020 Tuncay D'
'\n\n'
'Permission is hereby granted, free of charge, to any person obtaining'
'a copy of this software and associated documentation files (the'
'"Software"), to deal in the Software without restriction, including'
'without limitation the rights to use, copy, modify, merge, publish,'
'distribute, sublicense, and/or sell copies of the Software, and to'
'permit persons to whom the Software is furnished to do so, subject to'
'the following conditions:'
'\n\n'
'The above copyright notice and this permission notice shall be'
'included in all copies or substantial portions of the Software.'
'\n\n'
'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,'
'EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF'
'MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND'
'NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY'
'CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,'
'TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE'
'SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
'\n\n'
'Except as contained in this notice, the name(s) of the above copyright'
'holders shall not be used in advertising or otherwise to promote the sale,'
'use or other dealings in this Software without prior written'
'authorization.'
)
        self.EXEPATH = Path(path_of_calling_app).resolve()
        self.DIR = os.path.dirname(self.EXEPATH)
