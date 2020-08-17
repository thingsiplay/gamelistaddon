#!/usr/bin/python3

import os
import xml.etree.ElementTree as ET
from html import escape, unescape

# 1: Convert a Python dictionary into an ElementTree element.
# tag is the main tag to put all dictionary content as childs.
def dict2xmlElement(tag, d, source=None):
    element = ET.Element(tag)
    if source is not None and len(source) > 0:
        element.set('source', source)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        element.append(child)
    return element

# Shortcut
def dict2xmlGameElement(d, source=None):
    return dict2xmlElement('game', d, source)

# 2: Convert a single ElementTree element into a full ElementTree XML tree object.
# If no ElementTree xmlroot is given, a default one with "gamelist" as new root will be created.
def xmlElement2xmlTree(element, xmlroot=None):
    if xmlroot is None:
        xmlroot = ET.fromstring("<?xml version=\"1.0\"?>\n<gameList>\n</gameList>")
    xmlroot.append(element)
    new_xml_tree = ET.ElementTree()
    new_xml_tree._setroot(xmlroot)
    return new_xml_tree

# 3: Convert an ElementTree XML tree object into human readable string representation with indentation.
def xmlTree2rootString(xml):
    xmlroot = xml.getroot()
    indent(xmlroot)
    xmlroot = ET.tostring(xmlroot, encoding="unicode")
    return xmlroot

# Adds missing games from new ElementTree root into original root. Check is done by path as id.
# Returns 4 objects: original_root, diff_root, diff_paths, diff_names.
# Both root objects are ElementTree root objects. The diff_paths and diff_names are regular lists of new added games.
def OLDmergeGamelists(original_root, new_root):
    # diff will contain all newly added games.
    diff_root = ET.fromstring("<?xml version=\"1.0\"?>\n<gameList>\n</gameList>")
    original_games = original_root.findall('game')
    new_games = new_root.findall('game')
    # This will be used to check if a game exist in the original file, by comparing the basename only.
    original_basenames = []
    for path in original_root.findall('game/path'):
        original_basenames.append(os.path.basename(path.text))
    diff_paths = []
    diff_names = []
    # game is an ElementTree Element with all its structure.
    for game in new_games:
        path = game.find('path')
        if path is None:
            path = ''
        else:
            path = path.text
        # Add the current game to end result, if its path is not matching to the original games list.
        if len(path) == 0 or os.path.basename(path) not in original_basenames:
            original_root.append(game)
            diff_root.append(game)
            diff_paths.append(path)
            name = game.find('name')
            if name is None:
                diff_names.append('')
            else:
                diff_names.append(name.text)
    indent(original_root)
    indent(diff_root)
    return original_root, diff_root, diff_paths, diff_names


def mergeGamelists(base_root, add_root):  
    diff_root = ET.fromstring("<?xml version=\"1.0\"?>\n<gameList>\n</gameList>")
    
    # List of paths as a basenames from all games in base_root.
    base_names = []
    for path in base_root.findall('game/path'):
        base_names.append(os.path.basename(path.text))
    
    # Go through all new to add game entries.
    for game in add_root.findall('game'):
        path = game.find('path')
        if path is None:
            path = ''
        else:
            path = path.text
        # Check if new game from add_root is not found in original base_root.
        if len(path) == 0 or os.path.basename(path) not in base_names:
            base_root.append(game)
            diff_root.append(game)
    
    indent(base_root)
    indent(diff_root)
    return diff_root

def gameRoot2pathsAndNames(games_root): 
    diff_paths = []
    diff_names = []
    if games_root is not None:  
        for game in games_root.findall('game'):
            element = game.find('path')
            if element is None:
                diff_paths.append('')
            else:
                diff_paths.append(element.text)
            element = game.find('name')
            if element is None:
                diff_names.append('')
            else:
                diff_names.append(element.text)
    return diff_paths, diff_names

# https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python#33956544
#   by user: Erick M. Sprengel
# Indents an xml root object from ElementTree.
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem

# Add a line to the beginning of an existing text file. The file should exist, no error checking is done here.
def prepend_filecontent(filepath, new_content):
    with open(filepath, 'r') as original:
        old_content = original.read()
    with open(filepath, 'w') as modified:
        modified.write(new_content + old_content)
    return new_content + old_content
