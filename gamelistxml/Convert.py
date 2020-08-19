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
# base_root is manipulated directly.
# Returns new gameList root object with all new added games only.
# Duplicate mode can be "i" for "ignore" or "u" for "update".
# In ignore mode games from add_root existing in base_root will be ignored.
# In update mode games from add_root will be mixed and merged with every single tag from base_root.
# source is simply a string used as "source" attribute, which will be added to every updated game entry.
def mergeGamelists(base_root, add_root, duplicate='i', source=None, updateonly=None):
    #if updateonly is None:
    #    updateonly = ['name', 'path', 'image', 'marquee', 'video', 'desc', 'developer', 'publisher', 
    #                  'releasedate', 'genre', 'players', 'rating', 'lastplayed', 'playcount',]
    diff_root = ET.fromstring("<?xml version=\"1.0\"?>\n<gameList>\n</gameList>")
    
    # List of paths as a basenames from all games in base_root.
    base_names = []
    for path in base_root.findall('game/path'):
        if path.text is not None:
            base_names.append(os.path.basename(path.text))
        
    if duplicate == 'i': 
           
        for add_game in add_root.findall('game'):
            path = add_game.find('path')
            if path is None or path.text is None:
                path = ''
            else:
                path = path.text
            # Check if new game from add_root is not found in original base_root.
            if len(path) == 0 or os.path.basename(path) not in base_names:
                base_root.append(add_game)
                diff_root.append(add_game)
                
    elif duplicate == 'u': 
           
        for add_game in add_root.findall('game'):
            path = add_game.find('path')
            if path is None or path.text is None:
                path = ''
            else:
                path = path.text            
            if len(path) > 0 and os.path.basename(path) in base_names:
                # Game entry exists. Now update each individual tag.
                
                # First get a copy and remove it from base. The copy will be
                # edited and reinserted later.
                base_game = base_root.find('game/[path="' + path + '"]')
                # Try harder if not found. Check for basename now.
                if base_game is None:
                    for tag in base_root.iter():
                        if tag.tag == 'game':
                            game = tag
                        elif tag.tag == 'path' and tag.text is not None:
                            if os.path.basename(tag.text) == os.path.basename(path):
                                base_game = game
                                break
                            
                base_root.remove(base_game)
                
                updated = False
                # tag is from current new add_game
                for tag in add_game.iter():
                    # Ignore first tag from iter(), as it is always game.
                    if tag.tag != 'game' and (updateonly is None or tag.tag in updateonly):
                        
                        # Get element from base game based on current tag type.
                        # In example "path" element. If the original base game
                        # does have such a tag, remove it.
                        base_tag = base_game.find(tag.tag)
                        
                        if base_tag is not None:
                            base_game.remove(base_tag)
                            base_game.append(tag)
                        
                        # Mark the current game entry as updated, if both tag
                        # content are different. 
                        try:
                            if base_tag.text != tag.text:
                                updated = True
                        except AttributeError:
                            pass
                            
                if updated:
                    if source is not None:
                        base_game.set('source', source)
                    diff_root.append(base_game)
                base_root.append(base_game)
                    
            else:
                # Game entry does not exist. Simply add whole new game.
                base_root.append(add_game)      
    else:
        raise ValueError('Wrong argument value for duplicate in function mergeGamelists(): ' + duplicate)
    indent(base_root)
    indent(diff_root)
    return diff_root


def gameRoot2pathsAndNames(games_root): 
    diff_paths = []
    diff_names = []
    if games_root is not None:  
        for game in games_root.findall('game'):
            element = game.find('path')
            if element is None or element.text is None:
                diff_paths.append('')
            else:
                diff_paths.append(element.text)
            element = game.find('name')
            if element is None or element.text is None:
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
