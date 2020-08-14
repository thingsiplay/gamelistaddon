#!/usr/bin/python3

from gamelistxml import Convert
from constants import App

import xml.etree.ElementTree as ET
from os import path
import sys
import argparse

if __name__ == '__main__':
    APP = App.App(__file__)

    parser = argparse.ArgumentParser(prog='merge',
        description='merge from ' + APP.NAME + '. Combine two gamelist.xml files to add missing game entries.')
    parser.add_argument('--version', '-v', action='version', version=APP.VERSION)
    parser.add_argument('--base', '-b', metavar='file', required=True, type=str, help='Original gamelist.xml to compare against.')
    parser.add_argument('--add', '-a', metavar='file', required=True, type=str, help='Gamelist.xml file with new content to add.')
    parser.add_argument('--output', '-o', metavar='file', required=False, type=str, help='Save resulting combined xml as new file. (optional)')
    parser.add_argument('--log', '-l', metavar='file', required=False, type=str, help='Save new added games only as xml log file. (optional)')
    args = parser.parse_args()

    try:
        original_file = args.base
        new_file = args.add
        save_file = args.output
        os.path.exists(original_file)
        os.path.exists(new_file)
        if args.output is not None:
            os.path.exists(save_file)
        original_root = ET.parse(original_file).getroot()
        new_root = ET.parse(new_file).getroot()
        save_root, diff_root, diff_paths, diff_names = Convert.mergeGamelists(original_root, new_root)
        if args.output is not None:
            save_tree = ET.ElementTree()
            save_tree._setroot(save_root)
            save_tree.write(save_file, encoding="UTF-8", xml_declaration=None)
            Convert.prepend_filecontent(save_file, "<?xml version=\"1.0\"?>\n")
        if args.log is not None:
            os.path.exists(args.log)
            save_tree = ET.ElementTree()
            save_tree._setroot(diff_root)
            save_tree.write(args.log, encoding="UTF-8", xml_declaration=None)
            Convert.prepend_filecontent(args.log, "<?xml version=\"1.0\"?>\n")
    except:
        print('ERROR')
    else:
        for path in diff_paths:
            print(path)

    sys.exit(0)
