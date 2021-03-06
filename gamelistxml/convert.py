#!/usr/bin/python3

""" Functions to work with gamelist.xml files with gameList-structure.

    The data format is expected to have the gameList-structure from
    gamelist.xml files.  These are the databases for EmulationStation
    games, including the file and meta information generated by a
    scraper.  The functions in this module are for reading, converting
    or manipulating this specific file format.

    https://github.com/RetroPie/EmulationStation/blob/master/GAMELISTS.md

    Usage:
        # Convert from dict example.
        mydict = {
          'path': './file.smc',
          'name': 'Game Title',
          'rating': '0.65'
        }
        xml = convert.dict_to_element(mydict, 'game', APP.SOURCE)
        xml = convert.element_to_tree(xml)
        xml = convert.tree_to_string(xml)

        # How to write example.
        file = 'myfile.xml'
        xml_root.append(xml_element)
        xml_tree = ET.ElementTree()
        convert.indent(xml_root)
        xml_tree._setroot(xml_root)
        try:
            xml_tree.write(file, encoding='UTF-8', xml_declaration=None)
            convert.prepend_filecontent(file, '<?xml version="1.0"?>\n')
"""

import os
import xml.etree.ElementTree as ET
from html import unescape


def dict_to_element(dictionary, tagname, source=None):
    """ Convert a dict into a new ET element.

    Parameters
    ----------
    dictionary : dict
        Regular Python dict object.  Each key/value pair will be
        converted into an ElementTree object and added as a child
        tag element.
    tagname : str
        Name of the top level tag element to create.
    source : None or str, optional
        An optional attribute with the name 'source' and its content
        added to top level of tag element.  None will leave this out.

    Returns
    -------
    ElementTree.Element or None
        New ElementTree.Element object with child tag elements.
        None if an error occurs.

    Raises
    ------
    TypeError
        Value type of argument is not valid.
    """
    element = None
    if isinstance(tagname, str):
        element = ET.Element(tagname)
    elif source is not None:
        raise TypeError('Value type of argument tagname is not valid.')
    if isinstance(source, str):
        element.set('source', source)
    elif source is not None:
        raise TypeError('Value type of argument source is not valid.')
    if isinstance(dictionary, dict):
        for key, val in dictionary.items():
            child = ET.Element(key)
            child.text = str(val)
            element.append(child)
    elif source is not None:
        raise TypeError('Value type of argument tagname is not valid.')
    return element


def element_to_tree(element, xml_root=None):
    """ Convert single tag element into a full XML tree object.

    Parameters
    ----------
    element : ElementTree.Element
        The element with all its tags and content to convert.
    xml_root : None or ElementTree.Element, optional
        Optional base XML with one root element.  If not specified, a
        default root gameList-element will be created.

    Returns
    -------
    ElementTree.ElementTree
        Full XML object with gameList-element and its sub game-element.
    """
    if xml_root is None:
        xml_root = '<?xml version="1.0"?>\n<gameList>\n</gameList>'
        xml_root = ET.fromstring(xml_root)
    xml_root.append(element)
    new_xml_tree = ET.ElementTree()
    new_xml_tree._setroot(xml_root)
    return new_xml_tree


def tree_to_string(xml):
    """ Convert ElementTree to human readable string with indentation.

    Parameters
    ----------
    xml : ElementTree.ElementTree
        An ElementTree XML tree object with it's root.

    Returns
    -------
    str
        Unicode encoded string representation of the xml.  Output is
        indented and formatted to be read by humans.
    """
    xml_root = xml.getroot()
    indent(xml_root)
    return ET.tostring(xml_root, encoding='unicode')


def root_to_pathsnames(gamelist):
    """ Extract path and name lists from a gameList root object.

    Parameters
    ----------
    gameList : ElementTree.Element
        An ElementTree object with a gameList root and game-elements.
        Expects an ET object read from a gamelist.xml file.

    Returns
    -------
    list
        List of all text from path-tag for every game.
    list
        List of all text from name-tag for every game.
    """
    paths = []
    names = []
    if gamelist is not None:
        for game in gamelist.findall('game'):
            paths.append(game.findtext('path', ''))
            paths.append(game.findtext('name', ''))
    return paths, names


