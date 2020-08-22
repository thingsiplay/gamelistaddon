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
shutil.rmtree(BUILD_PATH, ignore_errors=True)
os.makedirs(BUILD_PATH, 0o777, True)
run(f'cp "README.md" "{BUILD_DIRNAME}"', False, APP.DIR)

if UI:

    # qt5 designer
    run('pyrcc5 images.qrc -o gui/images_rc.py', True, APP.DIR)
    run('pyuic5 MainWindow.ui --import-from=gui -o gui/MainWindow.py', True, APP.DIR)
    run('pyuic5 About.ui --import-from=gui -o gui/About.py', True, APP.DIR)

if PACKAGE or BUILD:
    
    # readme
    cmd = f'pandoc "{BUILD_DIRNAME}/README.md" -f markdown -t html -o "README.html"'
    run(cmd, True, APP.DIR)
    shutil.copy2('README.html', BUILD_DIRNAME)

if BUILD:

    # nuitka bin
    cmd = 'python3 -m nuitka --follow-imports --standalone --plugin-enable=qt-plugins --python-flag=no_site --remove-output' \
          + f' --output-dir="{BUILD_PATH}" "GamelistAddon.py"'
    run(cmd, True, APP.DIR)
    shutil.move(f'{BUILD_PATH}/GamelistAddon.dist', f'{BUILD_PATH}/{BIN_FOLDER}')
    shutil.copy2(f'{BUILD_PATH}/README.html', f'{BUILD_PATH}/{BIN_FOLDER}')
    shutil.copy2(f'LICENSE', f'{BUILD_PATH}/{BIN_FOLDER}')
    dir = os.path.join(BUILD_PATH, BIN_FOLDER)
    os.makedirs(os.path.join(dir, 'img'), 0o777, True)
    shutil.copy2(os.path.join('img', 'screen_addgame-thumb.png'), f'{dir}')
    shutil.copy2('run', f'{BUILD_PATH}')

if PACKAGE:

    # Remove all annoying pycache folders.
    run('find . | grep -E "(__pycache__$)" | xargs rm -rf', False, APP.DIR)
    
    # python    
    file = f'{BUILD_PATH}/gamelistaddon' + '-' + APP.VERSION + '.tar.gz'
    cmd = f'tar -czvf "{file}" --exclude=make.py *.py constants/*.* gui/*.* gamelistxml/*.* "img/screen_addgame-thumb.png" "README.html" LICENSE'
    run(cmd, True, APP.DIR)

    if BUILD:

        # nuitka bin        
        file = f'{BUILD_PATH}/gamelistaddon-Linux-64Bit' + '-' + APP.VERSION + '.tar.gz'
        cmd = f'tar -czvf "{file}" "{BIN_FOLDER}" run'
        run(cmd, True, BUILD_PATH)

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

        shutil.rmtree(os.path.join(BUILD_PATH, BIN_FOLDER), ignore_errors=True)
        os.remove(os.path.join(BUILD_PATH, 'run'))        
    else:        
        shutil.rmtree(BUILD_PATH, ignore_errors=True)

sys.exit(0)
