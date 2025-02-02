from PyQt6.QtWidgets import *
from PyQt6.QtGui import QCloseEvent
from PyQt6 import uic


class MainWindowView(QMainWindow):
	def __init__(self, parent: QWidget = None):
		super(MainWindowView, self).__init__(parent)
		self.ui_: QWidget = uic.loadUi("view/mainWindow.ui", self)

		self.epochComboBox_: QComboBox = self.epochComboBox
		self.typeComboBox_: QComboBox = self.typeComboBox

		self.refreshBtn_: QPushButton = self.refresh
		self.chooseClassBtn_: QPushButton = self.chooseClass
		self.addAutoBtn_: QPushButton = self.addAuto
		self.delAutoBtn_: QPushButton = self.delAutoCourse
		self.switchAutoBtn_: QPushButton = self.autoCourseSwitch
		self.saveAutoBtn_: QPushButton = self.saveCourseList
		self.clearAutoBtn_: QPushButton = self.clearCourseList
		self.loadAutoBtn_: QPushButton = self.loadCourseList

		self.searchEdit_: QLineEdit = self.searchEdit

		self.courseTableView_: QTableView = self.courseTable
		self.classTableView_: QTableView = self.classTable
		self.autoCourseTableView_: QTableView = self.autoCourseTable

		self.tabWidget_: QTabWidget = self.tabWidget

		self.exitMsgBox_: QMessageBox = QMessageBox(self)
		self.loadAutoMsgBox_: QMessageBox = QMessageBox(self)
		self.autoFileDialog_: QFileDialog = QFileDialog(self)

		self._exitMsgBoxInit()
		self._loadAutoMsgBoxInit()

	def _exitMsgBoxInit(self) -> None:
		self.exitMsgBox_.setWindowTitle("退出应用")
		self.exitMsgBox_.setText("确认退出应用？")
		self.exitMsgBox_.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		self.exitMsgBox_.button(QMessageBox.StandardButton.Yes).setText("退出")
		self.exitMsgBox_.button(QMessageBox.StandardButton.No).setText("取消")

	def _loadAutoMsgBoxInit(self) -> None:
		self.loadAutoMsgBox_.setWindowTitle("警告")
		self.loadAutoMsgBox_.setText("从文件加载课程会覆盖表格中现有的课程。是否继续？")
		self.loadAutoMsgBox_.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		self.loadAutoMsgBox_.button(QMessageBox.StandardButton.Yes).setText("继续")
		self.loadAutoMsgBox_.button(QMessageBox.StandardButton.No).setText("取消")

	def closeEvent(self, event: QCloseEvent) -> None:
		self.exitMsgBox_.exec()
		event.ignore()