def merge_gamelists(base_root, add_root, duplicate='i', source=None,
                    updateonly=None):
    """ Add missing game entries from one XML root to another.

    Takes two ElementTree root objects and combines them into one.  New
    entries from add_root are added to base_root, as it is manipulated
    directly.  The XML structure must be a gameList structure obtained
    from gamelist.xml files.  It will use the basename from path-tag as
    the id to determine if a game exist in base_root.  Both base_root
    and return value are indented ready to write to file.

    Parameters
    ----------
    base_root : ElementTree.Element
        Original XML gameList root to compare against.  This variable
        will be directly modified without making copies.  All new games
        from add_root are added here.
    add_root : ElementTree.Element
        XML gameList root content with game entries to add to
        base_root.  Every game entry is compared against it's path.
    duplicate : {'i', 'u'}
        'i' stands for 'ignore' and 'u' stands for 'update'.  This
        option determines the mode what happens if a game from add_root
        was found in base_root.  ignore will just leave the original
        entry as it is.  update will actually merge both game entries,
        with higher priority on the add_root content.  Every single tag
        is compared individually.  Additionally, the param updateonly
        can modify the behaviour of this duplicate mode.
    source : None or str, optional
        An optional attribute with the name 'source' and its content
        added to top level of tag element.  None will leave this out.
    updateonly : None, list
        Changes how duplicate operates, when its set to 'u'-mode.  Each
        list entry must be a string, containing a tagname.  Then only
        those tags are compared and updated and the others are
        untouched.  Defaults to None, which means update all tags.
        Possible tags: name, sortname, desc, developer, publisher,
        releasedate, genre, players, path, thumbnail, image, marquee,
        video, rating, favorite, hidden, kidgame, lastplayed, playcount

    Returns
    -------
    ElementTree.Element
        XML content with asme gameList structure.  In 'i'-mode, only
        those new added games are included, much like a diff.
        However in 'u'-mode of duplicate and the updateonly parameter
        active, only updated games are included.  In this case, tags
        that are identical in base_root and add_root do not trigger the
        updated status.
    Raises
    ------
    ValueError
        When an argument value is invalid.
    """
    diff_root = '<?xml version="1.0"?>\n<gameList>\n</gameList>'
    diff_root = ET.fromstring(diff_root)
    # List of paths as a basenames from all games in base_root.
    base_names = []
    for path in base_root.findall('game/path'):
        if path.text is not None:
            base_names.append(os.path.basename(path.text))

    if duplicate == 'i':

        for add_game in add_root.findall('game'):
            path = add_game.findtext('path', '')
            # Add game, if its not found in base.
            if (not path) or (os.path.basename(path) not in base_names):
                base_root.append(add_game)
                diff_root.append(add_game)

    elif duplicate == 'u':

        for add_game in add_root.findall('game'):
            path = add_game.findtext('path', '')
            # Check if game is exist in base content.
            if path and os.path.basename(path) in base_names:
                # Game entry exists.  Now update each individual tag.  Get a
                # copy of game entry and remove it from base.  The copy will
                # be manipulated and inserted back later.

                # First look for an exact match of path content.
                base_game = base_root.find(f'game/[path="{path}"]')
                # If not found, try harder.  Check for basename now.
                if base_game is None:
                    basename_path = os.path.basename(path)
                    for tag in base_root.iter():
                        # First element is always the whole game.
                        if tag.tag == 'game':
                            game = tag
                        # Look for path-tag.  Compare the filename portion of
                        # path against the filename from base file.  If they
                        # match, copy it and stop searching.
                        elif tag.tag == 'path' and tag.text is not None:
                            if os.path.basename(tag.text) == basename_path:
                                base_game = game
                                break
                # Remove game, because the edited copy will be inserted later.
                base_root.remove(base_game)

                # Look into all tag-elements from current new add_game.
                updated = False
                for tag in add_game.iter():
                    # Ignore first tag from iter(), as it is always game.
                    if tag.tag == 'game':
                        pass
                    elif updateonly is None or tag.tag in updateonly:
                        # Get element from base game by current tag type from
                        # add_game, in example 'path'-element.
                        base_tag = base_game.find(tag.tag)
                        # Replace tag from base_game with tag from add_game.
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
                # Copy the game to diff, if any update was done.
                if updated:
                    if source is not None:
                        base_game.set('source', source)
                    diff_root.append(base_game)
                base_root.append(base_game)

            else:
                # Game entry does not exist.  Simply add whole new game.
                base_root.append(add_game)
    else:
        raise ValueError('Invalid value for duplicate in merge_gamelists()'
                         f'{duplicate}')
    indent(base_root)
    indent(diff_root)
    return diff_root


