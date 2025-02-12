from PySide6.QtCore import pyqtSignal, QObject


class QrLogin(QObject):
	qrLoginSignal_ = pyqtSignal(bool, str)

	def __init__(self):
		super().__init__()


class ToMainWindow(QObject):
	toMainWindowSignal_ = pyqtSignal(str)

	def __init__(self):
		super().__init__()


class DataUpdateSignals(QObject):
	updateEpochTime_ = pyqtSignal()
	updateTypeName_ = pyqtSignal()
	updateChooseClass_ = pyqtSignal(bool, str)

	def __init__(self):
		super().__init__()
