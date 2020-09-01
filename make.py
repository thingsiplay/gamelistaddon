#!/usr/bin/python3

""" Custom make script to build and bundle the GamelistAddon app.

    First requirements are checked, mostly consisting of Python
    version and if needed commands are installed.  Then all parts are
    build and cleaned up.  Using any commandline arguments will cause
    to do only whats specified and deactivate everything else.

    Running without arguments will convert the gui related stuff to
    Python code, documentation to readable format, build a standalone
    version with nuitka (takes a long time), package several archives
    for distribution and delete some temporary files and folders.

    While a few files are created or updated in the main directory,
    a new subfolder named 'dist' (if not changed) will be created.
    This folder contains the archives/packages for distribution.

    Usage:
        ./make.py --help
        ./make.py
        ./make.py --ui --clean
"""

import os.path
import subprocess
import shutil
import sys
import argparse

from constants import app


def command_exist(command, check_command=True):
    """ Test if the command exist.

    Parameters
    ----------
    command : str
        Name of a command to check for existence, such as python3.
        Or if if check_command is False, this should be a full
        command with possible arguments.  It should output something,
        otherwiese the command is considered as not found.
    check_command : bool
        If True, the check is done with the 'command -v' approach, as
        it is probably the most stable way to test.  If the argument
        is False, then the cmd will be executed as it is and the user
        is responsible.

    Raises
    ------
    OSError
        In case the desired command does not exist or is not found.
    """
    if check_command:
        command = f'command -v {command}'
    output = subprocess.run(command, shell=True, check=True, encoding='utf-8',
                            stdout=subprocess.PIPE).stdout
    if not output:
        raise OSError(f'Command does not exist: {command}')


def run(command, write=True, wdir=None):
    """ Execute a shell command.

    Parameters
    ----------
    write : bool
        If this is true and an output is available, then the output is
        printed out.
    wdir : None or str
        Path to a directory.  Command is executed within this path as
        the current working directory is changed temporary.
    """
    print('run:', command)
    output = subprocess.run(command, check=True, shell=True, encoding='utf-8',
                            cwd=wdir, stdout=subprocess.PIPE).stdout
    if write and output:
        print(str(output))


# init
APP = app.App(__file__)
# Mother directory to operate and build in. Should be a folder name, as it is
# joined by absolute path APP.DIR.
# Important: Be careful with this, as rmtree on this folder will be done.
BUILD_DIRNAME = 'dist'
# Same as BUILD_DIR, but as a full path.
BUILD_PATH = os.path.join(APP.DIR, BUILD_DIRNAME)
# Folder name used with BUILD. This is just a folder name, created inside DIR.
BIN_FOLDER = 'GamelistAddon'
# Default values if no commandline options are available.
SETUP = True
UI = True
BUILD = True
PACKAGE = True
CLEAN = True

# commandline options
parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='make for GamelistAddon')
parser.add_argument('--setup', action='store_true',
                    help='Test if required apps are installed.')
parser.add_argument('--ui', action='store_true',
                    help='Convert resources and ui files from qt5 designer.')
parser.add_argument('--build', action='store_true',
                    help='Compile and build standalone distribution.')
parser.add_argument('--package', action='store_true',
                    help='Create various archives.')
parser.add_argument('--clean', action='store_true',
                    help='Remove temporary files.')
args = parser.parse_args()

if len(sys.argv) > 1:

    SETUP = args.setup
    UI = args.ui
    BUILD = args.build
    PACKAGE = args.package
    CLEAN = args.clean

if SETUP:

    # requirements
    command_exist('python3')
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise OSError('At least Python version 3.6 is required.')

    if UI:
        command_exist('pyuic5')
        command_exist('pyrcc5')

    if BUILD:
        command_exist('pip3 freeze | grep Nuitka', False)

    if PACKAGE:
        command_exist('pandoc')

# create fresh dist folder
shutil.rmtree(BUILD_PATH, ignore_errors=True)
os.makedirs(BUILD_PATH, 0o777, True)
run(f'cp "README.md" "{BUILD_DIRNAME}"', False, APP.DIR)

if UI:

    # qt5 designer
    run('pyrcc5 images.qrc -o gui/images_rc.py',
        True, APP.DIR)
    run('pyuic5 MainWindow.ui --import-from=gui -o gui/MainWindow.py',
        True, APP.DIR)
    run('pyuic5 About.ui --import-from=gui -o gui/About.py',
        True, APP.DIR)

if PACKAGE or BUILD:

    # readme
    cmd_ = (f'pandoc "{BUILD_DIRNAME}/README.md" '
            '-f markdown -t html -o "README.html"')
    run(cmd_, True, APP.DIR)
    shutil.copy2('README.html', BUILD_DIRNAME)

if BUILD:

    # nuitka bin
    cmd_ = ('python3 -m nuitka --follow-imports --standalone '
            '--plugin-enable=qt-plugins --python-flag=no_site --remove-output '
            f'--output-dir="{BUILD_PATH}" "GamelistAddon.py"')
    run(cmd_, True, APP.DIR)
    shutil.move(f'{BUILD_PATH}/GamelistAddon.dist',
                f'{BUILD_PATH}/{BIN_FOLDER}')
    shutil.copy2(f'{BUILD_PATH}/README.html',
                 f'{BUILD_PATH}/{BIN_FOLDER}')
    shutil.copy2('LICENSE',
                 f'{BUILD_PATH}/{BIN_FOLDER}')

    dir_ = os.path.join(BUILD_PATH, BIN_FOLDER)
    dir_ = os.path.join(dir_, 'img')
    os.makedirs(dir_, 0o777, True)

    img_ = os.path.join(APP.DIR, 'img')
    img_ = os.path.join(img_, 'screen_addgame-thumb.png')
    shutil.copy2(img_, dir_)

    shutil.copy2('run', BUILD_PATH)

if PACKAGE:

    # Remove all annoying pycache folders.
    run('find . | grep -E "(__pycache__$)" | xargs rm -rf', False, APP.DIR)

    # python
    file = f'{BUILD_PATH}/gamelistaddon-{APP.VERSION}.tar.gz'
    cmd_ = (f'tar -czvf "{file}" --exclude=make.py *.py constants/*.* gui/*.* '
            'gamelistxml/*.* "img/screen_addgame-thumb.png" "README.html" '
            'LICENSE')
    run(cmd_, True, APP.DIR)

    if BUILD:

        # nuitka bin
        file = f'{BUILD_PATH}/gamelistaddon-Linux-64Bit-{APP.VERSION}.tar.gz'
        cmd_ = f'tar -czvf "{file}" "{BIN_FOLDER}" run'
        run(cmd_, True, BUILD_PATH)

if CLEAN:

    # temporary files
    try:
        os.remove(os.path.join(BUILD_PATH, 'README.md'))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.path.join(BUILD_PATH, 'README.html'))
    except FileNotFoundError:
        pass
    shutil.rmtree(os.path.join(APP.DIR, 'build'), ignore_errors=True)
    run('find . | grep -E "(__pycache__$)" | xargs rm -rf', False, APP.DIR)

    if PACKAGE and BUILD:

        shutil.rmtree(os.path.join(BUILD_PATH, BIN_FOLDER),
                      ignore_errors=True)
        os.remove(os.path.join(BUILD_PATH, 'run'))
    else:
        shutil.rmtree(BUILD_PATH, ignore_errors=True)

sys.exit(0)
