from PyQt6.QtWidgets import *
from PyQt6 import uic


class LoginView(QWidget):
	def __init__(self, parent: QWidget = None):
		super(LoginView, self).__init__(parent)
		self.ui_: QWidget = uic.loadUi("view/login.ui", self)

		self.userAccountEdit_: QLineEdit = self.userAccountEdit
		self.userPasswordEdit_: QLineEdit = self.userPasswordEdit

		self.warningLabel_: QLabel = self.warningLabel
		self.qrCodeLabel_: QLabel = self.qrCodeLabel

		self.loginBtn_: QPushButton = self.loginBtn
		self.refreshBtn_: QPushButton = self.refreshBtn
