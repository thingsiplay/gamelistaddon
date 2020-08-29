#!/usr/bin/python3

""" Combine two gamelist.xml files to add missing game entries.

    Standalone commandline version of the merge functionality from
    Gamelist Addon program. Usage:

        merge.py -h
        merge.py -b input1.xml -a input2.xml -o out.xml
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET

from gamelistxml import Convert
from constants import App

if __name__ == '__main__':
    APP = App.App(__file__)

    parser = argparse.ArgumentParser(
        prog='merge.py',
        description=(f'merge.py from {APP.NAME}.  Combine '
                     'two gamelist.xml files to add missing game entries.'))
    parser.add_argument(
        '--version', '-v', action='version', version=APP.VERSION)
    parser.add_argument(
        '--base', '-b', metavar='file', required=True, type=str,
        help='Original gamelist.xml to compare against.')
    parser.add_argument(
        '--add', '-a', metavar='file', required=True, type=str,
        help='Gamelist.xml file with new content to add.')
    parser.add_argument(
        '--output', '-o', metavar='file', required=False, type=str,
        help='(optional) Save resulting combined xml as new file.')
    parser.add_argument(
        '--log', '-l', metavar='file', required=False, type=str,
        help='(optional) Save new added games as xml log file.')
    parser.add_argument(
        '--duplicate', '-d', metavar='mode', required=False, type=str,
        default='ignore', choices=['ignore', 'update'],
        help=('(optional) What to do if game entry exist already?\n'
                'Modes: "ignore" (default), "update"'))
    parser.add_argument(
        '--tag', '-t', metavar='tagname', required=False, type=str,
        action='append', default=None,
        choices=['name', 'sortname', 'desc', 'developer', 'publisher',
                 'releasedate', 'genre', 'players', 'path', 'thumbnail',
                 'image', 'marquee', 'video', 'rating', 'favorite', 'hidden',
                 'kidgame', 'lastplayed', 'playcount'],
        help=('(optional) Limit updates to specified tags only, when using '
              '"-d update" mode.  This argument can be specified multiple '
              'times.  Possible tags: name, sortname, desc, developer, '
              'publisher, releasedate, genre, players, path, thumbnail, '
              'image, marquee, video, rating, favorite, hidden, kidgame, '
              'lastplayed, playcount'))
    args = parser.parse_args()

    try:
        # Check if specified input files exist.
        os.path.exists(args.base)
        os.path.exists(args.add)
        # Build up necessary arguments and read xml files.
        original_root = ET.parse(args.base).getroot()
        new_root = ET.parse(args.add).getroot()
        if args.duplicate == 'ignore':
            DUPLICATE_MODE = 'i'
        elif args.duplicate == 'update':
            DUPLICATE_MODE = 'u'
        else:
            DUPLICATE_MODE = None
        # Merge the xml files and get the diff for log.
        diff_root = Convert.merge_gamelists(original_root, new_root,
                                           DUPLICATE_MODE, APP.SOURCE,
                                           args.tag)
        diff_paths, diff_names = Convert.root_to_pathsnames(diff_root)
        # Write the merged xml and diff log files.
        if args.output is not None:
            save_tree = ET.ElementTree()
            save_tree._setroot(original_root)
            save_tree.write(args.output, encoding='UTF-8',
                            xml_declaration=None)
            Convert.prepend_filecontent(args.output, '<?xml version="1.0"?>\n')
        if args.log is not None:
            save_tree = ET.ElementTree()
            save_tree._setroot(diff_root)
            save_tree.write(args.log, encoding='UTF-8', xml_declaration=None)
            Convert.prepend_filecontent(args.log, '<?xml version="1.0"?>\n')
    except Exception:
        print('ERROR')
    else:
        for path in diff_paths:
            print(path)
    sys.exit(0)
