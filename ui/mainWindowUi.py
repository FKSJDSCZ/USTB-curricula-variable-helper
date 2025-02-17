# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTableView, QTreeView, QVBoxLayout,
    QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1031, 678)
        self.preference = QAction(mainWindow)
        self.preference.setObjectName(u"preference")
        self.help = QAction(mainWindow)
        self.help.setObjectName(u"help")
        self.about = QAction(mainWindow)
        self.about.setObjectName(u"about")
        self.feedback = QAction(mainWindow)
        self.feedback.setObjectName(u"feedback")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.epochTreeView = QTreeView(self.mainSplitter)
        self.epochTreeView.setObjectName(u"epochTreeView")
        self.epochTreeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.epochTreeView.setTabKeyNavigation(True)
        self.epochTreeView.setDragDropOverwriteMode(True)
        self.epochTreeView.setAnimated(True)
        self.mainSplitter.addWidget(self.epochTreeView)
        self.rightSplitter = QSplitter(self.mainSplitter)
        self.rightSplitter.setObjectName(u"rightSplitter")
        self.rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.serviceTabWidget = QTabWidget(self.rightSplitter)
        self.serviceTabWidget.setObjectName(u"serviceTabWidget")
        self.courseQuery = QWidget()
        self.courseQuery.setObjectName(u"courseQuery")
        self.gridLayout_2 = QGridLayout(self.courseQuery)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.courseQuerySplitter = QSplitter(self.courseQuery)
        self.courseQuerySplitter.setObjectName(u"courseQuerySplitter")
        self.courseQuerySplitter.setOrientation(Qt.Orientation.Vertical)
        self.layoutWidget = QWidget(self.courseQuerySplitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.courseTableLayout = QVBoxLayout(self.layoutWidget)
        self.courseTableLayout.setObjectName(u"courseTableLayout")
        self.courseTableLayout.setContentsMargins(0, 0, 0, 0)
        self.searchLayout = QHBoxLayout()
        self.searchLayout.setObjectName(u"searchLayout")
        self.searchEdit = QLineEdit(self.layoutWidget)
        self.searchEdit.setObjectName(u"searchEdit")

        self.searchLayout.addWidget(self.searchEdit)

        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.searchLayout.addItem(self.horizontalSpacer)


        self.courseTableLayout.addLayout(self.searchLayout)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.courseTableLayout.addWidget(self.label_3)

        self.courseTableView = QTableView(self.layoutWidget)
        self.courseTableView.setObjectName(u"courseTableView")
        self.courseTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.courseTableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.courseTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.courseTableView.setSortingEnabled(True)
        self.courseTableView.setWordWrap(False)
        self.courseTableView.horizontalHeader().setMinimumSectionSize(0)
        self.courseTableView.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.courseTableView.horizontalHeader().setStretchLastSection(True)
        self.courseTableView.verticalHeader().setMinimumSectionSize(0)
        self.courseTableView.verticalHeader().setDefaultSectionSize(20)

        self.courseTableLayout.addWidget(self.courseTableView)

        self.courseQuerySplitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.courseQuerySplitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.classTableLayout = QVBoxLayout(self.layoutWidget1)
        self.classTableLayout.setObjectName(u"classTableLayout")
        self.classTableLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.classTableLayout.addWidget(self.label_4)

        self.classTableView = QTableView(self.layoutWidget1)
        self.classTableView.setObjectName(u"classTableView")
        self.classTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.classTableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.classTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.classTableView.setWordWrap(False)
        self.classTableView.horizontalHeader().setMinimumSectionSize(0)
        self.classTableView.horizontalHeader().setStretchLastSection(True)
        self.classTableView.verticalHeader().setVisible(True)
        self.classTableView.verticalHeader().setMinimumSectionSize(0)
        self.classTableView.verticalHeader().setDefaultSectionSize(20)

        self.classTableLayout.addWidget(self.classTableView)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer_2)

        self.chooseClassBtn = QPushButton(self.layoutWidget1)
        self.chooseClassBtn.setObjectName(u"chooseClassBtn")
        self.chooseClassBtn.setMinimumSize(QSize(90, 30))

        self.buttonLayout.addWidget(self.chooseClassBtn)

        self.addAutoBtn = QPushButton(self.layoutWidget1)
        self.addAutoBtn.setObjectName(u"addAutoBtn")
        self.addAutoBtn.setMinimumSize(QSize(90, 30))

        self.buttonLayout.addWidget(self.addAutoBtn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer_3)


        self.classTableLayout.addLayout(self.buttonLayout)

        self.courseQuerySplitter.addWidget(self.layoutWidget1)

        self.gridLayout_2.addWidget(self.courseQuerySplitter, 0, 0, 1, 1)

        self.serviceTabWidget.addTab(self.courseQuery, "")
        self.autoSelector = QWidget()
        self.autoSelector.setObjectName(u"autoSelector")
        self.gridLayout = QGridLayout(self.autoSelector)
        self.gridLayout.setObjectName(u"gridLayout")
        self.autoSelectorLayout = QVBoxLayout()
        self.autoSelectorLayout.setObjectName(u"autoSelectorLayout")
        self.label_6 = QLabel(self.autoSelector)
        self.label_6.setObjectName(u"label_6")

        self.autoSelectorLayout.addWidget(self.label_6)

        self.autoCourseTableLayout = QHBoxLayout()
        self.autoCourseTableLayout.setObjectName(u"autoCourseTableLayout")
        self.autoClassTableView = QTableView(self.autoSelector)
        self.autoClassTableView.setObjectName(u"autoClassTableView")
        self.autoClassTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.autoClassTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.autoClassTableView.setWordWrap(False)
        self.autoClassTableView.horizontalHeader().setMinimumSectionSize(0)
        self.autoClassTableView.horizontalHeader().setStretchLastSection(True)
        self.autoClassTableView.verticalHeader().setVisible(True)
        self.autoClassTableView.verticalHeader().setMinimumSectionSize(0)
        self.autoClassTableView.verticalHeader().setDefaultSectionSize(20)

        self.autoCourseTableLayout.addWidget(self.autoClassTableView)

        self.autoButtonLayout = QVBoxLayout()
        self.autoButtonLayout.setObjectName(u"autoButtonLayout")
        self.delAutoBtn = QPushButton(self.autoSelector)
        self.delAutoBtn.setObjectName(u"delAutoBtn")
        self.delAutoBtn.setMinimumSize(QSize(110, 30))

        self.autoButtonLayout.addWidget(self.delAutoBtn)

        self.switchAutoBtn = QPushButton(self.autoSelector)
        self.switchAutoBtn.setObjectName(u"switchAutoBtn")
        self.switchAutoBtn.setMinimumSize(QSize(110, 30))

        self.autoButtonLayout.addWidget(self.switchAutoBtn)

        self.saveAutoBtn = QPushButton(self.autoSelector)
        self.saveAutoBtn.setObjectName(u"saveAutoBtn")
        self.saveAutoBtn.setMinimumSize(QSize(110, 30))

        self.autoButtonLayout.addWidget(self.saveAutoBtn)

        self.clearAutoBtn = QPushButton(self.autoSelector)
        self.clearAutoBtn.setObjectName(u"clearAutoBtn")
        self.clearAutoBtn.setMinimumSize(QSize(110, 30))

        self.autoButtonLayout.addWidget(self.clearAutoBtn)

        self.loadAutoBtn = QPushButton(self.autoSelector)
        self.loadAutoBtn.setObjectName(u"loadAutoBtn")
        self.loadAutoBtn.setMinimumSize(QSize(110, 30))

        self.autoButtonLayout.addWidget(self.loadAutoBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.autoButtonLayout.addItem(self.verticalSpacer)


        self.autoCourseTableLayout.addLayout(self.autoButtonLayout)


        self.autoSelectorLayout.addLayout(self.autoCourseTableLayout)


        self.gridLayout.addLayout(self.autoSelectorLayout, 0, 0, 1, 1)

        self.serviceTabWidget.addTab(self.autoSelector, "")
        self.rightSplitter.addWidget(self.serviceTabWidget)
        self.layoutWidget2 = QWidget(self.rightSplitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.logLayout = QVBoxLayout(self.layoutWidget2)
        self.logLayout.setObjectName(u"logLayout")
        self.logLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.layoutWidget2)
        self.label_5.setObjectName(u"label_5")

        self.logLayout.addWidget(self.label_5)

        self.logOutput = QPlainTextEdit(self.layoutWidget2)
        self.logOutput.setObjectName(u"logOutput")
        self.logOutput.setReadOnly(True)
        self.logOutput.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.logLayout.addWidget(self.logOutput)

        self.rightSplitter.addWidget(self.layoutWidget2)
        self.mainSplitter.addWidget(self.rightSplitter)

        self.gridLayout_3.addWidget(self.mainSplitter, 0, 0, 1, 1)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1031, 33))
        font = QFont()
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.preference)
        self.menu_2.addAction(self.help)
        self.menu_2.addAction(self.about)
        self.menu_2.addAction(self.feedback)

        self.retranslateUi(mainWindow)

        self.serviceTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"\u9009\u8bfe\u52a9\u624b", None))
        self.preference.setText(QCoreApplication.translate("mainWindow", u"\u9996\u9009\u9879", None))
        self.help.setText(QCoreApplication.translate("mainWindow", u"\u4f7f\u7528\u5e2e\u52a9", None))
        self.about.setText(QCoreApplication.translate("mainWindow", u"\u5173\u4e8e\u8f6f\u4ef6", None))
        self.feedback.setText(QCoreApplication.translate("mainWindow", u"\u95ee\u9898\u53cd\u9988", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("mainWindow", u"\u952e\u5165\u4ee5\u641c\u7d22", None))
        self.label_3.setText(QCoreApplication.translate("mainWindow", u"\u8bfe\u7a0b\u5217\u8868\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("mainWindow", u"\u53ef\u9009\u8bb2\u53f0\uff1a", None))
        self.chooseClassBtn.setText(QCoreApplication.translate("mainWindow", u"\u9009\u62e9\u8bb2\u53f0", None))
        self.addAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u52a0\u5165\u62a2\u8bfe", None))
        self.serviceTabWidget.setTabText(self.serviceTabWidget.indexOf(self.courseQuery), QCoreApplication.translate("mainWindow", u"\u9009\u8bfe\u4e2d\u5fc3", None))
        self.label_6.setText(QCoreApplication.translate("mainWindow", u"\u5faa\u73af\u62a2\u8bfe\u8bfe\u7a0b\u5217\u8868\uff1a", None))
        self.delAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u5220\u9664\u9009\u4e2d\u7684\u8bfe\u7a0b", None))
        self.switchAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u5f00\u59cb\u5faa\u73af\u62a2\u8bfe", None))
        self.saveAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u4fdd\u5b58\u8bfe\u7a0b\u5217\u8868", None))
        self.clearAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u6e05\u7a7a\u8bfe\u7a0b\u5217\u8868", None))
        self.loadAutoBtn.setText(QCoreApplication.translate("mainWindow", u"\u8bfb\u53d6\u8bfe\u7a0b\u5217\u8868", None))
        self.serviceTabWidget.setTabText(self.serviceTabWidget.indexOf(self.autoSelector), QCoreApplication.translate("mainWindow", u"\u62a2\u8bfe\u4e2d\u5fc3", None))
        self.label_5.setText(QCoreApplication.translate("mainWindow", u"\u64cd\u4f5c\u65e5\u5fd7\uff1a", None))
        self.menu.setTitle(QCoreApplication.translate("mainWindow", u"\u8bbe\u7f6e", None))
        self.menu_2.setTitle(QCoreApplication.translate("mainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

