import os

from PySide6.QtWidgets import *
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt

from view.MainWindowView import MainWindowView
from service.MainWindowService import MainWindowService
from model.MainWindowModel import MainWindowModel


class MainWindowController:
	def __init__(self, mainWindowView: MainWindowView, mainWindowService: MainWindowService, mainWindowModel: MainWindowModel):
		self.view_: MainWindowView = mainWindowView
		self.service_: MainWindowService = mainWindowService
		self.model_: MainWindowModel = mainWindowModel

		self._tableInit()
		self._connectionInit()

	def _tableInit(self) -> None:
		self.view_.courseTableView_.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.view_.classTableView_.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.view_.autoCourseTableView_.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

		self.model_.courseTableProxyModel_.setSourceModel(self.model_.courseTableModel_)
		self.model_.courseTableProxyModel_.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		self.model_.courseTableProxyModel_.setFilterKeyColumn(-1)

		self.view_.courseTableView_.setModel(self.model_.courseTableProxyModel_)
		self.view_.classTableView_.setModel(self.model_.classTableModel_)
		self.view_.autoCourseTableView_.setModel(self.model_.autoClassTableModel_)

	def _connectionInit(self) -> None:
		# from view
		self.view_.epochComboBox_.currentIndexChanged.connect(self._onEpochIndexChanged)
		self.view_.typeComboBox_.currentIndexChanged.connect(self._onTypeIndexChanged)

		self.view_.refreshBtn_.clicked.connect(self._onRefreshBtnClicked)
		self.view_.chooseClassBtn_.clicked.connect(self._onChooseClassBtnClicked)
		self.view_.addAutoBtn_.clicked.connect(self._onAddAutoBtnClicked)
		self.view_.delAutoBtn_.clicked.connect(self._onDelAutoBtnClicked)
		self.view_.switchAutoBtn_.clicked.connect(self._onSwitchAutoBtnClicked)
		self.view_.saveAutoBtn_.clicked.connect(self._onSaveAutoBtnClicked)
		self.view_.clearAutoBtn_.clicked.connect(self._onClearAutoBtnClicked)
		self.view_.loadAutoBtn_.clicked.connect(lambda: self._onLoadAutoBtnClicked(False))

		self.view_.searchEdit_.textChanged.connect(self._onSearchTextChanged)

		self.view_.courseTableView_.clicked.connect(self._onCourseTableClicked)
		self.view_.classTableView_.clicked.connect(self._onClassTableClicked)
		self.view_.autoCourseTableView_.clicked.connect(self._onAutoCourseTableClicked)

		self.view_.exitMsgBox_.accepted.connect(self._onExit)
		self.view_.loadAutoMsgBox_.accepted.connect(lambda: self._onLoadAutoBtnClicked(True))

		# from LoginController
		self.toMainWindow_.toMainWindowSignal_.connect(self._viewInit)

		# from service
		self.service_.dataUpdate_.updateEpochTime_.connect(self._updateEpochTime)
		self.service_.dataUpdate_.updateTypeName_.connect(self._updateTypeName)

		# inside service
		self.service_.dataUpdate_.updateChooseClass_.connect(self.service_.updateChooseClassRes)
		self.service_.timer_.timeout.connect(self.service_.autoChooseClass)

	def viewInit(self, userName: str) -> None:
		self.model_.userName_ = userName
		self.service_.getEpochList()

		self.view_.show()

	def _updateEpochTime(self) -> None:
		# set epoch time to GUI
		self.view_.epochComboBox_.clear()
		self.view_.epochComboBox_.addItems(self.model_.epochTimeList_)

	def _onEpochIndexChanged(self) -> None:
		self.model_.currentEpochIndex_ = self.view_.epochComboBox_.currentIndex()
		self.service_.getTypeList()

	def _updateTypeName(self) -> None:
		# set course type to GUI
		self.view_.typeComboBox_.clear()
		self.view_.typeComboBox_.addItems(self.model_.typeNameList_)

		self._onTypeIndexChanged()

	def _onTypeIndexChanged(self) -> None:
		self.model_.currentTypeIndex_ = self.view_.typeComboBox_.currentIndex()
		self.service_.getTypeData(self.view_.typeComboBox_.count())
		self.view_.chooseClassBtn_.setDisabled(True)
		self.view_.addAutoBtn_.setDisabled(True)

	def _onRefreshBtnClicked(self) -> None:
		self.service_.getCourseData()

	def _onSearchTextChanged(self) -> None:
		text = self.view_.searchEdit_.text()
		self.model_.courseTableProxyModel_.setFilterRegularExpression(text)

	def _onCourseTableClicked(self, index: QModelIndex) -> None:
		self.model_.selectedCourse_ = self.model_.courseTableProxyModel_.mapToSource(index)
		self.service_.getClassData()
		self.view_.chooseClassBtn_.setDisabled(True)
		self.view_.addAutoBtn_.setDisabled(True)

	def _onClassTableClicked(self, index: QModelIndex) -> None:
		self.model_.selectedClass_ = index
		self.service_.getClassIndex()
		self.view_.chooseClassBtn_.setDisabled(False)
		if self.model_.type_ == "gxk":
			self.view_.addAutoBtn_.setDisabled(False)

	def _onChooseClassBtnClicked(self) -> None:
		self.service_.chooseClass()

	def _onAddAutoBtnClicked(self) -> None:
		self.service_.addAutoCourse()

	def _onAutoCourseTableClicked(self) -> None:
		self.model_.selectedAutoCourse_ = self.view_.autoCourseTableView_.selectionModel().selectedRows()

	def _onDelAutoBtnClicked(self) -> None:
		self.service_.deleteAutoCourse()

	def _onSwitchAutoBtnClicked(self) -> None:
		self.model_.autoClassIndex_ = 0
		self.service_.timerSwitch()
		text = self.view_.switchAutoBtn_.text()
		text = ("停止" if text[0:2] == "开始" else "开始") + text[2:]
		self.view_.switchAutoBtn_.setText(text)

	def _onSaveAutoBtnClicked(self) -> None:
		self.model_.saveFileName_, _ = self.view_.autoFileDialog_.getSaveFileName(self.view_, "保存文件", os.getcwd(),
		                                                                          "Json files (*.json);;Text files (*.txt)")
		self.service_.saveAutoCourse()

	def _onClearAutoBtnClicked(self) -> None:
		self.service_.clearAutoCourse()

	def _onLoadAutoBtnClicked(self, accepted: bool) -> None:
		if accepted or self.model_.autoClassTableModel_.rowCount() == 0:
			self.model_.loadFileName_, _ = self.view_.autoFileDialog_.getOpenFileName(self.view_, "打开文件",
			                                                                          os.getcwd(),
			                                                                          "Json files (*.json);;Text files (*.txt)")
			self.service_.loadAutoCourse()
		else:
			self.view_.loadAutoMsgBox_.exec()

	def _onExit(self) -> None:
		self.view_.close()
		self.service_.quitApp()
		QApplication.quit()
