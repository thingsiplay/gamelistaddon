#!/usr/bin/python3

import sys
import os.path
from pathlib import Path

# Contains application related constants.
# Call it like:
#   APP = App.App(__file__)
#   print(APP.NAME)
class App():
    def __init__(self, Path_of_calling_app):
        # Meta information
        self.NAME = 'Gamelist Addon'
        self.SOURCE = 'gamelistaddon'
        self.VERSION = '0.3'
        self.CREATOR = 'Tuncay D.'
        self.DESC = 'Add new game entries to gamelist.xml files created for EmulationStation.'
        self.LICENSE = """Copyright (C) 2020 Tuncay D

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization."""
        # Full path to the programs executable. This is not the script itself, it can be a container file from which
        # it was called from, such as pyinstallers --onefile build. This also resolves any links to the app, so it can
        # be called by any link.
        self.EXEPATH = Path(Path_of_calling_app).resolve()
        self.DIR = os.path.dirname(self.EXEPATH)
        self.INSTALLDIR = os.path.split(self.EXEPATH)[0]
