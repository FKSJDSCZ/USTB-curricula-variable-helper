from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QCloseEvent
from ui.mainWindowUi import Ui_mainWindow


class MainWindowView(QMainWindow):
	def __init__(self, parent: QMainWindow = None):
		super(MainWindowView, self).__init__(parent)
		self.mainWindow_ = Ui_mainWindow()
		self.mainWindow_.setupUi(self)

		self.autoFileDialog_: QFileDialog = QFileDialog(self)

		self._exitMsgBoxInit()
		self._loadAutoMsgBoxInit()

	def _exitMsgBoxInit(self) -> None:
		self.exitMsgBox_: QMessageBox = QMessageBox(self)
		self.exitMsgBox_.setWindowTitle("退出应用")
		self.exitMsgBox_.setText("确认退出应用？")
		self.exitMsgBox_.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		self.exitMsgBox_.button(QMessageBox.StandardButton.Yes).setText("退出")
		self.exitMsgBox_.button(QMessageBox.StandardButton.No).setText("取消")

	def _loadAutoMsgBoxInit(self) -> None:
		self.loadAutoMsgBox_: QMessageBox = QMessageBox(self)
		self.loadAutoMsgBox_.setWindowTitle("警告")
		self.loadAutoMsgBox_.setText("从文件加载课程会覆盖表格中现有的课程。是否继续？")
		self.loadAutoMsgBox_.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		self.loadAutoMsgBox_.button(QMessageBox.StandardButton.Yes).setText("继续")
		self.loadAutoMsgBox_.button(QMessageBox.StandardButton.No).setText("取消")

	def closeEvent(self, event: QCloseEvent) -> None:
		self.exitMsgBox_.exec()
		event.ignore()
