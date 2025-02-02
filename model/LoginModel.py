from PyQt6.QtGui import QPixmap


class LoginModel:
	def __init__(self):
		self.userAccount_: str = str()
		self.userPassword_: str = str()
		self.token_: str = str()
		self.appId_: str = str()
		self.sid_: str = str()

		self.qrCodePixmap_: QPixmap = QPixmap()
