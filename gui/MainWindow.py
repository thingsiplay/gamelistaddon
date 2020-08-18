# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 956)
        MainWindow.setMinimumSize(QtCore.QSize(640, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tab_mode = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_mode.setObjectName("tab_mode")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setContentsMargins(16, 16, 16, 16)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem, 7, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem1, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(16)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.b_new_addgame = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_new_addgame.sizePolicy().hasHeightForWidth())
        self.b_new_addgame.setSizePolicy(sizePolicy)
        self.b_new_addgame.setMinimumSize(QtCore.QSize(160, 45))
        self.b_new_addgame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/img/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_new_addgame.setIcon(icon)
        self.b_new_addgame.setIconSize(QtCore.QSize(24, 24))
        self.b_new_addgame.setObjectName("b_new_addgame")
        self.horizontalLayout_2.addWidget(self.b_new_addgame)
        self.b_import_addgame = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_import_addgame.sizePolicy().hasHeightForWidth())
        self.b_import_addgame.setSizePolicy(sizePolicy)
        self.b_import_addgame.setMinimumSize(QtCore.QSize(160, 45))
        self.b_import_addgame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/img/import.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_import_addgame.setIcon(icon1)
        self.b_import_addgame.setIconSize(QtCore.QSize(24, 24))
        self.b_import_addgame.setObjectName("b_import_addgame")
        self.horizontalLayout_2.addWidget(self.b_import_addgame)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.b_preview_addgame = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_preview_addgame.sizePolicy().hasHeightForWidth())
        self.b_preview_addgame.setSizePolicy(sizePolicy)
        self.b_preview_addgame.setMinimumSize(QtCore.QSize(160, 45))
        self.b_preview_addgame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/img/preview.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_preview_addgame.setIcon(icon2)
        self.b_preview_addgame.setIconSize(QtCore.QSize(24, 24))
        self.b_preview_addgame.setObjectName("b_preview_addgame")
        self.horizontalLayout_2.addWidget(self.b_preview_addgame)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 13, 0, 1, 1)
        self.l_pagetitle_addgame = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setItalic(True)
        self.l_pagetitle_addgame.setFont(font)
        self.l_pagetitle_addgame.setAlignment(QtCore.Qt.AlignCenter)
        self.l_pagetitle_addgame.setObjectName("l_pagetitle_addgame")
        self.gridLayout_3.addWidget(self.l_pagetitle_addgame, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.l_name = QtWidgets.QLabel(self.tab)
        self.l_name.setObjectName("l_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.l_name)
        self.le_name = QtWidgets.QLineEdit(self.tab)
        self.le_name.setClearButtonEnabled(True)
        self.le_name.setObjectName("le_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_name)
        self.l_path = QtWidgets.QLabel(self.tab)
        self.l_path.setObjectName("l_path")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.l_path)
        self.le_path = QtWidgets.QLineEdit(self.tab)
        self.le_path.setClearButtonEnabled(True)
        self.le_path.setObjectName("le_path")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.le_path)
        self.l_image = QtWidgets.QLabel(self.tab)
        self.l_image.setObjectName("l_image")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.l_image)
        self.le_image = QtWidgets.QLineEdit(self.tab)
        self.le_image.setClearButtonEnabled(True)
        self.le_image.setObjectName("le_image")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.le_image)
        self.l_marquee = QtWidgets.QLabel(self.tab)
        self.l_marquee.setObjectName("l_marquee")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.l_marquee)
        self.le_marquee = QtWidgets.QLineEdit(self.tab)
        self.le_marquee.setClearButtonEnabled(True)
        self.le_marquee.setObjectName("le_marquee")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.le_marquee)
        self.l_video = QtWidgets.QLabel(self.tab)
        self.l_video.setObjectName("l_video")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.l_video)
        self.le_video = QtWidgets.QLineEdit(self.tab)
        self.le_video.setClearButtonEnabled(True)
        self.le_video.setObjectName("le_video")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.le_video)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.formLayout.setItem(7, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.l_desc = QtWidgets.QLabel(self.tab)
        self.l_desc.setObjectName("l_desc")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.l_desc)
        self.pte_desc = QtWidgets.QPlainTextEdit(self.tab)
        self.pte_desc.setObjectName("pte_desc")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.pte_desc)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.formLayout.setItem(9, QtWidgets.QFormLayout.LabelRole, spacerItem4)
        self.l_developer = QtWidgets.QLabel(self.tab)
        self.l_developer.setObjectName("l_developer")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.l_developer)
        self.le_developer = QtWidgets.QLineEdit(self.tab)
        self.le_developer.setClearButtonEnabled(True)
        self.le_developer.setObjectName("le_developer")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.le_developer)
        self.l_publisher = QtWidgets.QLabel(self.tab)
        self.l_publisher.setObjectName("l_publisher")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.l_publisher)
        self.le_publisher = QtWidgets.QLineEdit(self.tab)
        self.le_publisher.setClearButtonEnabled(True)
        self.le_publisher.setObjectName("le_publisher")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.le_publisher)
        self.l_releasedate = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_releasedate.sizePolicy().hasHeightForWidth())
        self.l_releasedate.setSizePolicy(sizePolicy)
        self.l_releasedate.setMinimumSize(QtCore.QSize(120, 0))
        self.l_releasedate.setMaximumSize(QtCore.QSize(120, 16777215))
        self.l_releasedate.setBaseSize(QtCore.QSize(120, 0))
        self.l_releasedate.setObjectName("l_releasedate")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.l_releasedate)
        self.le_releasedate = QtWidgets.QLineEdit(self.tab)
        self.le_releasedate.setPlaceholderText("")
        self.le_releasedate.setClearButtonEnabled(True)
        self.le_releasedate.setObjectName("le_releasedate")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.le_releasedate)
        self.l_genre = QtWidgets.QLabel(self.tab)
        self.l_genre.setObjectName("l_genre")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.l_genre)
        self.le_genre = QtWidgets.QLineEdit(self.tab)
        self.le_genre.setClearButtonEnabled(True)
        self.le_genre.setObjectName("le_genre")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.le_genre)
        self.l_players = QtWidgets.QLabel(self.tab)
        self.l_players.setObjectName("l_players")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.l_players)
        self.le_players = QtWidgets.QLineEdit(self.tab)
        self.le_players.setClearButtonEnabled(True)
        self.le_players.setObjectName("le_players")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.le_players)
        self.l_rating = QtWidgets.QLabel(self.tab)
        self.l_rating.setObjectName("l_rating")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.l_rating)
        self.le_rating = QtWidgets.QLineEdit(self.tab)
        self.le_rating.setPlaceholderText("")
        self.le_rating.setClearButtonEnabled(True)
        self.le_rating.setObjectName("le_rating")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.le_rating)
        self.gridLayout_3.addLayout(self.formLayout, 5, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem5, 6, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem6, 14, 0, 1, 1)
        self.b_save_addgame = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_save_addgame.sizePolicy().hasHeightForWidth())
        self.b_save_addgame.setSizePolicy(sizePolicy)
        self.b_save_addgame.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_save_addgame.setFont(font)
        self.b_save_addgame.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.b_save_addgame.setFocusPolicy(QtCore.Qt.WheelFocus)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/img/saveas.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_addgame.setIcon(icon3)
        self.b_save_addgame.setIconSize(QtCore.QSize(32, 32))
        self.b_save_addgame.setObjectName("b_save_addgame")
        self.gridLayout_3.addWidget(self.b_save_addgame, 15, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem7, 3, 0, 1, 1)
        self.tab_mode.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setContentsMargins(16, 16, 16, 16)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.b_save_merge = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_save_merge.sizePolicy().hasHeightForWidth())
        self.b_save_merge.setSizePolicy(sizePolicy)
        self.b_save_merge.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.b_save_merge.setFont(font)
        self.b_save_merge.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.b_save_merge.setIcon(icon3)
        self.b_save_merge.setIconSize(QtCore.QSize(32, 32))
        self.b_save_merge.setObjectName("b_save_merge")
        self.gridLayout_5.addWidget(self.b_save_merge, 8, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setHorizontalSpacing(16)
        self.formLayout_2.setVerticalSpacing(19)
        self.formLayout_2.setObjectName("formLayout_2")
        self.le_original_merge = QtWidgets.QLineEdit(self.tab_2)
        self.le_original_merge.setClearButtonEnabled(True)
        self.le_original_merge.setObjectName("le_original_merge")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.le_original_merge)
        self.l_new_merge = QtWidgets.QLabel(self.tab_2)
        self.l_new_merge.setObjectName("l_new_merge")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.l_new_merge)
        self.tb_new_merge = QtWidgets.QToolButton(self.tab_2)
        self.tb_new_merge.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tb_new_merge.setObjectName("tb_new_merge")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tb_new_merge)
        self.le_new_merge = QtWidgets.QLineEdit(self.tab_2)
        self.le_new_merge.setClearButtonEnabled(True)
        self.le_new_merge.setObjectName("le_new_merge")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.le_new_merge)
        self.tb_original_merge = QtWidgets.QToolButton(self.tab_2)
        self.tb_original_merge.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tb_original_merge.setObjectName("tb_original_merge")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tb_original_merge)
        self.l_original_merge = QtWidgets.QLabel(self.tab_2)
        self.l_original_merge.setObjectName("l_original_merge")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.l_original_merge)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.rb_ignore_merge = QtWidgets.QRadioButton(self.tab_2)
        self.rb_ignore_merge.setCheckable(True)
        self.rb_ignore_merge.setChecked(True)
        self.rb_ignore_merge.setObjectName("rb_ignore_merge")
        self.horizontalLayout.addWidget(self.rb_ignore_merge)
        self.rb_update_merge = QtWidgets.QRadioButton(self.tab_2)
        self.rb_update_merge.setCheckable(True)
        self.rb_update_merge.setObjectName("rb_update_merge")
        self.horizontalLayout.addWidget(self.rb_update_merge)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem9 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem9)
        self.gb_log_merge = QtWidgets.QGroupBox(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gb_log_merge.sizePolicy().hasHeightForWidth())
        self.gb_log_merge.setSizePolicy(sizePolicy)
        self.gb_log_merge.setObjectName("gb_log_merge")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_log_merge)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pte_log_merge = QtWidgets.QPlainTextEdit(self.gb_log_merge)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.pte_log_merge.setFont(font)
        self.pte_log_merge.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.pte_log_merge.setReadOnly(True)
        self.pte_log_merge.setObjectName("pte_log_merge")
        self.gridLayout_2.addWidget(self.pte_log_merge, 6, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.rb_xml_merge = QtWidgets.QRadioButton(self.gb_log_merge)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_xml_merge.sizePolicy().hasHeightForWidth())
        self.rb_xml_merge.setSizePolicy(sizePolicy)
        self.rb_xml_merge.setObjectName("rb_xml_merge")
        self.gridLayout_4.addWidget(self.rb_xml_merge, 0, 2, 1, 1)
        self.rb_name_merge = QtWidgets.QRadioButton(self.gb_log_merge)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_name_merge.sizePolicy().hasHeightForWidth())
        self.rb_name_merge.setSizePolicy(sizePolicy)
        self.rb_name_merge.setChecked(True)
        self.rb_name_merge.setObjectName("rb_name_merge")
        self.gridLayout_4.addWidget(self.rb_name_merge, 0, 0, 1, 1)
        self.rb_path_merge = QtWidgets.QRadioButton(self.gb_log_merge)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_path_merge.sizePolicy().hasHeightForWidth())
        self.rb_path_merge.setSizePolicy(sizePolicy)
        self.rb_path_merge.setObjectName("rb_path_merge")
        self.gridLayout_4.addWidget(self.rb_path_merge, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.gb_log_merge)
        self.gridLayout_5.addLayout(self.verticalLayout_3, 2, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem10, 7, 0, 1, 1)
        self.l_pagetitle_merge = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setItalic(True)
        self.l_pagetitle_merge.setFont(font)
        self.l_pagetitle_merge.setAlignment(QtCore.Qt.AlignCenter)
        self.l_pagetitle_merge.setObjectName("l_pagetitle_merge")
        self.gridLayout_5.addWidget(self.l_pagetitle_merge, 0, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem11, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.b_savelog_merge = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_savelog_merge.sizePolicy().hasHeightForWidth())
        self.b_savelog_merge.setSizePolicy(sizePolicy)
        self.b_savelog_merge.setMinimumSize(QtCore.QSize(160, 45))
        self.b_savelog_merge.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.b_savelog_merge.setIcon(icon3)
        self.b_savelog_merge.setIconSize(QtCore.QSize(24, 24))
        self.b_savelog_merge.setObjectName("b_savelog_merge")
        self.horizontalLayout_3.addWidget(self.b_savelog_merge)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem13, 3, 0, 1, 1)
        self.tab_mode.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tab_mode, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 720, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionReadme = QtWidgets.QAction(MainWindow)
        self.actionReadme.setMenuRole(QtWidgets.QAction.ApplicationSpecificRole)
        self.actionReadme.setObjectName("actionReadme")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout.setObjectName("actionAbout")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionClose.setObjectName("actionClose")
        self.menuHelp.addAction(self.actionReadme)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionClose)
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.l_name.setBuddy(self.le_name)
        self.l_path.setBuddy(self.le_path)
        self.l_image.setBuddy(self.le_image)
        self.l_marquee.setBuddy(self.le_marquee)
        self.l_video.setBuddy(self.le_video)
        self.l_desc.setBuddy(self.pte_desc)
        self.l_developer.setBuddy(self.le_developer)
        self.l_publisher.setBuddy(self.le_publisher)
        self.l_releasedate.setBuddy(self.le_releasedate)
        self.l_genre.setBuddy(self.le_genre)
        self.l_players.setBuddy(self.le_players)
        self.l_rating.setBuddy(self.le_rating)
        self.l_new_merge.setBuddy(self.le_new_merge)
        self.l_original_merge.setBuddy(self.le_original_merge)

        self.retranslateUi(MainWindow)
        self.tab_mode.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.b_new_addgame.setToolTip(_translate("MainWindow", "Clear the entry fields and start all over again."))
        self.b_new_addgame.setText(_translate("MainWindow", " &Clear"))
        self.b_import_addgame.setToolTip(_translate("MainWindow", "Load up and copy a game entry. Any of the fields above are used as filters."))
        self.b_import_addgame.setText(_translate("MainWindow", " Imp&ort"))
        self.b_preview_addgame.setToolTip(_translate("MainWindow", "The XML representation of this game entry"))
        self.b_preview_addgame.setText(_translate("MainWindow", " Previe&w"))
        self.l_pagetitle_addgame.setText(_translate("MainWindow", "Add a single game entry to an existing or new gamelist.xml file."))
        self.l_name.setToolTip(_translate("MainWindow", "game title"))
        self.l_name.setText(_translate("MainWindow", "&name"))
        self.le_name.setToolTip(_translate("MainWindow", "game title"))
        self.l_path.setToolTip(_translate("MainWindow", "Required: Path to ROM file."))
        self.l_path.setText(_translate("MainWindow", "&path *"))
        self.le_path.setToolTip(_translate("MainWindow", "Required: Path to ROM file."))
        self.l_image.setText(_translate("MainWindow", "&image"))
        self.l_marquee.setText(_translate("MainWindow", "mar&quee"))
        self.l_video.setText(_translate("MainWindow", "&video"))
        self.l_desc.setText(_translate("MainWindow", "des&c"))
        self.l_developer.setText(_translate("MainWindow", "de&veloper"))
        self.l_publisher.setText(_translate("MainWindow", "p&ublisher"))
        self.l_releasedate.setToolTip(_translate("MainWindow", "YYYYMMDD"))
        self.l_releasedate.setText(_translate("MainWindow", "&releasedate"))
        self.le_releasedate.setToolTip(_translate("MainWindow", "YYYYMMDD"))
        self.l_genre.setText(_translate("MainWindow", "&genre"))
        self.l_players.setText(_translate("MainWindow", "p&layers"))
        self.l_rating.setToolTip(_translate("MainWindow", "0.65"))
        self.l_rating.setText(_translate("MainWindow", "&rating"))
        self.le_rating.setToolTip(_translate("MainWindow", "0.65"))
        self.b_save_addgame.setToolTip(_translate("MainWindow", "Convert to XML game entry and add output to gamelist.xml file."))
        self.b_save_addgame.setText(_translate("MainWindow", " &Save to gamelist…"))
        self.tab_mode.setTabText(self.tab_mode.indexOf(self.tab), _translate("MainWindow", "&Add Game"))
        self.b_save_merge.setToolTip(_translate("MainWindow", "Start merging and save output to gamelist.xml file format."))
        self.b_save_merge.setText(_translate("MainWindow", " &Save to gamelist…"))
        self.l_new_merge.setToolTip(_translate("MainWindow", "Required: Path to XML file with additional content."))
        self.l_new_merge.setText(_translate("MainWindow", "Add co&ntent *"))
        self.tb_new_merge.setToolTip(_translate("MainWindow", "Select a file with new gamelist.xml content for merge operation."))
        self.tb_new_merge.setText(_translate("MainWindow", "..."))
        self.tb_original_merge.setToolTip(_translate("MainWindow", "Select a file with original gamelist.xml content for merge operation."))
        self.tb_original_merge.setText(_translate("MainWindow", "..."))
        self.l_original_merge.setToolTip(_translate("MainWindow", "Required: Path to XML file with missing content."))
        self.l_original_merge.setText(_translate("MainWindow", "&Base content *"))
        self.label.setToolTip(_translate("MainWindow", "What to do when same game is detected?"))
        self.label.setText(_translate("MainWindow", "Duplicates Mode:"))
        self.rb_ignore_merge.setToolTip(_translate("MainWindow", "Use game from Base content"))
        self.rb_ignore_merge.setText(_translate("MainWindow", "&Ignore"))
        self.rb_update_merge.setToolTip(_translate("MainWindow", "Merge both games and each of their tags. Add content has higher priority."))
        self.rb_update_merge.setText(_translate("MainWindow", "Update"))
        self.gb_log_merge.setToolTip(_translate("MainWindow", "Log shows changes or additions only. Output gamelist file contains all games."))
        self.gb_log_merge.setTitle(_translate("MainWindow", "Log:"))
        self.rb_xml_merge.setText(_translate("MainWindow", "&xml"))
        self.rb_name_merge.setText(_translate("MainWindow", "&name"))
        self.rb_path_merge.setText(_translate("MainWindow", "&path"))
        self.l_pagetitle_merge.setText(_translate("MainWindow", "Combine two gamelist.xml files to add missing game entries."))
        self.b_savelog_merge.setToolTip(_translate("MainWindow", "Save current Log view to file."))
        self.b_savelog_merge.setText(_translate("MainWindow", " Save &log"))
        self.tab_mode.setTabText(self.tab_mode.indexOf(self.tab_2), _translate("MainWindow", "&Merge Gamelists"))
        self.menuHelp.setTitle(_translate("MainWindow", "He&lp"))
        self.actionReadme.setText(_translate("MainWindow", "&Manual"))
        self.actionAbout.setText(_translate("MainWindow", "&About"))
        self.actionClose.setText(_translate("MainWindow", "&Exit"))
from gui import images_rc