def get_game_bypath(root, path):
    """ Search and get game-element from an ElementTree XML root.

    First matching game element will be read.  Comparison is done at
    basename level of path, which means ignoring its directory part
    and comparing filenames only.

    Parameters
    ----------
    root : ElementTree.Element
        ElementTree object with gameList-root and game-sub elements.
        Used as the source xml to look for game entries.
    path : str
        Exact full path to search for.  Although the function will
        extract the basename (means excluding any directory part)
        and compare the filename only.

    Returns
    -------
    ElementTree.Element or None
        game root object with all tags and sub elements if any match is
        found, None otherwise.
    """
    base_path = os.path.basename(path)
    game = None
    for element in root.getiterator('game'):
        element_path = element.findtext('path', '')
        # Get full game-element, if filenames from both path match.
        if base_path == os.path.basename(element_path):
            game = element
            break
    return game


def get_game_byfilters(root, filters=None):
    """ Search and get game-element from an ElementTree XML root.

    The first found game element will be read.  If any filters are
    active, then the first matching game is read.  Only one of the
    filters need to match, not all of them.

    Parameters
    ----------
    root : ElementTree.Element
        A XML root with multiple game elements is expected.
    filters : dict or None
        Multiple pairs of tag names and text, in example
        {'path': '.file', 'favorite': 'true'}.  Each key represents
        the tag name and its value is the tag text.  Every pair is
        searched and compared for each game in root, until one match
        is found.  A match occurs, if
            a) a game has a tag name matching dict key, such as 'path'
            b) and the dict value is found in somewhere in tag text
        None ignores the filter.  Get first game element in this case.

    Returns
    -------
    ElementTree.Element or None
        game root object with all tags and sub elements if any match is
        found, None otherwise.
    dict or None
        If any game is found via matching filter, then the dict
        contains two keys: 'name' and 'text'.  Both contain the values
        from active filters.  None if no match occured or no filter was
        used at all.

    Raises
    ------
    ValueError
        Wrong variable type for parameter 'filters'.
    """
    if isinstance(filters, dict):
        # Filters are active.  Load all game elements from XML content and go
        # through each single game.
        # game_element is a ElementTree.Element
        for game_element in root.findall('game'):
            # filter_name is a string like 'path'
            # filter_text is a string like './filename.smc' or 'true'
            for filter_name, filter_text in filters.items():
                # Check if current game from XML file have a sub element with
                # the same name of the current active filter.  Read the text
                # content of the tag.
                # xml_text is a string like './file.smc' or 'true'
                xml_text = game_element.findtext(filter_name)
                if xml_text is not None:
                    xml_text = unescape(xml_text)
                    # There are two types of filter: string and bool.
                    # bool filter: Compare exact value from filter to lower
                    # case value from tag in game element.
                    # string filter: Value from filter must appear anywhere
                    # in the string from tag in game element.
                    if ((filter_text in ['true', 'false']
                       and filter_text == xml_text.lower())
                       or filter_text in xml_text):
                        # Congratulation! A match is found.  Single filter
                        # match is enough.  Read the entire game content and
                        # stop the search.
                        match = {'name': filter_name, 'text': filter_text}
                        return game_element, match
    # Without filter, just get first entry.
    elif filters is None:
        return root.find('game'), None
    else:
        raise ValueError(f'Wrong type for filters: {type(filters)}')
    return None, None


# Functions created by others.


def indent(element, level=0):
    """ Indents an XML root object from ElementTree.

    Parameters
    ----------
    element : ElementTree.Element
        The XML root object to manipulate and indent.
    level : int, optional
        I guess at which level of indentation it should start.  Can be
        ignored and used with default value of 0.

    Returns
    -------
    ElementTree.Element
        Same object as input, but indented.

    Notes
    -----
    This function is not created by me. The original source is:
    https://effbot.org/zone/element-lib.htm#prettyprint
    2004 by Fredrik Lundh
    """
    i = '\n' + level * '  '
    # if len(element)
    if element:
        if not element.text or not element.text.strip():
            element.text = i + '  '
        if not element.tail or not element.tail.strip():
            element.tail = i
        for element in element:
            indent(element, level + 1)
        if not element.tail or not element.tail.strip():
            element.tail = i
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = i
    return element


def prepend_filecontent(filepath, new_content):
    """ Add a line to beginning of an existing text file.

    Parameters
    ----------
    filepath : str
        Path to an existing file to open and overwrite.  The content
        will be added to the head of this file.
    new_content : str
        Text to add to the opened file.

    Returns
    -------
    str
        Same merged content written to file.

    Notes
    -----
    The file should exist, no error checking is done.
    """
    with open(filepath, 'r') as original:
        old_content = original.read()
    with open(filepath, 'w') as modified:
        modified.write(new_content + old_content)
    return new_content + old_content
