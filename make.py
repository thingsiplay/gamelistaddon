#!/usr/bin/python3

from constants import App

import os.path
import subprocess
import shutil
import sys
import argparse

def command_exist(cmd, checkVersion=True):
    if checkVersion:
        checkVersion = 'command -v '
    else:
        checkVersion = ''
    output = subprocess.run(checkVersion + cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout
    if len(output) == 0:
        raise NotImplementedError('command does not exist: ' + cmd)

def run(cmd, write=True, dir=None):
    print('run:', cmd)
    output = subprocess.run(cmd, cwd=dir, shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout
    if write and len(output) > 0:
        print(str(output))

# init
APP = App.App(__file__)
# Mother directory to operate and build in.
DIR = 'dist'
# Folder name used with BUILD. This is just a folder name, created inside DIR.
BIN_FOLDER = 'GamelistAddon'
# Default values if no commandline options are available.
SETUP = True
UI = True
BUILD = True
PACKAGE = True
CLEAN = True

# commandline options
parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description='make for GamelistAddon')
parser.add_argument('--setup', action='store_true', help='Test if required apps are installed.')
parser.add_argument('--ui', action='store_true', help='Convert resources and ui files from qt5 designer.')
parser.add_argument('--build', action='store_true', help='Compile and build standalone distribution.')
parser.add_argument('--package', action='store_true', help='Create various archives.')
parser.add_argument('--clean', action='store_true', help='Remove temporary files.')
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
    
    if UI:
        command_exist('pyuic5')
        command_exist('pyrcc5')
        
    if BUILD:    
        command_exist('pip3 freeze | grep Nuitka', False)
    
    if PACKAGE:
        command_exist('pandoc')


# create fresh dist folder
run(f'rm -R -f "{DIR}"', False, APP.DIR)
run(f'mkdir -p "{DIR}"', False, APP.DIR)
run(f'cp "README.md" "{DIR}"', False, APP.DIR)

if UI:

    # qt5 designer
    run('pyrcc5 images.qrc -o gui/images_rc.py', True, APP.DIR)
    run('pyuic5 MainWindow.ui --import-from=gui -o gui/MainWindow.py', True, APP.DIR)
    run('pyuic5 About.ui --import-from=gui -o gui/About.py', True, APP.DIR)

if PACKAGE or BUILD:
    
    # readme
    cmd = f'pandoc "{DIR}/README.md" -f markdown -t html -o "README.html"'
    run(cmd, True, APP.DIR)
    shutil.copy2('README.html', DIR)

if BUILD:

    # nuitka bin
    run(f'mkdir -p "{DIR}"', False, APP.DIR)
    cmd = 'python3 -m nuitka --follow-imports --standalone --plugin-enable=qt-plugins --python-flag=no_site --remove-output' \
          + f' --output-dir="{DIR}" "GamelistAddon.py"'
    run(cmd, True, APP.DIR)
    shutil.move(f'{DIR}/GamelistAddon.dist', f'{DIR}/{BIN_FOLDER}')
    shutil.copy2(f'{DIR}/README.html', f'{DIR}/{BIN_FOLDER}')
    shutil.copy2(f'LICENSE', f'{DIR}/{BIN_FOLDER}')
    run(f'mkdir -p {DIR}/{BIN_FOLDER}/img', False, APP.DIR)
    shutil.copy2(f'img/screen_addgame-thumb.png', f'{DIR}/{BIN_FOLDER}/img')
    shutil.copy2('run', f'{DIR}')

if PACKAGE:

    # init
    run(f'mkdir -p "{DIR}"', False, APP.DIR)
    # Remove all annoying pycache folders.
    run('find . | grep -E "(__pycache__$)" | xargs rm -rf', False, APP.DIR)
    
    # python    
    file = f'{DIR}/gamelistaddon' + '-' + APP.VERSION + '.tar.gz'
    cmd = f'tar -czvf "{file}" --exclude=make.py *.py constants/*.* gui/*.* gamelistxml/*.* "img/screen_addgame-thumb.png" "README.html" LICENSE'
    run(cmd, True, APP.DIR)

    if BUILD:

        # nuitka bin        
        file = 'gamelistaddon-Linux-64Bit' + '-' + APP.VERSION + '.tar.gz'
        cmd = f'tar -czvf "{file}" "{BIN_FOLDER}" run'
        run(cmd, True, os.path.join(APP.DIR, DIR))

if CLEAN:

    # temporary files
    run('rm -f README.md', False, os.path.join(APP.DIR, DIR))
    run('rm -f README.html', False, os.path.join(APP.DIR, DIR))
    run('rm -R -f build', False, APP.DIR)
    run('find . | grep -E "(__pycache__$)" | xargs rm -rf', False, APP.DIR)

    if PACKAGE and BUILD:

        run(f'rm -R -f "{BIN_FOLDER}"', False, os.path.join(APP.DIR, DIR))
        run('rm -f "run"', False, os.path.join(APP.DIR, DIR))

sys.exit(0)
