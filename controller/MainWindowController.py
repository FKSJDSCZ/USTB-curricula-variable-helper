import os
import logging

from PySide6.QtWidgets import QHeaderView, QApplication
from PySide6.QtCore import QObject, Qt, QModelIndex

from view.MainWindowView import MainWindowView
from service.MainWindowService import MainWindowService
from model.MainWindowModel import MainWindowModel


class MainWindowController(QObject):
	def __init__(self, mainWindowView: MainWindowView, mainWindowService: MainWindowService, mainWindowModel: MainWindowModel, /):
		super().__init__()
		self.view_: MainWindowView = mainWindowView
		self.service_: MainWindowService = mainWindowService
		self.model_: MainWindowModel = mainWindowModel

		self._modelBindInit()
		self._connectionInit()

	def _modelBindInit(self) -> None:
		self.view_.mainWindow_.courseTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.view_.mainWindow_.classTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.view_.mainWindow_.autoClassTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

		self.model_.courseTableProxyModel_.setSourceModel(self.model_.courseTableModel_)
		self.model_.courseTableProxyModel_.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		self.model_.courseTableProxyModel_.setFilterKeyColumn(-1)

		self.view_.mainWindow_.epochTreeView.setModel(self.model_.epochTreeModel_)
		self.view_.mainWindow_.courseTableView.setModel(self.model_.courseTableProxyModel_)
		self.view_.mainWindow_.classTableView.setModel(self.model_.classTableModel_)
		self.view_.mainWindow_.autoClassTableView.setModel(self.model_.autoClassTableModel_)

	def _connectionInit(self) -> None:
		# from view
		self.view_.mainWindow_.epochTreeView.clicked.connect(self._onEpochTreeClicked)

		self.view_.mainWindow_.chooseClassBtn.clicked.connect(lambda: self.service_.chooseClass(0))
		self.view_.mainWindow_.addAutoBtn.clicked.connect(self._onAddAutoBtnClicked)
		self.view_.mainWindow_.delAutoBtn.clicked.connect(self._onDelAutoBtnClicked)
		self.view_.mainWindow_.switchAutoBtn.clicked.connect(self._onSwitchAutoBtnClicked)
		self.view_.mainWindow_.saveAutoBtn.clicked.connect(self._onSaveAutoBtnClicked)
		self.view_.mainWindow_.clearAutoBtn.clicked.connect(self._onClearAutoBtnClicked)
		self.view_.mainWindow_.loadAutoBtn.clicked.connect(lambda: self._onLoadAutoBtnClicked(False))

		self.view_.mainWindow_.searchEdit.textChanged.connect(self._onSearchTextChanged)

		self.view_.mainWindow_.courseTableView.clicked.connect(self._onCourseTableClicked)
		self.view_.mainWindow_.classTableView.clicked.connect(self._onClassTableClicked)
		self.view_.mainWindow_.autoClassTableView.clicked.connect(self._onAutoClassTableClicked)

		self.view_.exitMsgBox_.accepted.connect(self._onExit)
		self.view_.loadAutoMsgBox_.accepted.connect(lambda: self._onLoadAutoBtnClicked(True))

		# from service
		self.service_.typeNameUpdated_.connect(lambda: self.view_.mainWindow_.epochTreeView.expand(self.model_.currentEpochIndex_))

		# inside service
		self.service_.chooseClassUpdated_.connect(self.service_.updateChooseClassRes)
		self.service_.timer_.timeout.connect(self.service_.autoChooseClass)

	def viewInit(self, userName: str) -> None:
		"""Before step 0"""
		self.view_.mainWindow_.chooseClassBtn.setDisabled(True)
		self.view_.mainWindow_.addAutoBtn.setDisabled(True)
		self.model_.userName_ = userName
		self.service_.getEpochList()
		self.view_.show()

	def _onEpochTreeClicked(self, index: QModelIndex) -> None:
		self.view_.mainWindow_.chooseClassBtn.setDisabled(True)
		self.view_.mainWindow_.addAutoBtn.setDisabled(True)

		parentIndex = index.parent()
		if parentIndex.isValid():
			"""Before step 4: get selected course type index & get course list"""
			self.model_.currentTypeIndex_ = index
			self.service_.getCourseList()
		else:
			"""Before step 2: get selected epoch index"""
			if index != self.model_.currentEpochIndex_:
				if self.model_.currentEpochIndex_.row() != -1:
					self.model_.courseTableModel_.clear()
					self.model_.classTableModel_.clear()
					self.model_.epochTreeModel_.itemFromIndex(self.model_.currentEpochIndex_).setRowCount(0)
				self.model_.currentEpochIndex_ = index
				self.service_.getTypeList()

	def _onSearchTextChanged(self) -> None:
		text = self.view_.mainWindow_.searchEdit.text()
		self.model_.courseTableProxyModel_.setFilterRegularExpression(text)

	def _onCourseTableClicked(self, index: QModelIndex) -> None:
		"""Before step 6: get selected course index"""
		self.view_.mainWindow_.chooseClassBtn.setDisabled(True)
		self.view_.mainWindow_.addAutoBtn.setDisabled(True)
		self.model_.selectedCourse_ = self.model_.courseTableProxyModel_.mapToSource(index)
		self.service_.getClassList()

	def _onClassTableClicked(self, index: QModelIndex) -> None:
		self.model_.selectedClass_ = index
		self.service_.getClassIndex()
		self.view_.mainWindow_.chooseClassBtn.setEnabled(True)
		if self.model_.type_ == "gxk":
			self.view_.mainWindow_.addAutoBtn.setEnabled(True)

	def _onAddAutoBtnClicked(self) -> None:
		self.service_.addAutoClass()

	def _onAutoClassTableClicked(self) -> None:
		self.model_.selectedAutoClass = self.view_.mainWindow_.autoClassTableView.selectionModel().selectedRows()

	def _onDelAutoBtnClicked(self) -> None:
		self.service_.deleteAutoClass()

	def _onSwitchAutoBtnClicked(self) -> None:
		self.model_.autoClassIndex_ = 0
		self.service_.timerSwitch()
		text = self.view_.mainWindow_.switchAutoBtn.text()
		text = ("停止" if text[0:2] == "开始" else "开始") + text[2:]
		self.view_.mainWindow_.switchAutoBtn.setText(text)

	def _onSaveAutoBtnClicked(self) -> None:
		self.model_.saveFileName_, _ = self.view_.autoFileDialog_.getSaveFileName(
			self.view_,
			"保存文件",
			os.getcwd(),
			"Json files (*.json);;Text files (*.txt)"
		)
		self.service_.saveAutoClass()

	def _onClearAutoBtnClicked(self) -> None:
		self.service_.clearAutoClass()

	def _onLoadAutoBtnClicked(self, accepted: bool) -> None:
		if accepted or self.model_.autoClassTableModel_.rowCount() == 0:
			self.model_.loadFileName_, _ = self.view_.autoFileDialog_.getOpenFileName(
				self.view_,
				"打开文件",
				os.getcwd(),
				"Json files (*.json);;Text files (*.txt)"
			)
			self.service_.loadAutoClass()
		else:
			self.view_.loadAutoMsgBox_.exec()

	def _onExit(self) -> None:
		self.view_.close()
		self.service_.quitApp()
