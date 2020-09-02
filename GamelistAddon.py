#!/usr/bin/python3

""" GUI tool to add or merge game entries in a gamelist.xml files.

    In the 'Add Game' view the user fills a form.  This data can be
    saved to a new XML file in the format of gameList-structure for
    EmulationStation.  It can also be added to an existing file.

    The 'Merge Gamelists' view needs two gamelist.xml files as input.
    It will then combine them into a new file by adding or updating
    game-entries from those files.  Additionally a log with the new or
    updated entries are displayed.

    Look into README.md or README.html for more info.  Also the module
    constants/app.py contains some meta information, such as the
    projects version.

    Usage:
        ./GamelistAddon.py
"""

import os.path
import sys
import subprocess
import xml.etree.ElementTree as ET
import urllib.parse
from html import escape, unescape

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from gui.MainWindow import Ui_MainWindow
from gui.About import Ui_dialog_about
from gamelistxml import convert
from constants import app


class MainWin(qtw.QMainWindow):
    """ Main window and functionality of the application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Last saved data
        self.diff_names = []
        self.diff_paths = []
        self.diff_root = None

        # Variables for duplicate check of certain actions.
        # Used by the method
        self.last_le_releasedate_editingFinished_check = None
        self.last_save_file = None
        self.last_import_file = None
        self.last_default_dir = os.getcwd()

        # Menu and other essentials
        self.tab_mode = self.findChild(qtw.QTabWidget, 'tab_mode')
        self.statusbar = self.findChild(qtw.QStatusBar, 'statusbar')
        self.menuHelp = self.findChild(qtw.QMenu, 'menuHelp')
        self.actionAbout = self.findChild(qtw.QAction, 'actionAbout')
        self.actionClose = self.findChild(qtw.QAction, 'actionClose')
        self.actionReadme = self.findChild(qtw.QAction, 'actionReadme')

        # Tab indexes
        self.tabindex_settings_merge = 2  # tab_3

        # Menu handler connection
        self.actionAbout.triggered.connect(self.actionAbout_triggered)
        self.actionClose.triggered.connect(self.actionClose_triggered)
        self.actionReadme.triggered.connect(self.actionReadme_triggered)

        # Labels for Edit Widgets
        self.l_name = self.findChild(qtw.QLabel, 'l_name')
        self.l_path = self.findChild(qtw.QLabel, 'l_path')
        self.l_image = self.findChild(qtw.QLabel, 'l_image')
        self.l_marquee = self.findChild(qtw.QLabel, 'l_marquee')
        self.l_video = self.findChild(qtw.QLabel, 'l_video')
        self.l_desc = self.findChild(qtw.QLabel, 'l_desc')
        self.l_developer = self.findChild(qtw.QLabel, 'l_developer')
        self.l_publisher = self.findChild(qtw.QLabel, 'l_publisher')
        self.l_releasedate = self.findChild(qtw.QLabel, 'l_releasedate')
        self.l_genre = self.findChild(qtw.QLabel, 'l_genre')
        self.l_players = self.findChild(qtw.QLabel, 'l_players')
        self.l_rating = self.findChild(qtw.QLabel, 'l_rating')

        self.l_original_merge = self.findChild(qtw.QLabel, 'l_original_merge')
        self.l_new_merge = self.findChild(qtw.QLabel, 'l_new_merge')

        # Edit Widgets
        self.le_name = self.findChild(qtw.QLineEdit, 'le_name')
        self.le_path = self.findChild(qtw.QLineEdit, 'le_path')
        self.le_image = self.findChild(qtw.QLineEdit, 'le_image')
        self.le_marquee = self.findChild(qtw.QLineEdit, 'le_marquee')
        self.le_video = self.findChild(qtw.QLineEdit, 'le_video')
        self.pte_desc = self.findChild(qtw.QPlainTextEdit, 'pte_desc')
        self.le_developer = self.findChild(qtw.QLineEdit, 'le_developer')
        self.le_publisher = self.findChild(qtw.QLineEdit, 'le_publisher')
        self.le_releasedate = self.findChild(qtw.QLineEdit, 'le_releasedate')
        self.le_genre = self.findChild(qtw.QLineEdit, 'le_genre')
        self.le_players = self.findChild(qtw.QLineEdit, 'le_players')
        self.le_rating = self.findChild(qtw.QLineEdit, 'le_rating')
        self.le_sortname = self.findChild(qtw.QLineEdit, 'le_sortname')
        self.le_thumbnail = self.findChild(qtw.QLineEdit, 'le_thumbnail')

        self.le_original_merge = self.findChild(
            qtw.QLineEdit, 'le_original_merge')
        self.le_new_merge = self.findChild(qtw.QLineEdit, 'le_new_merge')
        self.pte_log_merge = self.findChild(
            qtw.QPlainTextEdit, 'pte_log_merge')

        # Edit Widgets handler connection
        self.le_path.textChanged.connect(self.le_path_textChanged)

        self.le_original_merge.textChanged.connect(
            self.le_original_merge_textChanged)
        self.le_new_merge.textChanged.connect(self.le_new_merge_textChanged)

        # Edit Widgets validators
        reg_ex = qtc.QRegExp(r'[1-2]\d\d\d?([01]\d?([0-3]\d)?)?')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_releasedate)
        self.le_releasedate.setValidator(input_validator)

        reg_ex = qtc.QRegExp(r'[1-9]\d?')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_players)
        self.le_players.setValidator(input_validator)

        self.le_rating = self.findChild(qtw.QLineEdit, 'le_rating')
        reg_ex = qtc.QRegExp(r'(0\.\d\d|1\.00)')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_rating)
        self.le_rating.setValidator(input_validator)

        # Buttons and Checkbox Widgets
        self.cb_favorite = self.findChild(qtw.QCheckBox, 'cb_favorite')
        self.cb_hidden = self.findChild(qtw.QCheckBox, 'cb_hidden')
        self.cb_kidgame = self.findChild(qtw.QCheckBox, 'cb_kidgame')

        self.b_new_addgame = self.findChild(qtw.QPushButton, 'b_new_addgame')
        self.b_import_addgame = self.findChild(
            qtw.QPushButton, 'b_import_addgame')
        self.b_preview_addgame = self.findChild(
            qtw.QPushButton, 'b_preview_addgame')
        self.b_save_addgame = self.findChild(qtw.QPushButton, 'b_save_addgame')

        self.tb_original_merge = self.findChild(
            qtw.QToolButton, 'tb_original_merge')
        self.tb_new_merge = self.findChild(qtw.QToolButton, 'tb_new_merge')
        self.b_save_merge = self.findChild(qtw.QPushButton, 'b_save_merge')
        self.rb_name_merge = self.findChild(qtw.QRadioButton, 'rb_name_merge')
        self.rb_path_merge = self.findChild(qtw.QRadioButton, 'rb_path_merge')
        self.rb_xml_merge = self.findChild(qtw.QRadioButton, 'rb_xml_merge')
        self.b_savelog_merge = self.findChild(
            qtw.QPushButton, 'b_savelog_merge')

        self.rb_ignore_merge = self.findChild(
            qtw.QRadioButton, 'rb_ignore_merge')
        self.rb_update_merge = self.findChild(
            qtw.QRadioButton, 'rb_update_merge')

        self.rb_useall_settings_merge = self.findChild(
            qtw.QRadioButton, 'rb_useall_settings_merge')
        self.rb_usecustom_settings_merge = self.findChild(
            qtw.QRadioButton, 'rb_usecustom_settings_merge')

        self.b_selectnone_settings_merge = self.findChild(
            qtw.QPushButton, 'b_selectnone_settings_merge')
        self.b_selectall_settings_merge = self.findChild(
            qtw.QPushButton, 'b_selectall_settings_merge')

        self.cb_name_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_name_settings_merge')
        self.cb_path_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_path_settings_merge')
        self.cb_image_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_image_settings_merge')
        self.cb_marquee_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_marquee_settings_merge')
        self.cb_video_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_video_settings_merge')
        self.cb_desc_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_desc_settings_merge')
        self.cb_developer_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_developer_settings_merge')
        self.cb_publisher_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_publisher_settings_merge')
        self.cb_releasedate_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_releasedate_settings_merge')
        self.cb_genre_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_genre_settings_merge')
        self.cb_players_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_players_settings_merge')
        self.cb_rating_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_rating_settings_merge')
        self.cb_lastplayed_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_lastplayed_settings_merge')
        self.cb_playcount_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_playcount_settings_merge')
        self.cb_sortname_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_sortname_settings_merge')
        self.cb_thumbnail_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_thumbnail_settings_merge')
        self.cb_favorite_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_favorite_settings_merge')
        self.cb_hidden_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_hidden_settings_merge')
        self.cb_kidgame_settings_merge = self.findChild(
            qtw.QCheckBox, 'cb_kidgame_settings_merge')

        # Button Widgets handler connection
        self.b_new_addgame.clicked.connect(self.b_new_addgame_clicked)
        self.b_import_addgame.clicked.connect(self.b_import_addgame_clicked)
        self.b_preview_addgame.clicked.connect(self.b_preview_addgame_clicked)
        self.b_save_addgame.clicked.connect(self.b_save_addgame_clicked)

        self.tb_original_merge.clicked.connect(self.tb_original_merge_clicked)
        self.tb_new_merge.clicked.connect(self.tb_new_merge_clicked)
        self.b_save_merge.clicked.connect(self.b_save_merge_clicked)
        self.b_savelog_merge.clicked.connect(self.b_savelog_merge_clicked)
        # Note: Following buttons share same handler.
        self.rb_name_merge.clicked.connect(self.rb_path_and_name_merge_clicked)
        self.rb_path_merge.clicked.connect(self.rb_path_and_name_merge_clicked)
        self.rb_xml_merge.clicked.connect(self.rb_path_and_name_merge_clicked)

        self.rb_ignore_merge.clicked.connect(self.rb_ignore_merge_clicked)
        self.rb_update_merge.clicked.connect(self.rb_update_merge_clicked)

        self.rb_useall_settings_merge.clicked.connect(
            self.rb_useall_settings_merge_clicked)
        self.rb_usecustom_settings_merge.clicked.connect(
            self.rb_usecustom_settings_merge_clicked)

        self.b_selectnone_settings_merge.clicked.connect(
            self.b_selectnone_settings_merge_clicked)
        self.b_selectall_settings_merge.clicked.connect(
            self.b_selectall_settings_merge_clicked)

        # Groups and Layouts
        self.gb_log_merge = self.findChild(qtw.QGroupBox, 'gb_log_merge')
        self.gb_custom_settings_merge = self.findChild(
            qtw.QGroupBox, 'gb_custom_settings_merge')

        # Style sheets defaults
        style = 'QPushButton{ background: azure; color: blue; }'
        self.style_save = style
        style = 'QPushButton{ background: honeydew; color: green; }'
        self.style_import = style
        style = 'QToolButton{ background: honeydew; color: green; }'
        self.style_toolimport = style
        style = 'QPushButton{ background: seashell; color: sandybrown; }'
        self.style_delete = style

        # Style sheets apply
        self.b_save_addgame.setStyleSheet(self.style_save)
        self.b_preview_addgame.setStyleSheet(self.style_save)
        self.b_save_merge.setStyleSheet(self.style_save)
        self.b_savelog_merge.setStyleSheet(self.style_save)

        self.b_preview_addgame.setStyleSheet(self.style_save)
        self.b_import_addgame.setStyleSheet(self.style_import)
        self.b_new_addgame.setStyleSheet(self.style_delete)
        self.tb_original_merge.setStyleSheet(self.style_toolimport)
        self.tb_new_merge.setStyleSheet(self.style_toolimport)

        self.b_selectnone_settings_merge.setStyleSheet(self.style_delete)
        self.b_selectall_settings_merge.setStyleSheet(self.style_delete)

        # Start by disabling the save buttons and defaults.
        # If any of the texts is empty, the button will get disabled.
        self.le_path_textChanged()
        self.le_original_merge_textChanged()
        self.le_new_merge_textChanged()
        self.rb_ignore_merge_clicked()
        self.update_log_text()
        self.statusbar.showMessage('Ready.')

        # Show Window
        self.setWindowTitle(f'{APP.NAME} v{APP.VERSION}')
        self.setWindowIcon(qtg.QIcon(':/Icons/img/winkemojis-wink.svg'))
        self.show()

    # Menu handlers

    def actionReadme_triggered(self):
        self.run_with_default_app(os.path.join(APP.DIR, 'README.html'))

    def actionAbout_triggered(self):
        about.show()

    def actionClose_triggered(self):
        self.close()

    # Widget handlers

    def rb_useall_settings_merge_clicked(self):
        self.gb_custom_settings_merge.setEnabled(False)

    def rb_usecustom_settings_merge_clicked(self):
        self.gb_custom_settings_merge.setEnabled(True)

    def rb_ignore_merge_clicked(self):
        self.rb_ignore_merge.setChecked(True)
        self.rb_update_merge.setChecked(False)
        self.tab_mode.setTabVisible(self.tabindex_settings_merge, False)

    def rb_update_merge_clicked(self):
        self.rb_ignore_merge.setChecked(False)
        self.rb_update_merge.setChecked(True)
        self.tab_mode.setTabVisible(self.tabindex_settings_merge, True)

    def le_path_textChanged(self):
        if self.le_path.text():
            self.b_save_addgame.setEnabled(True)
            self.b_save_addgame.setStyleSheet(self.style_save)
        else:
            self.b_save_addgame.setEnabled(False)
            self.b_save_addgame.setStyleSheet('')

    def le_new_merge_textChanged(self):
        norm = self.normalize_filepath(self.le_new_merge.text())
        if norm != self.le_new_merge.text():
            self.le_new_merge.setText(norm)
        if self.le_original_merge.text() and self.le_new_merge.text():
            self.b_save_merge.setEnabled(True)
            self.b_save_merge.setStyleSheet(self.style_save)
        else:
            self.b_save_merge.setEnabled(False)
            self.b_save_merge.setStyleSheet('')

    def le_original_merge_textChanged(self):
        norm = self.normalize_filepath(self.le_original_merge.text())
        if norm != self.le_original_merge.text():
            self.le_original_merge.setText(norm)
        if self.le_original_merge.text() and self.le_new_merge.text():
            self.b_save_merge.setEnabled(True)
            self.b_save_merge.setStyleSheet(self.style_save)
        else:
            self.b_save_merge.setEnabled(False)
            self.b_save_merge.setStyleSheet('')

    def rb_path_and_name_merge_clicked(self):
        self.update_log_text()

    def b_preview_addgame_clicked(self):
        """ Show preview of the game xml data message box. """
        self.msg_continue(self.get_xmlpreview(),
                          'Information', f'{APP.NAME} XML Preview')

    def b_new_addgame_clicked(self):
        """ Ask user if all gui input content should be cleared. """
        msg = 'Do you want start a new game entry from scratch?'
        if self.msg_continue(msg, 'Warning', f'{APP.NAME} Delete'):
            self.clear_all_input_fields()

    def b_import_addgame_clicked(self):
        """ Select a file and search for a matching game content.
        Fill all fields by the data from gamelist.xml file. """
        msg = 'Choose a gamelist.xml file to read an entry'
        file = self.dialog_choose_file(msg, '*.xml', mode='Load',
                                       wdir=self.last_import_file)
        if file:
            self.last_import_file = file
            self.fill_form_by_xml(file)

    def tb_original_merge_clicked(self):
        """ Select a file with original content to merge. """
        msg = 'Choose old base gamelist.xml file to compare to.'
        file = self.dialog_choose_file(msg, '*.xml', mode='Load',
                                       wdir=self.last_import_file)
        if file:
            self.last_import_file = file
            self.le_original_merge.setText(file)

    def tb_new_merge_clicked(self):
        """ Select a file with original content to append. """
        msg = 'Choose new gamelist.xml with additional data to append.'
        file = self.dialog_choose_file(msg, '*.xml', mode='Load',
                                       wdir=self.last_import_file)
        if file:
            self.last_import_file = file
            self.le_new_merge.setText(file)

    def b_selectnone_settings_merge_clicked(self):
        """ Deselect all tags in settings for merge update. """
        self.cb_name_settings_merge.setChecked(False)
        self.cb_path_settings_merge.setChecked(False)
        self.cb_image_settings_merge.setChecked(False)
        self.cb_marquee_settings_merge.setChecked(False)
        self.cb_video_settings_merge.setChecked(False)
        self.cb_desc_settings_merge.setChecked(False)
        self.cb_developer_settings_merge.setChecked(False)
        self.cb_publisher_settings_merge.setChecked(False)
        self.cb_releasedate_settings_merge.setChecked(False)
        self.cb_genre_settings_merge.setChecked(False)
        self.cb_players_settings_merge.setChecked(False)
        self.cb_rating_settings_merge.setChecked(False)
        self.cb_lastplayed_settings_merge.setChecked(False)
        self.cb_playcount_settings_merge.setChecked(False)
        self.cb_sortname_settings_merge.setChecked(False)
        self.cb_thumbnail_settings_merge.setChecked(False)
        self.cb_favorite_settings_merge.setChecked(False)
        self.cb_hidden_settings_merge.setChecked(False)
        self.cb_kidgame_settings_merge.setChecked(False)

    def b_selectall_settings_merge_clicked(self):
        """ Select all tags in settings for merge update. """
        self.cb_name_settings_merge.setChecked(True)
        self.cb_path_settings_merge.setChecked(True)
        self.cb_image_settings_merge.setChecked(True)
        self.cb_marquee_settings_merge.setChecked(True)
        self.cb_video_settings_merge.setChecked(True)
        self.cb_desc_settings_merge.setChecked(True)
        self.cb_developer_settings_merge.setChecked(True)
        self.cb_publisher_settings_merge.setChecked(True)
        self.cb_releasedate_settings_merge.setChecked(True)
        self.cb_genre_settings_merge.setChecked(True)
        self.cb_players_settings_merge.setChecked(True)
        self.cb_rating_settings_merge.setChecked(True)
        self.cb_lastplayed_settings_merge.setChecked(True)
        self.cb_playcount_settings_merge.setChecked(True)
        self.cb_sortname_settings_merge.setChecked(True)
        self.cb_thumbnail_settings_merge.setChecked(True)
        self.cb_favorite_settings_merge.setChecked(True)
        self.cb_hidden_settings_merge.setChecked(True)
        self.cb_kidgame_settings_merge.setChecked(True)

    def fill_form_by_xml(self, xml_file):
        """ Fill out form by selected XML file.

        Opens a XML file with a gameList structure and searches for a
        game to read.  The User entries in 'Add Game' view from the GUI
        are used as filters.  A game matching one of the filters is
        considered to be a match and will be read entirely to fill out
        its data to the GUI.

        Parameters
        ----------
        xml_file : str
            Path to a XML file in gamelist.xml format.
        """
        try:
            xml_root = ET.parse(xml_file).getroot()
        except ET.ParseError as error:
            xml_root = None
            msg = ('Error! Could not parse gamelist XML file '
                   f'{str(error.position)}:\n{xml_file}')
            self.msg_show_error(msg, 'Critical', 'Could not read file.')

        xml_game = None
        if xml_root:
            # Search XML content and get game content.  Use all tag names and
            # text from user input form as filters.
            filters = self.create_dict_from_gui()
            if not filters:
                filters = None
            xml_game, match = convert.get_game_byfilters(xml_root, filters)
            # Finally if game is found, get data and write to GUI edit fields.
            if xml_game:
                # match will be a dict if any user filter was active.  It will
                # contain the data which caused the match.  None if no filter
                # was active.
                # keys in match: 'name' and 'text'
                if match:
                    msg = ('Game data loaded by matching filter: '
                           f'{match["name"]}')
                else:
                    msg = 'First game data loaded. No filter active.'

                # Go through each tag in game element and write its content to
                # corresponding edit field in GUI.
                self.clear_all_input_fields()
                for tag in xml_game.iter():
                    try:
                        if tag.tag == "name":
                            self.le_name.setText(unescape(tag.text))
                        elif tag.tag == "path":
                            self.le_path.setText(unescape(tag.text))
                        elif tag.tag == "image":
                            self.le_image.setText(unescape(tag.text))
                        elif tag.tag == "marquee":
                            self.le_marquee.setText(unescape(tag.text))
                        elif tag.tag == "video":
                            self.le_video.setText(unescape(tag.text))
                        elif tag.tag == "desc":
                            self.pte_desc.setPlainText(unescape(tag.text))
                        elif tag.tag == "developer":
                            self.le_developer.setText(unescape(tag.text))
                        elif tag.tag == "publisher":
                            self.le_publisher.setText(unescape(tag.text))
                        elif tag.tag == "releasedate":
                            self.le_releasedate.setText(unescape(tag.text))
                        elif tag.tag == "genre":
                            self.le_genre.setText(unescape(tag.text))
                        elif tag.tag == "players":
                            self.le_players.setText(unescape(tag.text))
                        elif tag.tag == "rating":
                            self.le_rating.setText(unescape(tag.text))
                        elif tag.tag == "sortname":
                            self.le_sortname.setText(unescape(tag.text))
                        elif tag.tag == "thumbnail":
                            self.le_thumbnail.setText(unescape(tag.text))
                        elif tag.tag == "favorite":
                            if tag.text == 'true':
                                self.cb_favorite.setChecked(True)
                        elif tag.tag == "hidden":
                            if tag.text == 'true':
                                self.cb_hidden.setChecked(True)
                        elif tag.tag == "kidgame":
                            if tag.text == 'true':
                                self.cb_kidgame.setChecked(True)
                    except TypeError:
                        pass
            else:
                msg = 'No game. Filters do not match.'
        self.statusbar.showMessage(msg)

    def get_xmlpreview(self, max_len=80):
        """ Creates a XML representation of current GUI form.

        Convert current entry fields from gui to xml format as a
        string representation.  Trim too long entries for quick
        showcase, in example for use in a message box, before saving
        to file.

        Parameters
        ----------
        max_len : int
            Defines the maximum character length for each tag text.  If
            the text exceeds this limit, it will be truncated and the
            character '…' is added.
        """
        xml = self.create_dict_from_gui()
        for tag, value in xml.items():
            if len(value) > max_len:
                xml[tag] = value[:max_len] + '…'
        xml = convert.dict_to_element(xml, 'game', APP.SOURCE)
        xml = convert.element_to_tree(xml)
        xml = convert.tree_to_string(xml)
        return xml

    def b_save_addgame_clicked(self):
        """ Add game data from GUI form to selected XML file.

        Convert current entry fields from gui to xml format and add to
        a selected XML file.  Create a new file or overwrite an
        existing one.  In case of adding the data to an existing file,
        the function will search if the game already exist in the file.
        For this matter, it compares the basename of the path-tag from
        user form and the file.
        """
        # The current path of user input will be used as an identification to
        # find duplicate entry. It will compare basename only.
        current_path = self.le_path.text().strip()
        if current_path == '' or len(os.path.basename(current_path)) == 0:
            msg = 'Filename in path required to save an xml game entry.'
            self.msg_show_error(msg, 'Warning', 'No file.')
        else:
            msg = 'Save game data. Overwrite existing or create new file.'
            file = self.dialog_choose_file(msg, '*.xml', mode='Save',
                                           wdir=self.last_save_file)
            if file:
                # Add extension in case its missing and file does not exist.
                if (os.path.splitext(file)[1]
                        == '' and not os.path.exists(file)):
                    file = f'{file}.xml'
                # Remember last used file, so next time a file is selected the
                # last folder can be used as starting point.
                self.last_save_file = file

                # Overwrite existing file or create from scratch.
                if os.path.isfile(file) and os.path.exists(file):
                    # Overwrite existing file.

                    # The user xml data.
                    xml = self.create_dict_from_gui()
                    xml_element = convert.dict_to_element(xml, 'game',
                                                          APP.SOURCE)
                    xml_tree = convert.element_to_tree(xml_element)

                    # Load up xml file from disk.
                    try:
                        file_xml_root = ET.parse(file).getroot()
                    except ET.ParseError as error:

                        msg = ('Error! Could not parse gamelist XML file '
                               f'{str(error.position)}:\n{file}')
                        self.msg_show_error(msg, 'Critical',
                                            'Could not read file.')
                        file_xml_root = None

                    # Proceed only if file was read correctly.
                    if file_xml_root is not None:

                        # Search for basename of path in. If a duplicate was
                        # detected, return game entry, otherwise None.
                        xml_game = convert.get_game_bypath(
                            file_xml_root, current_path)

                        # Ask the user what to do if a game was found.
                        if xml_game is not None:
                            # Game entry found in xml file. Ask to what to do.
                            msg = ('Game entry collison! Game with same '
                                   'basename in path already exists in '
                                   'XML file.\n'
                                   'Basename from path:\n\n'
                                   f'"{os.path.basename(current_path)}"\n\n'
                                   'Do you want replace the entire game '
                                   'entry and overwrite file?')
                            removeGame = self.msg_continue(
                                msg, 'Question', f'{APP.NAME} Overwrite XML')
                            if removeGame:
                                file_xml_root.remove(xml_game)
                        # Append new game entry and write to file.  Any
                        # existing entry should be removed prior to this.
                        if xml_game is None or removeGame:
                            file_xml_root.append(xml_element)
                            xml_tree = ET.ElementTree()
                            convert.indent(file_xml_root)
                            xml_tree._setroot(file_xml_root)
                            try:
                                xml_tree.write(file, encoding='UTF-8',
                                               xml_declaration=None)
                                convert.prepend_filecontent(
                                    file, '<?xml version="1.0"?>\n')
                                self.statusbar.showMessage(
                                    f'File saved to: {file}')
                            except OSError:
                                msg = f'Error! Could not write file:\n{file}'
                                self.msg_show_error(
                                    msg, 'Critical', 'File not saved.')
                # Write file from scratch with single game content.
                else:
                    xml = self.create_dict_from_gui()
                    xml = convert.dict_to_element(xml, 'game', APP.SOURCE)
                    convert.indent(xml)
                    xml = convert.element_to_tree(xml)
                    try:
                        xml.write(file, encoding='UTF-8', xml_declaration=None)
                        convert.prepend_filecontent(file,
                                                    '<?xml version="1.0"?>\n')
                        self.statusbar.showMessage(f'File saved to: {file}')
                    except OSError:
                        msg = f'Error! Could not write to new file:\n{file}'
                        self.msg_show_error(msg, 'Warning', 'File not saved.')

    def b_save_merge_clicked(self):
        """ Merges two selected gamelist.xml files into new version.

        Takes two XML files in gamelist.xml format and merges them into
        one file.  All game entries missing in original file will be
        added to new file, based on the current settings.  After the
        process is done, a log with all added or updated games will be
        displayed in the log area.
        """
        original_file = self.le_original_merge.text()
        new_file = self.le_new_merge.text()
        if not os.path.exists(original_file):
            msg = ('File from input field do not exist. Original:'
                   f'\n{original_file}')
            self.msg_show_error(msg, 'Critical', 'File does not exist.')
        elif not os.path.exists(new_file):
            msg = f'File from input field do not exist. New:\n{new_file}'
            self.msg_show_error(msg, 'Critical', 'File does not exist.')
        elif os.path.samefile(original_file, new_file):
            msg = f'Both paths from input point to same file:\n{new_file}'
            self.msg_show_error(msg, 'Critical', 'Identical files.')
        else:
            try:
                e_file = original_file
                original_root = ET.parse(original_file).getroot()
                e_file = new_file
                new_root = ET.parse(new_file).getroot()
            except ET.ParseError as error:
                msg = ('Error! Could not parse gamelist XML file '
                       f'{str(error.position)}:\n{e_file}')
                self.msg_show_error(msg, 'Critical', 'Could not read file.')
            else:
                msg = 'Merge and save. Overwrite or create new file.'
                save_file = self.dialog_choose_file(
                    msg, '*.xml', mode='Save', wdir=self.last_save_file)
                if save_file:
                    # Add extension in case it is missing and the file does
                    # not exist.
                    if (os.path.splitext(save_file)[1]
                            == '' and not os.path.exists(save_file)):
                        save_file = save_file + '.xml'
                    self.last_save_file = save_file

                    updateonly = self.create_list_from_gui_updateonly()

                    # Create the new combined data by merging both files.
                    if self.rb_ignore_merge.isChecked():
                        duplicate_mode = 'i'
                    elif self.rb_update_merge.isChecked():
                        duplicate_mode = 'u'
                    else:
                        duplicate_mode = None

                    # Main merge process
                    self.diff_root = convert.merge_gamelists(
                        original_root, new_root, duplicate_mode, APP.SOURCE,
                        updateonly)
                    self.diff_paths, self.diff_names = (
                        convert.root_to_pathsnames(self.diff_root))

                    # Save process
                    save_tree = ET.ElementTree()
                    save_tree._setroot(original_root)
                    try:
                        save_tree.write(save_file, encoding='UTF-8',
                                        xml_declaration=None)
                        convert.prepend_filecontent(save_file,
                                                    '<?xml version="1.0"?>\n')
                        self.statusbar.showMessage(f'File saved: {save_file}')
                    except OSError:
                        msg = f'Error! Could not write XML file:\n{save_file}'
                        self.msg_show_error(msg, 'Critical', 'File not saved.')
                        self.gb_log_merge.setTitle('Log: ')
                    else:
                        self.update_log_text()
                        log_text = ''
                        # ignore duplicates
                        if duplicate_mode == 'i':
                            log_text = 'new added'
                        # update or replace duplicates
                        elif duplicate_mode == 'u' and updateonly is None:
                            log_text = 'merged'
                        elif duplicate_mode == 'u' and updateonly is not None:
                            log_text = 'updated tags'
                        # This should not happen.
                        else:
                            msg = ('Error! Wrong value for duplicate_mode: '
                                   f'{duplicate_mode}')
                            self.msg_show_error(msg, 'Critical',
                                                'Wrong value.')
                            msg = f'Wrong value for mode: {duplicate_mode}'
                            raise ValueError(msg)

                        len_original = str(len(original_root))
                        len_diff = str(len(self.diff_paths))
                        msg = (f'Log: {len_diff} {log_text} '
                               f'({len_original} total games)')
                        self.gb_log_merge.setTitle(msg)

    def b_savelog_merge_clicked(self):
        """ Save the log information from text view to file. """
        msg = 'Save current log as new or append to existing file.'
        save_file = self.dialog_choose_file(msg, '*.*', mode='Save',
                                            wdir=self.last_save_file)
        if save_file:
            self.last_save_file = save_file
            if self.rb_xml_merge.isChecked():
                save_tree = ET.ElementTree()
                save_tree._setroot(self.diff_root)
                try:
                    save_tree.write(save_file, encoding='UTF-8',
                                    xml_declaration=None)
                    convert.prepend_filecontent(save_file,
                                                '<?xml version="1.0"?>\n')
                    self.statusbar.showMessage(f'File saved to: {save_file}')
                except OSError:
                    msg = f'Error! Could not write to XML file:\n{save_file}'
                    self.msg_show_error(msg, 'Critical', 'File not saved.')
                    self.gb_log_merge.setTitle('Log: ')
            else:
                try:
                    with open(save_file, 'w') as s_file:
                        s_file.write(self.pte_log_merge.toPlainText())
                        self.statusbar.showMessage(f'File saved: {save_file}')
                except PermissionError:
                    msg = f'Error! No permission to save file:\n{save_file}'
                    self.msg_show_error(msg, 'Critical', 'File not saved.')
                except OSError:
                    msg = f'Error! Could not write to log file:\n{save_file}'
                    self.msg_show_error(msg, 'Critical', 'File not saved.')

    # Helper functions

    def create_dict_from_gui(self):
        """ Read 'Add Game' view form and create a dict out of it.

        Returns
        -------
        dict
            Keys are the tag names and their values are the tag text.
            Contains only those, which have a user text in the GUI.
        """
        dict_ = {}
        if not self.le_name.text() == '':
            dict_['name'] = escape(self.le_name.text().strip())
        if not self.le_path.text() == '':
            dict_['path'] = escape(self.le_path.text().strip())
        if not self.le_image.text() == '':
            dict_['image'] = escape(self.le_image.text().strip())
        if not self.le_marquee.text() == '':
            dict_['marquee'] = escape(self.le_marquee.text().strip())
        if not self.le_video.text() == '':
            dict_['video'] = escape(self.le_video.text().strip())
        if not self.pte_desc.toPlainText() == '':
            dict_['desc'] = escape(self.pte_desc.toPlainText().strip())
        if not self.le_developer.text() == '':
            dict_['developer'] = escape(self.le_developer.text().strip())
        if not self.le_publisher.text() == '':
            dict_['publisher'] = escape(self.le_publisher.text().strip())
        if not self.le_releasedate.text() == '':
            dict_['releasedate'] = escape(self.le_releasedate.text().strip())
        if not self.le_genre.text() == '':
            dict_['genre'] = escape(self.le_genre.text().strip())
        if not self.le_players.text() == '':
            dict_['players'] = escape(self.le_players.text().strip())
        if not self.le_rating.text() == '':
            dict_['rating'] = escape(self.le_rating.text().strip())
        if not self.le_sortname.text() == '':
            dict_['sortname'] = escape(self.le_sortname.text().strip())
        if not self.le_thumbnail.text() == '':
            dict_['thumbnail'] = escape(self.le_thumbnail.text().strip())
        if self.cb_favorite.isChecked():
            dict_['favorite'] = 'true'
        if self.cb_hidden.isChecked():
            dict_['hidden'] = 'true'
        if self.cb_kidgame.isChecked():
            dict_['kidgame'] = 'true'
        return dict_

    def create_list_from_gui_updateonly(self):
        """ List of all active tags in settings for merge update.

        Returns
        -------
        list or None
            Contains all tag names, which are currently active in the
            GUI at settings view for merge update.  None should be
            treated as 'all', which is a shortcut.
        """
        list_ = []
        if self.rb_useall_settings_merge.isChecked():
            list_ = None
        else:
            if self.cb_name_settings_merge.isChecked():
                list_.append('name')
            if self.cb_path_settings_merge.isChecked():
                list_.append('path')
            if self.cb_image_settings_merge.isChecked():
                list_.append('image')
            if self.cb_marquee_settings_merge.isChecked():
                list_.append('marquee')
            if self.cb_video_settings_merge.isChecked():
                list_.append('video')
            if self.cb_desc_settings_merge.isChecked():
                list_.append('desc')
            if self.cb_developer_settings_merge.isChecked():
                list_.append('developer')
            if self.cb_publisher_settings_merge.isChecked():
                list_.append('publisher')
            if self.cb_releasedate_settings_merge.isChecked():
                list_.append('releasedate')
            if self.cb_genre_settings_merge.isChecked():
                list_.append('genre')
            if self.cb_players_settings_merge.isChecked():
                list_.append('players')
            if self.cb_rating_settings_merge.isChecked():
                list_.append('rating')
            if self.cb_lastplayed_settings_merge.isChecked():
                list_.append('lastplayed')
            if self.cb_playcount_settings_merge.isChecked():
                list_.append('playcount')
            if self.cb_sortname_settings_merge.isChecked():
                list_.append('sortname')
            if self.cb_thumbnail_settings_merge.isChecked():
                list_.append('thumbnail')
            if self.cb_favorite_settings_merge.isChecked():
                list_.append('favorite')
            if self.cb_hidden_settings_merge.isChecked():
                list_.append('hidden')
            if self.cb_kidgame_settings_merge.isChecked():
                list_.append('kidgame')
            # If all tags are selected, then default to None. None should be
            # treated as all. Very important to changes the number when adding
            # new tags to Settings Merge Update.
            if len(list_) == 19:
                list_ = None
        return list_

    def clear_all_input_fields(self):
        """ Delete all data in the input fields of the GUI. """
        self.le_name.clear()
        self.le_path.clear()
        self.le_image.clear()
        self.le_marquee.clear()
        self.le_video.clear()
        self.pte_desc.clear()
        self.le_developer.clear()
        self.le_publisher.clear()
        self.le_releasedate.clear()
        self.le_genre.clear()
        self.le_players.clear()
        self.le_rating.clear()
        self.le_sortname.clear()
        self.le_thumbnail.clear()
        self.cb_favorite.setChecked(False)
        self.cb_hidden.setChecked(False)
        self.cb_kidgame.setChecked(False)

    def update_log_text(self):
        """ Update the log view with current selected display mode. """
        if self.rb_name_merge.isChecked():
            names = ''
            if self.diff_names:
                names = '\n'.join(self.diff_names)
            # Strangely if the last item is an empty string, it would be cut
            # off while converting with .join().  So just add the last new
            # line in this case.
            if self.diff_names and self.diff_names[-1] == '':
                names = names + '\n'
            self.pte_log_merge.setPlainText(names)
        elif self.rb_path_merge.isChecked():
            names = '\n'.join(self.diff_paths)
            if self.diff_paths and self.diff_paths[-1] == '':
                names = names + '\n'
            self.pte_log_merge.setPlainText(names)
        elif self.rb_xml_merge.isChecked():
            if self.diff_root is not None:
                xml = ET.tostring(self.diff_root, encoding='unicode')
                self.pte_log_merge.setPlainText(xml)
        if len(self.pte_log_merge.toPlainText()) > 0:
            self.b_savelog_merge.setEnabled(True)
            self.b_savelog_merge.setStyleSheet(self.style_save)
        else:
            self.b_savelog_merge.setEnabled(False)
            self.b_savelog_merge.setStyleSheet('')

    def run_with_default_app(self, file):
        """ Run the file with default associated app on the system.

        Parameters
        ----------
        file : str
            The file to run.
        """
        try:
            if os.path.exists(file):
                if sys.platform.startswith('linux'):
                    subprocess.call(["xdg-open", file])
                else:
                    os.startfile(file)  # pylint: disable=E1101
            else:
                msg = f'File not found:\n{file}'
                self.msg_show_error(msg, 'Warning')
        except Exception:
            msg = f'Could not run the file with default application:\n{file}'
            self.msg_show_error(msg, 'Warning')

    def normalize_filepath(self, file):
        """ Unquotes and normalizes drag and dropped paths.

        Converts paths with percent encoding and unquotes to actual
        real character representations, such as '%20' to ' ' (space).
        Also removes the 'file://' portion.  These happen especially
        when dealing with local files copied or drag and dropped.

        Parameters
        ----------
        file : str
            Regular file path as a string, expected from a drag and
            drop action.

        Returns
        -------
        str
            Cleaned up version of the file path.
        """
        file = file.replace('file://', '')
        file = urllib.parse.unquote(file)
        file = file.strip()
        return file

    # Dialog and message box related helper functions

    def msg_show_error(self, message, mode=None, short=None):
        """ Displays a standardized error message box.

        Not only shows it a message box to the user, it also prints to
        stdout and changes the statusbar.

        Parameters
        ----------
        message : str
            The main message to show in the message box.
        mode : None or {'Warning', 'Critical', 'Information'}
            Specifies the type of message box.  Defaults to None, which
            does not display specific icons.
        short : None or str
            Short version of the message for display in statusbar.
            If not specified, then the message is used as default.
        """
        if short is None:
            short = message
        msgBox = qtw.QMessageBox()
        if mode == 'Warning':
            msgBox.setIcon(qtw.QMessageBox.Warning)
        elif mode == 'Critical':
            msgBox.setIcon(qtw.QMessageBox.Critical)
        elif mode == 'Information':
            msgBox.setIcon(qtw.QMessageBox.Information)
        else:
            raise ValueError('Invalid value for "mode" in msg_show_error().')
        msgBox.setWindowTitle(APP.NAME)
        msgBox.setText(message)
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        self.statusbar.showMessage(short)
        print(message)
        msgBox.exec()

    def msg_continue(self, message, mode='Question', title=None):
        """ Standard message box asking to continue with process.

        A standard message asking to continue with process.  Depending
        on the options, an additional 'No' button and an icon are
        added.  Title defaults to APP.NAME.  If the user clicks the
        'Ok' (or 'Yes') button, then the function returns True,
        otherwiese False.

        Parameters
        ----------
        message : str
            The main message to show in the message box.
        title : None or str
            The title of the message box.  Defaults to None, which
            is treated as APP.NAME.
        mode : None or {'Warning', 'Critical', 'Information'}
            Specifies the type of message box.  Defaults to None, which
            does not display specific icons.  Depending on the mode,
            additional 'No' button can be added and a proper icon.

        Returns
        -------
        bool
            True if the user clicked 'ok' button, False otherwise.
        """
        msgBox = qtw.QMessageBox()
        # Ask to proceed. Default is ok.
        if mode == 'Question':
            msgBox.setIcon(qtw.QMessageBox.Question)
            msgBox.setStandardButtons(qtw.QMessageBox.No | qtw.QMessageBox.Ok)
            msgBox.setDefaultButton(qtw.QMessageBox.Ok)
            msgBox.setEscapeButton(qtw.QMessageBox.No)
        # No question, just show an information.
        elif mode == 'Information':
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.setDefaultButton(qtw.QMessageBox.Ok)
            msgBox.setEscapeButton(qtw.QMessageBox.Ok)
        # Important. Ask to proceed. Default is no.
        elif mode == 'Warning':
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setStandardButtons(qtw.QMessageBox.No | qtw.QMessageBox.Ok)
            msgBox.setDefaultButton(qtw.QMessageBox.No)
            msgBox.setEscapeButton(qtw.QMessageBox.No)
        # Like Information, but do not show any icon.
        elif mode is None:
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.setDefaultButton(qtw.QMessageBox.Ok)
            msgBox.setEscapeButton(qtw.QMessageBox.Ok)
        else:
            raise ValueError('Wrong value for "mode" in msg_continue().')

        if title is None:
            title = APP.NAME
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        return bool(msgBox.exec() == qtw.QMessageBox.Ok)

    def dialog_choose_file(self, title, filetype=None, mode=None, wdir=None):
        """ Show a standardized dialog for selecting files.

        Creates a dialog for choosing a file.  Will return the full
        path of selected file or an empty string if operation was
        cancelled.

        Parameters
        ----------
        title : str
            Title of the window as a short description.
        filetype : str
            Show only selected file types, in example '*.xml'.
        mode : None or {'Load', 'Save'}
            Sets the operational mode to save or load accept dialog.
            Only 'Load' and 'Save' are recognized.  Anything else
            defaults to load type, but only if 'Load' is set
            specifically, a file exist test will be done additionally.
        wdir : None or str
            Initial directory for opening the file.  None defaults to
            current working directory or used last folder.

        Returns
        -------
        str
            Full file path of selected file.  If user aborts selection,
            then an empty string is returned.
        """
        dialog = qtw.QFileDialog()
        dialog.setWindowTitle(title)
        if filetype is not None:
            dialog.setNameFilter(filetype)
        if wdir is None:
            if self.last_default_dir is None:
                wdir = os.getcwd()
            else:
                wdir = self.last_default_dir
        if os.path.isfile(wdir):
            wdir = os.path.dirname(wdir)
        self.last_default_dir = wdir
        dialog.setDirectory(wdir)
        dialog.setFileMode(qtw.QFileDialog.AnyFile)
        if mode == 'Save':
            dialog.setAcceptMode(qtw.QFileDialog.AcceptSave)
        dialog.setOptions((qtw.QFileDialog.DontUseNativeDialog
                          | qtw.QFileDialog.DontConfirmOverwrite))
        if dialog.exec_() == qtw.QDialog.Accepted:
            # Get the file string and add default extension if not present.
            file = str(dialog.selectedFiles()[0])
        else:
            file = ''
        if mode == 'Load':
            if not os.path.exists(file):
                file = ''
        return file


class About(qtw.QDialog):
    """ Creates the About dialog of the application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init
        self.ui = Ui_dialog_about()
        self.ui.setupUi(self)

        self.l_appname = self.findChild(qtw.QLabel, 'l_appname')
        self.l_appcreator = self.findChild(qtw.QLabel, 'l_appcreator')
        self.l_appversion = self.findChild(qtw.QLabel, 'l_appversion')
        self.l_appdesc = self.findChild(qtw.QLabel, 'l_appdesc')
        self.pte_appversion = self.findChild(
            qtw.QPlainTextEdit, 'pte_applicense')

        self.l_appname.setText(APP.NAME)
        self.l_appcreator.setText(APP.CREATOR)
        self.l_appversion.setText(APP.VERSION)
        self.l_appdesc.setText(APP.DESC)
        self.pte_appversion.setPlainText(APP.LICENSE.lstrip())


if __name__ == '__main__':
    APP = app.App(__file__)
    win = qtw.QApplication(sys.argv)
    mainwin = MainWin()
    about = About()
    sys.exit(win.exec_())
