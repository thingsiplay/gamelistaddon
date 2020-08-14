#!/usr/bin/python3

import os.path
import sys
import subprocess
import xml.etree.ElementTree as ET

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from html import escape, unescape

from gui.MainWindow import Ui_MainWindow
from gui.About import Ui_dialog_about
from gamelistxml import Convert
from constants import App


class MainWin(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Last saved data
        self.diff_names = []
        self.diff_paths = []
        self.diff_root = None

        # Variables for dublicate check of certain actions.
        # Used by the method
        self.last_le_releasedate_editingFinished_check = None
        self.last_save_file = None
        self.last_import_file = None
        self.last_default_dir = os.getcwd()

        # Menu and other essentials
        self.statusbar = self.findChild(qtw.QStatusBar, 'statusbar')
        self.menuHelp = self.findChild(qtw.QMenu, 'menuHelp')
        self.actionAbout = self.findChild(qtw.QAction, 'actionAbout')
        self.actionClose = self.findChild(qtw.QAction, 'actionClose')
        self.actionReadme = self.findChild(qtw.QAction, 'actionReadme')

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

        self.le_original_merge = self.findChild(qtw.QLineEdit, 'le_original_merge')
        self.le_new_merge = self.findChild(qtw.QLineEdit, 'le_new_merge')
        self.pte_log_merge = self.findChild(qtw.QPlainTextEdit, 'pte_log_merge')

        # Edit Widgets handler connection
        self.le_path.textChanged.connect(self.le_path_textChanged)

        self.le_original_merge.textChanged.connect(self.le_original_merge_textChanged)
        self.le_new_merge.textChanged.connect(self.le_new_merge_textChanged)

        # Edit Widgets validators
        reg_ex = qtc.QRegExp('[1-2]\d\d\d?([01]\d?([0-3]\d)?)?')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_releasedate)
        self.le_releasedate.setValidator(input_validator)

        reg_ex = qtc.QRegExp('[1-9]\d?')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_players)
        self.le_players.setValidator(input_validator)

        self.le_rating = self.findChild(qtw.QLineEdit, 'le_rating')
        reg_ex = qtc.QRegExp('(0\.\d\d|1\.00)')
        input_validator = qtg.QRegExpValidator(reg_ex, self.le_rating)
        self.le_rating.setValidator(input_validator)

        # Button Widgets
        self.b_new_addgame = self.findChild(qtw.QPushButton, 'b_new_addgame')
        self.b_import_addgame = self.findChild(qtw.QPushButton, 'b_import_addgame')
        self.b_preview_addgame = self.findChild(qtw.QPushButton, 'b_preview_addgame')
        self.b_save_addgame = self.findChild(qtw.QPushButton, 'b_save_addgame')

        self.tb_original_merge = self.findChild(qtw.QToolButton, 'tb_original_merge')
        self.tb_new_merge = self.findChild(qtw.QToolButton, 'tb_new_merge')
        self.b_save_merge = self.findChild(qtw.QPushButton, 'b_save_merge')
        self.rb_name_merge = self.findChild(qtw.QRadioButton, 'rb_name_merge')
        self.rb_path_merge = self.findChild(qtw.QRadioButton, 'rb_path_merge')
        self.rb_xml_merge = self.findChild(qtw.QRadioButton, 'rb_xml_merge')
        self.b_savelog_merge = self.findChild(qtw.QPushButton, 'b_savelog_merge')

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

        # Groups and Layouts
        self.gb_log_merge = self.findChild(qtw.QGroupBox, 'gb_log_merge')

        # Style sheets defaults
        self.style_save = 'QPushButton{ background: azure; color: blue; }'
        self.style_import = 'QPushButton{ background: honeydew; color: green; }'
        self.style_toolimport = 'QToolButton{ background: honeydew; color: green; }'
        self.style_delete = 'QPushButton{ background: seashell; color: sandybrown; }'

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

        # Start by disabling the save buttons. If any of the texts is empty, the button will get disabled.
        self.le_path_textChanged()
        self.le_original_merge_textChanged()
        self.le_new_merge_textChanged()
        self.update_log_text()
        self.statusbar.showMessage('Ready.')

        # Show Window
        self.setWindowTitle(APP.NAME + ' v' + APP.VERSION)
        self.setWindowIcon(qtg.QIcon(':/Icons/img/winkemojis-wink.svg'))
        self.show()

    # Menu handlers

    def actionReadme_triggered(self):
        self.run_with_default_app(os.path.join(APP.INSTALLDIR, 'README.html'))

    def actionAbout_triggered(self):
        about.show()

    def actionClose_triggered(self):
        self.close_application()

    # Widget handlers

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

    # Ask user if all gui input content should be cleared.
    def b_new_addgame_clicked(self):
        msgBox = qtw.QMessageBox()
        msgBox.setIcon(qtw.QMessageBox.Question)
        msgBox.setWindowTitle(APP.NAME + ' Delete')
        msgBox.setText("Do you want start over a new game entry from scratch?")
        msgBox.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == qtw.QMessageBox.Yes:
            self.clear_all_input_fields()

    # Select a file and search for a matching game content. Fill all fields by the data from gamelist.xml file.
    def b_import_addgame_clicked(self):
        file = self.dialog_choose_file('Choose a gamelist.xml file to read an entry',
                                       '*.xml', mode='Load', dir=self.last_import_file)
        if len(file) > 0:
            self.last_import_file = file
            self.fill_guiedits_by_xml(file)

    # Select a file with original gamelist.xml content for merge operation.
    def tb_original_merge_clicked(self):
        file = self.dialog_choose_file('Choose old base gamelist.xml file to compare to.', '*.xml',
                                       mode='Load', dir=self.last_import_file)
        if len(file) > 0:
            self.last_import_file = file
            self.le_original_merge.setText(file)

    # Select a file with new gamelist.xml content for merge operation.
    def tb_new_merge_clicked(self):
        file = self.dialog_choose_file('Choose new gamelist.xml file with additional data to append.',
                                       '*.xml', mode='Load', dir=self.last_import_file)
        if len(file) > 0:
            self.last_import_file = file
            self.le_new_merge.setText(file)

            # Actual function to parse gamelist.xml and search for matching content. Each input field with an active content
    # will be used to search game. Only one of the filters need to match for a match to be considered successfull. All
    # existing data in the GUIs edit fields will be wiped out and filled with found data.
    # Import button
    def fill_guiedits_by_xml(self, xml_file):
        active_filters = self.create_dict_from_gui()
        try:
            xml_root = ET.parse(xml_file).getroot()
        except ET.ParseError as error:
            xml_root = None
            self.showErrorMessage('Error! Could not parse gamelist XML file '
                                    + str(error.position) +  ':\n' + xml_file, 'Critical', 'Could not read file.')
        xml_gameFound = None
        if xml_root is not None:
            # Check if user made any input in the edit fields.
            if len(active_filters) > 0:
                # Each item is a full game Element with all its subelements.
                for game_element in xml_root.findall('game'):
                    # Each filter is the name of the edit field, which has a content on the gui, in example "path"
                    # or "name". Only one of the active filters need to match to get first found game.
                    for filter_name in active_filters:
                        # Check if game Element from XML file have a subelement with same of the filter, like "path"
                        # or "name".
                        if game_element.findtext(filter_name) is not None:
                            # Check if current active filters content, in example "0.65" or "Mario" matches the
                            # content from corresponding tag content in XML file.
                            if active_filters[filter_name] in unescape(game_element.findtext(filter_name)):
                                # Single filter match is enough. Consider game found and break out through all loops.
                                xml_gameFound = game_element
                                self.statusbar.showMessage('Game data loaded by matching filter: ' + filter_name)
                                break
                        # End of "for filter_name"
                        if xml_gameFound:
                            break
                    # Emd of "for game_element"
                    if xml_gameFound:
                        break
                    # The following out commented lines with "#~" is the same algorithm as above, but all active
                    # filters must match on a game.
                    '''
                    #~number_of_filters = len(active_filters)
                    #~matches = 0
                    #~for filter_name in active_filters:
                        #~if game_element.findtext(filter_name) is not None and active_filters[filter_name] in unescape(game_element.findtext(filter_name)):
                            #~matches = matches + 1
                        #~else:
                            #~matches = 0
                            #~break
                    #~if matches >= number_of_filters:
                        #~xml_gameFound = game_element
                        #~break
                    '''
            # End of "if len(active_filters)". No filter set in gui. Get first found entry from xml.
            else:
                xml_gameFound = xml_root.find('game')
                self.statusbar.showMessage('First game data loaded. No filter active.')
            # Finally if game is found, get its data and write to GUI edit fields.
            if xml_gameFound is not None:
                self.clear_all_input_fields()
                # Go through each tag in the game element and write its text to the corresponding user edit fields,
                # in example content of "name".
                for tag in xml_gameFound.iter():
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
                    except TypeError:
                        pass
            else:
                self.statusbar.showMessage('No game loaded. Filters do not match.')

    # Show a quick preview of the game xml data in a Message Box. This is what would be written to the file if save
    # button was used.
    def b_preview_addgame_clicked(self):
        xml = self.create_dict_from_gui()
        if 'desc' in xml and len(xml['desc']) > 80:
            xml['desc'] = xml['desc'][:80] + '…'
        xml = Convert.dict2xmlGameElement(xml, APP.SOURCE)
        xml = Convert.xmlElement2xmlTree(xml)
        xml = Convert.xmlTree2rootString(xml)

        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle(APP.NAME + ' XML Preview')
        msgBox.setText(xml)
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        msgBox.exec()

    # Add the game data to selected XML file. Create a new file or overwrite an existing one. If the game content
    # already exists, then ask the user what to do. The check is done by comparing the basename without directory part
    # in "path". Unless there is no basename, then the strings will be used as it is.
    def b_save_addgame_clicked(self):
        # The current path of user input will be used as an identification to find dublicate entry. It will compare
        # basename only.
        current_path = self.le_path.text().strip()
        if current_path == '' or len(os.path.basename(current_path)) == 0:
            self.showErrorMessage('No filename in path. Filename required to save an xml game entry.', 'Warning', 'No file.')
        else:
            file = self.dialog_choose_file('Save game data. Overwrite existing or create new file.',
                                           '*.xml', mode='Save', dir=self.last_save_file)
            if len(file) > 0:
                # Add extension in case it is missing and the file does not exist.
                if os.path.splitext(file)[1] == '' and not os.path.exists(file):
                    file = file + '.xml'

                self.last_save_file = file

                # Overwrite existing file or create from scratch.
                if os.path.isfile(file) and os.path.exists(file):
                    # Overwrite existing file.

                    # The user xml data.
                    xml = self.create_dict_from_gui()
                    xml_element = Convert.dict2xmlGameElement(xml, APP.SOURCE)
                    xml_tree = Convert.xmlElement2xmlTree(xml_element)

                    # Load up xml file from disk.
                    try:
                        file_xml_root = ET.parse(file).getroot()
                    except ET.ParseError as error:
                        self.showErrorMessage('Error! Could not parse gamelist XML file '
                                                + str(error.position) + ':\n' + file, 'Critical', 'Could not read file.')
                        file_xml_root = None

                    # Proceed only if file was read correctly.
                    if file_xml_root is not None:
                        # Now let's compare the basename of user input in path against all basename in path from
                        # xml file on disk. If any duplicate is found, then stop searching.
                        dupeCheck = os.path.basename(current_path)
                        xml_gameFound = None
                        for item in file_xml_root.getiterator('game'):
                            itemPath = item.find('path')
                            if itemPath is None:
                                itemPath = ''
                            else:
                                itemPath = itemPath.text
                            if dupeCheck == os.path.basename(itemPath):
                                # Capture the item in its entirety, so it can be used to remove it later.
                                xml_gameFound = item
                                break
                        # Ask the user what to do if a game with same basename was found.
                        if xml_gameFound is not None:
                            # Game entry found in xml file. Ask to overwrite entry or abort.
                            msgBox = qtw.QMessageBox()
                            msgBox.setIcon(qtw.QMessageBox.Question)
                            msgBox.setWindowTitle(APP.NAME + ' Overwrite XML')
                            msgBox.setText('Game entry collison! Game with same basename in path already exists in XML file.\n'
                                           + 'Basename from path:\n\n"' + dupeCheck + '"\n\n'
                                           + 'Do you want replace the entire game entry and overwrite file?')
                            msgBox.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No)

                            returnValue = msgBox.exec()
                            if returnValue == qtw.QMessageBox.Yes:
                                # Now remove the dublicate game tag element.
                                file_xml_root.remove(xml_gameFound)
                        # Append new game entry and write to file. Any existing entry should be removed prior to this.
                        if xml_gameFound is None or returnValue == qtw.QMessageBox.Yes:
                            file_xml_root.append(xml_element)
                            xml_tree = ET.ElementTree()
                            Convert.indent(file_xml_root)
                            xml_tree._setroot(file_xml_root)
                            try:
                                xml_tree.write(file, encoding="UTF-8", xml_declaration=None)
                                Convert.prepend_filecontent(file, "<?xml version=\"1.0\"?>\n")
                                self.statusbar.showMessage('File saved to: ' + file)
                            except OSError:
                                self.showErrorMessage('Error! Could not write to file: \n' + file, 'Critical', 'File not saved.')
                # Write file from scratch with single game content.
                else:
                    xml = self.create_dict_from_gui()
                    xml = Convert.dict2xmlGameElement(xml, APP.SOURCE)
                    Convert.indent(xml)
                    xml = Convert.xmlElement2xmlTree(xml)
                    try:
                        xml.write(file, encoding="UTF-8", xml_declaration=None)
                        Convert.prepend_filecontent(file, "<?xml version=\"1.0\"?>\n")
                        self.statusbar.showMessage('File saved to: ' + file)
                    except OSError:
                        self.showErrorMessage('Error! Could not write to new file:\n' + file, 'Warning', 'File not saved.')


    # Takes two xml files and merges them into one file. All game entries missing in original file will be added from
    # new file. Existing entries are not touched. To determine if a game exists, the path of it will be used as an
    # identifier.
    # The user is asked to select two files and then an output file. After the process is done, a log with all added
    # games will be displayed in the log area.
    def b_save_merge_clicked(self):
        original_file = self.le_original_merge.text()
        new_file = self.le_new_merge.text()
        if not os.path.exists(original_file) :
            self.showErrorMessage('File from input field do not exist. Original:\n' + original_file,
                                  'Critical', 'File does not exist.')
        elif not os.path.exists(new_file):
            self.showErrorMessage('File from input field do not exist. New:\n' + new_file,
                                  'Critical', 'File does not exist.')
        elif os.path.samefile(original_file, new_file):
            self.showErrorMessage('Both paths from input point to same file.' + new_file,
                                  'Critical', 'Identical files.')
        else:
            try:
                e = original_file
                original_root = ET.parse(original_file).getroot()
                e = new_file
                new_root = ET.parse(new_file).getroot()
            except ET.ParseError as error:
                self.showErrorMessage('Error! Could not parse gamelist XML file '
                                      + str(error.position) + ':\n' + e, 'Critical', 'Could not read file.')
            else:
                save_file = self.dialog_choose_file('Merge and save. Overwrite existing or create new file.',
                                                    '*.xml', mode='Save', dir=self.last_save_file)
                if len(save_file) > 0:
                    # Add extension in case it is missing and the file does not exist.
                    if os.path.splitext(save_file)[1] == '' and not os.path.exists(save_file):
                        save_file = save_file + '.xml'

                    self.last_save_file = save_file

                    # Create the new combined data by merging both files.
                    save_root, self.diff_root, self.diff_paths, self.diff_names = Convert.mergeGamelists(original_root, new_root)

                    save_tree = ET.ElementTree()
                    save_tree._setroot(save_root)
                    try:
                        save_tree.write(save_file, encoding="UTF-8", xml_declaration=None)
                        Convert.prepend_filecontent(save_file, "<?xml version=\"1.0\"?>\n")
                        self.statusbar.showMessage('File saved to: ' + save_file)
                    except OSError:
                        self.showErrorMessage('Error! Could not write to XML file: \n' + save_file, 'Critical', 'File not saved.')
                        self.gb_log_merge.setTitle('Log: ')
                    else:
                        self.update_log_text()
                        self.gb_log_merge.setTitle( 'Log: ' + str(len(self.diff_paths)) + ' added' )

    # Saves the current log information from text view to a file.
    def b_savelog_merge_clicked(self):
        save_file = self.dialog_choose_file('Save current log as new or append to existing file.',
                                            '*.*', mode='Save', dir=self.last_save_file)
        if len(save_file) > 0:
            self.last_save_file = save_file
            if self.rb_xml_merge.isChecked():
                save_tree = ET.ElementTree()
                save_tree._setroot(self.diff_root)
                try:
                    save_tree.write(save_file, encoding="UTF-8", xml_declaration=None)
                    Convert.prepend_filecontent(save_file, "<?xml version=\"1.0\"?>\n")
                    self.statusbar.showMessage('File saved to: ' + save_file)
                except OSError:
                    self.showErrorMessage('Error! Could not write to XML file: \n' + save_file, 'Critical', 'File not saved.')
                    self.gb_log_merge.setTitle('Log: ')
            else:
                try:
                    with open(save_file, 'w') as f:
                        f.write(self.pte_log_merge.toPlainText())
                        self.statusbar.showMessage('File saved to: ' + save_file)
                except PermissionError:
                    self.showErrorMessage('Error! No permission to save file:\n' + save_file, 'Critical', 'File not saved.')
                except OSError:
                    self.showErrorMessage('Error! Could not write to log file:\n' + save_file, 'Critical', 'File not saved.')

    # Helper functions

    # Just a shorthand to show an error message box and print to terminal.
    def showErrorMessage(self, message, type=None, short=None):
        if short is None:
            short = message
        self.statusbar.showMessage(message)
        print(message)
        msgBox = qtw.QMessageBox()
        if type == 'Warning':
            msgBox.setIcon(qtw.QMessageBox.Warning)
        elif type == 'Critical':
            msgBox.setIcon(qtw.QMessageBox.Critical)
        elif type == 'Information':
            msgBox.setIcon(qtw.QMessageBox.Information)
        msgBox.setWindowTitle(APP.NAME)
        msgBox.setText(message)
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        msgBox.exec()

    # Show a standardized dialog for loading or saving files. Returns full path of file or an empty string if cancelled.
    # In case of mode='load', the file will be checked if its exists. In case of mode='save', button is named 'save'
    # accordingly.
    def dialog_choose_file(self, title, filter=None, mode=None, dir=None):
        dialog = qtw.QFileDialog()
        dialog.setWindowTitle(title)
        if filter is not None:
            dialog.setNameFilter(filter)
        if dir is None:
            if self.last_default_dir is None:
                dir = os.getcwd()
            else:
                dir = self.last_default_dir
        if os.path.isfile(dir):
            dir = os.path.dirname(dir)
        self.last_default_dir = dir
        dialog.setDirectory(dir)
        dialog.setFileMode(qtw.QFileDialog.AnyFile)
        if mode == 1 or mode == 'Save':
            dialog.setAcceptMode(qtw.QFileDialog.AcceptSave)
        dialog.setOptions(qtw.QFileDialog.DontUseNativeDialog | qtw.QFileDialog.DontConfirmOverwrite)
        if dialog.exec_() == qtw.QDialog.Accepted:
            # Get the file string and add default extension if not present.
            file = str(dialog.selectedFiles()[0])
        else:
            file = ''
        if mode == 0 or mode == 'Load':
            if not os.path.exists(file):
                file = ''
        return file

    # Read all non empty user text fields and create a Python dictionary out of it.
    def create_dict_from_gui(self):
        d = {}
        if not self.le_name.text() == '':
            d['name'] = escape( self.le_name.text().strip() )
        if not self.le_path.text() == '':
            d['path'] = escape( self.le_path.text().strip() )
        if not self.le_image.text() == '':
            d['image'] = escape( self.le_image.text().strip() )
        if not self.le_marquee.text() == '':
            d['marquee'] = escape( self.le_marquee.text().strip() )
        if not self.le_video.text() == '':
            d['video'] = escape( self.le_video.text().strip() )
        if not self.pte_desc.toPlainText() == '':
            d['desc'] = escape( self.pte_desc.toPlainText().strip() )
        if not self.le_developer.text() == '':
            d['developer'] = escape( self.le_developer.text().strip() )
        if not self.le_publisher.text() == '':
            d['publisher'] = escape( self.le_publisher.text().strip() )
        if not self.le_releasedate.text() == '':
            d['releasedate'] = escape( self.le_releasedate.text().strip() )
        if not self.le_genre.text() == '':
            d['genre'] = escape( self.le_genre.text().strip() )
        if not self.le_players.text() == '':
            d['players'] = escape( self.le_players.text().strip() )
        if not self.le_rating.text() == '':
            d['rating'] = escape( self.le_rating.text().strip() )
        return d

    # Delete all data in the input fields of the GUI.
    def clear_all_input_fields(self):
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

    # Update the current log view in ui with the current selected display mode.
    def update_log_text(self):
        if self.rb_name_merge.isChecked():
            list = '\n'.join(self.diff_names)
            # Strangely if the last item is an empty string, it would be cut off while converting with .join(). So
            # just add the last new line in this case.
            if len(self.diff_names) > 0 and self.diff_names[-1] == '':
                list = list + '\n'
            self.pte_log_merge.setPlainText(list)
        elif self.rb_path_merge.isChecked():
            list = '\n'.join(self.diff_paths)
            if len(self.diff_paths) > 0 and self.diff_paths[-1] == '':
                list = list + '\n'
            self.pte_log_merge.setPlainText(list)
        elif self.rb_xml_merge.isChecked():
            if self.diff_root is not None:
                xml = ET.tostring(self.diff_root, encoding="unicode")
                self.pte_log_merge.setPlainText(xml)
        if len(self.pte_log_merge.toPlainText()) > 0:
            self.b_savelog_merge.setEnabled(True)
            self.b_savelog_merge.setStyleSheet(self.style_save)
        else:
            self.b_savelog_merge.setEnabled(False)
            self.b_savelog_merge.setStyleSheet('')

    # Open or run the file with default associated application on the system.
    def run_with_default_app(self, file):
        try:
            if os.path.exists(file):
                if sys.platform.startswith('linux'):
                    subprocess.call(["xdg-open", file])
                else:
                    os.startfile(file)
            else:
                self.showErrorMessage('Readme file not found:\n' + file, 'Warning')
        except:
            self.showErrorMessage('Could not run the file with default application:\n' + file, 'Warning')

    # This is just in case the user drag and drops the file, so the file:// format is supported.
    def normalize_filepath(self, file):
        file = file.replace('file://', '')
        file = file.replace('%20', ' ')
        file = file.lstrip()
        file = file.rstrip()
        return file

    # Ask the user to end.
    def close_application(self):
        message = 'Do you want close the application? Any non saved data will be lost.'

        msgBox = qtw.QMessageBox()
        msgBox.setIcon(qtw.QMessageBox.Warning)
        msgBox.setWindowTitle(APP.NAME)
        msgBox.setText(message)
        msgBox.setStandardButtons(qtw.QMessageBox.No|qtw.QMessageBox.Ok)
        msgBox.setDefaultButton(qtw.QMessageBox.No)
        msgBox.setEscapeButton(qtw.QMessageBox.No)

        if msgBox.exec() == qtw.QMessageBox.Ok:
            self.close()

class About(qtw.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init
        self.ui = Ui_dialog_about()
        self.ui.setupUi(self)

        self.l_appname = self.findChild(qtw.QLabel, 'l_appname')
        self.l_appcreator = self.findChild(qtw.QLabel, 'l_appcreator')
        self.l_appversion = self.findChild(qtw.QLabel, 'l_appversion')
        self.l_appdesc = self.findChild(qtw.QLabel, 'l_appdesc')
        self.pte_appversion = self.findChild(qtw.QPlainTextEdit, 'pte_applicense')

        self.l_appname.setText(APP.NAME)
        self.l_appcreator.setText(APP.CREATOR)
        self.l_appversion.setText(APP.VERSION)
        self.l_appdesc.setText(APP.DESC)
        self.pte_appversion.setPlainText(APP.LICENSE.lstrip())


if __name__ == '__main__':
    APP = App.App(__file__)
    win = qtw.QApplication(sys.argv)
    mainwin = MainWin()
    about = About()
    sys.exit(win.exec_())