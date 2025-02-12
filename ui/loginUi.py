# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_login(object):
    def setupUi(self, login):
        if not login.objectName():
            login.setObjectName(u"login")
        login.setEnabled(True)
        login.resize(590, 360)
        login.setMinimumSize(QSize(590, 360))
        login.setMaximumSize(QSize(590, 360))
        self.label = QLabel(login)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 30, 101, 41))
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label_2 = QLabel(login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 330, 81, 16))
        self.label_2.setOpenExternalLinks(True)
        self.phoneNumberEdit = QLineEdit(login)
        self.phoneNumberEdit.setObjectName(u"phoneNumberEdit")
        self.phoneNumberEdit.setGeometry(QRect(40, 120, 251, 31))
        self.label_3 = QLabel(login)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 80, 191, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_3.setFont(font1)
        self.label_3.setMouseTracking(True)
        self.smsCodeEdit = QLineEdit(login)
        self.smsCodeEdit.setObjectName(u"smsCodeEdit")
        self.smsCodeEdit.setGeometry(QRect(40, 180, 141, 31))
        self.loginBtn = QPushButton(login)
        self.loginBtn.setObjectName(u"loginBtn")
        self.loginBtn.setGeometry(QRect(100, 270, 81, 31))
        self.loginBtn.setAutoDefault(False)
        self.loginBtn.setFlat(False)
        self.refreshBtn = QPushButton(login)
        self.refreshBtn.setObjectName(u"refreshBtn")
        self.refreshBtn.setGeometry(QRect(390, 270, 71, 31))
        self.qrCodeLabel = QLabel(login)
        self.qrCodeLabel.setObjectName(u"qrCodeLabel")
        self.qrCodeLabel.setGeometry(QRect(330, 50, 201, 201))
        self.warningLabel = QLabel(login)
        self.warningLabel.setObjectName(u"warningLabel")
        self.warningLabel.setGeometry(QRect(40, 230, 251, 21))
        self.warningLabel.setStyleSheet(u"QLabel { color : red; }")
        self.warningLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.getmsgBtn = QPushButton(login)
        self.getmsgBtn.setObjectName(u"getmsgBtn")
        self.getmsgBtn.setGeometry(QRect(190, 180, 101, 31))
        self.getmsgBtn.setAutoDefault(False)
        self.getmsgBtn.setFlat(False)

        self.retranslateUi(login)

        QMetaObject.connectSlotsByName(login)
    # setupUi

    def retranslateUi(self, login):
        login.setWindowTitle(QCoreApplication.translate("login", u"\u7528\u6237\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("login", u"| \u7528\u6237\u767b\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("login", u"<a href=\"https://jwgl.ustb.edu.cn\">\u6559\u52a1\u7cfb\u7edf\u7f51\u7ad9</a>", None))
        self.phoneNumberEdit.setText(QCoreApplication.translate("login", u"18955566361", None))
        self.phoneNumberEdit.setPlaceholderText(QCoreApplication.translate("login", u"\u8bf7\u8f93\u5165\u624b\u673a\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("login", u"\u6b22\u8fce\u767b\u5f55\u5317\u4eac\u79d1\u6280\u5927\u5b66\u6559\u52a1\u5e73\u53f0", None))
        self.smsCodeEdit.setPlaceholderText(QCoreApplication.translate("login", u"\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801", None))
        self.loginBtn.setText(QCoreApplication.translate("login", u"\u767b\u5f55", None))
        self.refreshBtn.setText(QCoreApplication.translate("login", u"\u5237\u65b0", None))
        self.getmsgBtn.setText(QCoreApplication.translate("login", u"\u83b7\u53d6\u9a8c\u8bc1\u7801", None))
    # retranslateUi

